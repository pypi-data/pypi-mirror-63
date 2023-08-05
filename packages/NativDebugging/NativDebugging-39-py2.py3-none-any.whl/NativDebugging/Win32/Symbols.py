#
#   Symbols.py
#
#   Win32 PE symbols handler for python
#   https://github.com/assafnativ/NativDebugging.git
#   Nativ.Assaf@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

from __future__ import print_function
from builtins import range
from .Win32Structs import *
from comtypes.client import CreateObject, GetModule
import time
import os
from collections import namedtuple
from ..Patterns.Finder import *

class PDBSymbols(object):
    def __init__(self, fileName):
        self.msdia = GetModule("msdia140.dll")
        self.dataSource = CreateObject(self.msdia.DiaSource, interface=self.msdia.IDiaDataSource)
        ext = fileName.split(os.path.extsep)[-1]
        if 'pdb' == ext.lower():
            self.dataSource.loadDataFromPdb(fileName)
        else:
            symPath = os.environ.get('_NT_SYMBOL_PATH', 'SRV**\\\\symbols\\symbols')
            self.dataSource.loadDataForExe(fileName, symPath, None)
        self.session = self.dataSource.openSession()
        self.globalScope = self.session.globalScope

    def _getSingleSymbolObject(self, name, caseSensetive, symType):
        searchType = 1
        if not caseSensetive:
            searchType = 2
        children = self.globalScope.findChildren(symType, name, searchType)
        if (not children) or (0 == children.count):
            raise Exception("No children for type")
        if 1 != children.count:
            raise Exception("Ambiguous struct name. %d match" % children.count)
        return children.Item(0)

    def findGlobalSymbolRVA(self, name, caseSensetive=True):
        sym = self._getSingleSymbolObject(name, caseSensetive, SymTagEnum['SymTagData'])
        return sym.relativeVirtualAddress

    def getStruct(self, name, caseSensetive=True, maxDepth=20):
        child = self._getSingleSymbolObject(name, caseSensetive, SymTagEnum['SymTagUDT'])
        structName = child.name
        structElements = child.findChildren(0, None, 0)
        if not structElements:
            raise Exception("No struct elements")
        return self._getAllMembers(structElements, maxDepth=maxDepth)

    def _getAllMembers(self, structElements, base=0, maxDepth=20):
        members = []
        if 0 == maxDepth:
            return members
        for memberIndex in range(structElements.count):
            member = structElements.Item(memberIndex)
            members.extend(self._fetchSymData(member, base=base, maxDepth=maxDepth))
        return members

    def _fetchSymData(self, symData, base=0, maxDepth=20):
        if 0 == maxDepth:
            return []
        symTag = SymTagEnumTag[symData.symTag]
        if symTag == 'SymTagVTable':
            if None == symData.type.name:
                name = 'VFN_table'
            else:
                name = symData.type.name + '__VFN_table'
            return [SHAPE(name, (base+symData.offset, None), POINTER(isNullValid=True), fromStart=True)]
        elif symTag == 'SymTagBaseClass':
            return self._getAllMembers(symData.type.findChildren(0, None, 0), base=base+symData.offset, maxDepth=maxDepth)
        elif symTag == 'SymTagData':
            name = symData.name
            while name.startswith('_'):
                name = name[1:]
            dataKind = SymDataKindTag[symData.dataKind]
            if dataKind != 'Member':
                return []
            return self._getSymTagDataTypeAsShape(symData.Type, name, base+symData.offset, maxDepth=maxDepth)
        return []

    def _getAllChildren(self, dataType, symTypeFilter=None):
        if None == symTypeFilter:
            symTypeFilter = 0
        members = dataType.findChildren(symTypeFilter, None, 0)
        return [members.Item(x) for x in range(members.count)]

    def _getSymTagDataTypeAsShape(self, dataType, name, base, maxDepth):
        if 0 == maxDepth:
            return []
        name, base, dataType, dataTypeArgs, dataTypeKw = self._getSymTagDataType(dataType, name, base, maxDepth)
        if -1 == base:
            place = 0
        else:
            place = (base, None)
        return [SHAPE(name, place, dataType(*dataTypeArgs, **dataTypeKw), fromStart=True)]

    def _getSymTagDataType(self, dataType, name, base, maxDepth):
        dataTypeName = dataType.name
        if not dataTypeName:
            dataTypeName = 'void'
        memberTypeSymTag = SymTagEnumTag[dataType.symTag]
        if 'SymTagUDT' == memberTypeSymTag:
            if dataTypeName.startswith('std::basic_string<'):
                if 'wchar_t' in dataType.name:
                    isWide = True
                    def chooser(ctx):
                        return (ctx.maxStringLength * 2) < 0x10
                else:
                    isWide = False
                    def chooser(ctx):
                        return ctx.maxStringLength < 0x10
                return (
                        name,
                        base,
                        STRUCT,
                        [[
                            SHAPE('stringLength', (0x10, None), SIZE_T()),
                            SHAPE('maxStringLength', 0, SIZE_T()),
                            SHAPE('data', (0, None),
                                SWITCH(
                                chooser,
                                {
                                    True: [
                                        SHAPE('string', 0, STRUCT([
                                            SHAPE('string', 0, STRING(isUnicode=isWide, maxSize=0x10, isPrintable=False, size='_parent._parent.stringLength'))])) ],
                                    False: [
                                        SHAPE('string', 0, POINTER_TO_STRUCT([
                                                SHAPE('string', 0, STRING(isUnicode=isWide, isPrintable=False, size='_parent._parent.stringLength'))])),
                                        SHAPE('dummy', 0, ANYTHING(size=8))]}), fromStart=True)
                        ]], {'desc':dataTypeName})
            elif dataTypeName.startswith('std::unique_ptr'):
                struct = self._getUniquePtr(dataType, maxDepth-1)
                if 'std::default_delete' in dataTypeName:
                    return (
                            name,
                            base,
                            POINTER_TO_STRUCT,
                            [struct],
                            {   'isNullValid':True,
                                'desc':dataTypeName })
                else:
                    return (
                            name,
                            base,
                            STRUCT,
                            [[
                                SHAPE('deleter' + name, 0, POINTER(isNullValid=True)),
                                SHAPE(name, 0, POINTER_TO_STRUCT(struct, isNullValid=True))]],
                            { 'desc':dataTypeName })

            elif dataTypeName.startswith('std::shared_ptr'):
                baseType = self._getAllChildren(dataType, SymTagEnum['SymTagBaseClass'])
                if 1 != len(baseType):
                    raise Exception("Failed to parse shared_ptr")
                baseType = baseType[0]
                struct = self._getUniquePtr(baseType, maxDepth-1)
                return (
                        name,
                        base,
                        STRUCT,
                        [[
                            SHAPE('ptr', 0, POINTER_TO_STRUCT(struct, isNullValid=True)),
                            SHAPE('rep', 0, POINTER(isNullValid=True))]],
                        { 'desc':dataTypeName })
            elif dataTypeName.startswith('std::function'):
                return (name, base, ARRAY, [10, SIZE_T, [], {}], {'desc':dataTypeName})
            elif    dataTypeName.startswith('std::map') or \
                    dataTypeName.startswith('std::multimap') or \
                    dataTypeName.startswith('std::set') or \
                    dataTypeName.startswith('std::multiset'):

                baseType = self._getAllChildren(dataType, SymTagEnum['SymTagBaseClass'])
                if 1 != len(baseType):
                    raise Exception("Failed to parse shared_ptr")
                baseType = baseType[0]
                struct = self._getMapType(baseType, maxDepth-1)

                def parseNode(patFinder, startAddress, context):
                    isNil = patFinder.readUInt8(startAddress + (patFinder.getPointerSize() * 3) + 1)
                    if isNil:
                        return [SHAPE('duummy', 0, ANYTHING())]
                    return [
                        SHAPE('left', 0, POINTER_TO_STRUCT(parseNode)),
                        SHAPE('parent', 0, POINTER()),
                        SHAPE('right', 0, POINTER_TO_STRUCT(parseNode)),
                        SHAPE('dummy', 0, SIZE_T()),
                        SHAPE('data', 0, STRUCT(struct))]

                return (
                        name,
                        base,
                        STRUCT,
                        [[
                            SHAPE('tree', 0, POINTER_TO_STRUCT([
                                SHAPE('left', 0, POINTER()),
                                SHAPE('anchor', 0, POINTER_TO_STRUCT(parseNode)),
                                SHAPE('right', 0, POINTER()),
                                SHAPE('color', 0, BYTE()),
                                SHAPE('isNil', 0, BYTE(1))])),
                            SHAPE('treeSize', 0, SIZE_T())]],
                        { 'desc':dataTypeName })

            elif dataTypeName.startswith('std::vector') and 'bool' not in dataTypeName:
                structSize, struct = self._getVectorTypeAndSize(dataType, maxDepth-1)
                def arraySizeProc(ctx):
                    return (ctx._parent.last - ctx._parent.first) // structSize
                return (
                        name,
                        base,
                        STRUCT,
                        [[
                            SHAPE('first', 0, POINTER(isNullValid=True)),
                            SHAPE('last', 0, POINTER(isNullValid=True)),
                            SHAPE('end', 0, POINTER(isNullValid=True)),
                            SHAPE('data', 0, POINTER_TO_STRUCT([SHAPE('items', 0, ARRAY(
                                arraySizeProc, STRUCT, [struct]))], isNullValid=True), fromStart=True)]],
                        { 'desc':dataTypeName } )
            elif dataTypeName.startswith('nonstd::optional'):
                structSize, struct = self._getOptionalTypeAndSize(dataType, maxDepth-1)
                if 1 == structSize:
                    alignment = 0
                elif structSize in [1,2,4,8]:
                    alignment = structSize
                else:
                    alignment = None
                def chooser(ctx):
                    return 0 != (ctx.has_value_ & 0xff)
                if alignment:
                    return (
                            name,
                            base,
                            STRUCT,
                            [[
                                SHAPE('has_value_', 0, BYTE()),
                                SHAPE('contained', (0, 0, alignment),
                                    SWITCH(
                                        chooser,
                                        {
                                            True: struct,
                                            False: [] }))]],
                            { 'desc':dataTypeName })
                else:
                    return (
                            name,
                            base,
                            STRUCT,
                            [[
                                SHAPE('has_value_', 0, SIZE_T()),
                                SHAPE('contained', 0,
                                    SWITCH(
                                        chooser,
                                        {
                                            True: struct,
                                            False: [] }))]],
                            { 'desc':dataTypeName })

            else:
                content = self._getAllMembers(dataType.findChildren(0, None, 0), base=0, maxDepth=maxDepth)
                if not content:
                    return ( name, base, ANYTHING, [], {'desc':dataTypeName})
                return ( name, base, STRUCT, [content], {'desc':dataTypeName})
        elif 'SymTagPointerType' == memberTypeSymTag:
            content = self._getAllMembers(dataType.findChildren(0, None, 0), base=0, maxDepth=maxDepth-1)
            if not content:
                return ( name, base, POINTER, [], {'isNullValid':True, 'desc':dataTypeName} )
            return (
                        name,
                        base,
                        POINTER_TO_STRUCT,
                        [content],
                        {'isNullValid':True, 'desc':dataTypeName} )
        elif memberTypeSymTag in ['SymTagBaseType', 'SymTagEnum']:
            if dataType.baseType in [7, 1, 5, 10, 12, 14, 20, 21, 22, 23, 24, 31]:
                dataInfo = {'isSigned':False}
            elif dataType.baseType in [6, 2, 3, 4, 11, 13, 15, 16, 17, 18, 19]:
                dataInfo = {'isSigned':True, 'desc':dataTypeName}
            elif 8 == dataType.baseType:
                if 8 == dataType.length:
                    return (name, base, DOUBLE, [], {'desc':dataTypeName})
                elif 4 == dataType.length:
                    return (name, base, FLOAT, [], {'desc':dataTypeName})
                else:
                    raise Exception("Invlaid size for float %d" % dataType.length)
            else:
                raise Exception("Unknown data type %d" % dataType.baseType)
            if 'SymTagEnum' == memberTypeSymTag:
                enumChildrenItems = self._getAllChildren(dataType)
                values = {x.value : x.name for x in enumChildrenItems}
                dataInfo['value'] = values
            dataInfo['size'] = dataType.length
            dataInfo['desc'] = dataTypeName
            return (name, base, NUMBER, [], dataInfo)
        elif 'SymTagArrayType' == memberTypeSymTag:
            arrayCount = dataType.count
            arrayName, _, arrayType, arrayTypeArgs, arrayTypeKw = self._getSymTagDataType(dataType.type, 'A', 0, maxDepth)
            return (name, base, ARRAY, [arrayCount, arrayType, arrayTypeArgs, arrayTypeKw], {'desc':arrayName})
        else:
            raise Exception("Unknown ember type %s" % memberTypeSymTag)

    def _getUniquePtr(self, dataType, maxDepth):
        return self._getSubType(dataType, 'element_type', maxDepth)[1]

    def _getMapType(self, dataType, maxDepth):
        return self._getSubType(dataType, 'value_type', maxDepth)[1]

    def _getVectorTypeAndSize(self, dataType, maxDepth):
        return self._getSubType(dataType, 'value_type', maxDepth)

    def _getOptionalTypeAndSize(self, dataType, maxDepth):
        return self._getSubType(dataType, 'value_type', maxDepth)

    def _getSubType(self, dataType, itemName, maxDepth):
        baseType = dataType.findChildren(SymTagEnum['SymTagTypedef'], itemName, 1)
        if baseType.count != 1:
            raise Exception("Failed to parse %s" % itemName)
        baseType = baseType.Item(0)
        typeSize = baseType.length
        return (typeSize, self._getSymTagDataTypeAsShape(baseType.type, 'val', base=0, maxDepth=maxDepth-1))

def parseSymbolsDump( symbols_dump ):
    result = []
    f = open(symbols_dump, 'r')
    for l in f.readlines():
        address_pos = l.find('Address: ')
        name_pos = l.find('Name: ')
        if -1 == address_pos or -1 == name_pos:
            continue
        address_pos += len('Address: ')
        name_pos += len('Name: ')
        result.append( (l[name_pos:l.find('\n')], int(l[address_pos:address_pos + l[address_pos:].find(' ')], 16)) )
    f.close()
    return result

def solveAddr( addr, symbols, base=0 ):
    for sym in symbols:
        if sym[1]+base == addr:
            return( sym[0] )
    return None
