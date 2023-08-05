
from struct import pack, unpack
from ..MemReaderBase import *
from ..GUIDisplayBase import *
from math import ceil
from .Finder import *

PDB2_SIGNATURE = "Microsoft C/C++ program database 2.00\r\n\032JG\0\0"
PDB7_SIGNATURE = "Microsoft C/C++ MSF 7.00\r\n\x1ADS\0\0\0"

PDB7_PATTERN = [
        SHAPE("signature",      0,  n_string(fixedValue=PDB7_SIGNATURE)),
        SHAPE("pageSize",       0,  n_uint32()),
        ASSERT(lambda reader,ctx:0==(ctx.pageSize&0xff)),
        SHAPE("allocTablePtr",  0,  n_uint32()),
        SHAPE("numFilePages",   0,  n_uint32()),
        SHAPE("rootSize",       0,  n_uint32()),
        SHAPE("reserved",       0,  n_uint32()),
        SHAPE("rootIndex",      0,  n_uint32()),
        ASSIGN("numRootPages",  lambda reader,ctx:int(ceil(float(ctx.rootSize)/ctx.pageSize))),
        SHAPE("root", lambda ctx,addr:(addr + ctx.rootIndex*ctx.pageSize, ctx.rootIndex*ctx.pageSize),
                n_array("numRootPages", n_uint32, []))]

class StreamReader(MemReaderBase, GUIDisplayBase):
    def __init__(self, fileReader, pages, pageSize, length=None):
        self.fileReader = fileReader
        self.pages = pages
        self.pageSize = pageSize
        if None == length:
            self.length = len(pages) * pageSize
        else:
            self.length = length
        self._ENDIANITY = self.fileReader.getEndianity()
        MemReaderBase.__init__(self)

    def virtualAddrToPhy(self, addr):
        page = addr // self.pageSize
        return self.pages[page] * self.pageSize + (addr % self.pageSize)

    def __len__(self):
        return self.length

    def readAddr( self, addr ):
        if 4 == self._POINTER_SIZE:
            return unpack(self._ENDIANITY + 'L', self.readMemory(addr, 4))
        elif 8 == self._POINTER_SIZE:
            return unpack(self._ENDIANITY + 'Q', self.readMemory(addr, 8))
        else:
            raise Exception("Unknown pointer size")

    def readUInt64( self, addr ):
        return unpack(self._ENDIANITY + 'Q', self.readMemory(addr, 8))[0]
    def readUInt32( self, addr ):
        return unpack(self._ENDIANITY + 'L', self.readMemory(addr, 4))[0]
    def readUInt16( self, addr ):
        return unpack(self._ENDIANITY + 'H', self.readMemory(addr, 2))[0]
    def readUInt8( self, addr ):
        return self.fileReader.readUInt8(self.virtualAddrToPhy(addr))

    def readMemory( self, addr, length ):
        bytesLeft = length
        result = ''
        pageSize = self.pageSize
        while 0 != bytesLeft:
            phy = self.virtualAddrToPhy(addr)
            bytesLeftInPage = pageSize - (phy % pageSize)
            if bytesLeftInPage >= bytesLeft:
                result += self.fileReader.readMemory(phy, bytesLeft)
                bytesLeft = 0
            else:
                result += self.fileReader.readMemory(phy, bytesLeftInPage)
                bytesLeft   -= bytesLeftInPage
                addr        += bytesLeftInPage
        return result

    def readString( self, addr, maxSize=None, isUnicode=False ):
        result = ''
        bytesCounter = 0

        while True:
            if False == isUnicode:
                char = self.readUInt8(addr)
                bytesCounter += 1
            else:
                char = self.readUInt16(addr)
                bytesCounter += 2
            if 1 < char and char < 0x80:
                result += chr(char)
            else:
                return result
            if None != maxSize and bytesCounter > maxSize:
                return result

    def isAddressValid( self, addr ):
        return (addr >= 0) and (addr < len(self))

    def getDefaultDataSize(self):
        return self.fileReader.getDefaultDataSize()
    def getEndianity(self):
        return self.fileReader.getEndianity()
    def getPointerSize(self):
        return self.fileReader.getPointerSize()
    def getPageSize(self):
        return self.pageSize

def getRootStream(fileReader):
    patFinder = PatternFinder(fileReader)
    header = next(patFinder.search(PDB7_PATTERN, 0))
    return StreamReader(fileReader, [x.Item for x in header.root], header.pageSize)

PDB_ROOT_STREAM_PATTERN = [
        SHAPE("numStreams",     0,  n_uint32()),
        SHAPE("streamSizes",    0,
            n_array("numStreams", n_uint32, [])) ]

def getStreams(rootStream):
    numStreams = rootStream.readUInt32(0)
    pos = 4
    streamsSizes = []
    for i in range(numStreams):
        streamsSizes.append(rootStream.readUInt32(pos))
        pos += 4
    streams = []
    pageSize = rootStream.getPageSize()
    for streamSize in streamsSizes:
        if 0xffffffff == streamSize:
            streams.append(None)
            continue
        pages = []
        numPages = int(ceil(float(streamSize) / pageSize))
        for i in range(numPages):
            pages.append(rootStream.readUInt32(pos))
            pos += 4
        streams.append(StreamReader(rootStream.fileReader, pages, pageSize, streamSize))
    return streams

def getPdbStream(rootStream):
    return getStreams(rootStream)[0]

def getTypesStream(rootStream):
    return getStreams(rootStream)[1]

def getDebugStream(rootStream):
    return getStreams(rootStream)[2]

OFF_CB_PATTERN = [
        SHAPE("off",    0,  c_uint32()),
        SHAPE("cb",     0,  c_uint32()) ]
TYPE_PATTERN = [
        SHAPE("length",     0,  c_uint16()),
        SHAPE("typeData",   0,  n_string(size="length")),
        SHAPE("data",       0,  n_switch("typeData", {
            "LF_ARGLIST"    : LF_ARGLIST_PATTERN,
            "LF_ARRAY"      : LF_ARRAY_PATTERN,
            "LF_ARRAY_ST"   : LF_ARRAYST_PATTERN,
            "LF_BITFIELD"   : LF_BITFIELD_PATTERN,
            "LF_CLASS"      : LF_CLASS_PATTERN,
            "LF_ENUM"       : LF_ENUM_PATTERN,
            "LF_FIELDLIST"  : LF_FIELDLIST_PATTERN,
            "LF_MFUNCTION"  : LF_MFUNC_PATTERN,
            "LF_MODIFIER"   : LF_MODIFIER_PATTERN,
            "LF_POINTER"    : LF_POINTER_PATTERN,
            "LF_PROCEDURE"  : LF_PROCEDURE_PATTERN,
            "LF_STRUCTURE"  : LF_STRUCTURE_PATTERN,
            "LF_STRUCTURE_ST": LF_STRUCTUREST_PATTERN,
            "LF_UNION"      : LF_UNION_PATTERN,
            "LF_UNION_ST"   : LF_UNIONST_PATTERN,
            "LF_VTSHAPE"    : LF_VTSHAPE_PATTERN }))]

PDB_TYPES_STREAM_PATTERN = [
        SHAPE("version",        0,  c_uint32()),
        SHAPE("headerSize",     0,  c_uint32()),
        SHAPE("tiMin",          0,  c_uint32()),
        SHAPE("tiMax",          0,  c_uint32()),
        SHAPE("followSize",     0,  c_uint32()),
        SHAPE("sn",             0,  c_uint16()),
        SHAPE("padding",        0,  c_uint16()),
        SHAPE("hashKey",        0,  c_uint32()),
        SHAPE("buckets",        0,  c_uint32()),
        SHAPE("hashVals",       0,  n_struct(OFF_CB_PATTERN)),
        SHAPE("tiOff",          0,  n_struct(OFF_CB_PATTERN)),
        SHAPE("hashAdj",        0,  n_struct(OFF_CB_PATTERN)),
        SHAPE("types",          0,
            n_array(lambda ctx:ctx.tiMax-ctx.tiMin, n_struct, [TYPE_PATTERN]))]

