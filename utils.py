import BMPdata
import struct
import base64


def timeStr(duration_ms, colon=True):
    ''' Convert ms to 'MM:SS' or 'HH h MM min '''
    seconds = int(duration_ms / 1000)
    if colon:
        hours = int(int(seconds / 60) / 60)
        hoursSrt = ''
        if hours:
            hoursSrt = f'{hours:02}:'

        return f'{hoursSrt}{int(seconds / 60):02}:{int(seconds % 60):02}'

    else:
        minutes = int(seconds / 60)
        hours = int(minutes / 60)

        return f'{hours} h {int(minutes % 60)} min'


def delSpecCh(str):
    for ch in list('\\/:*?"<>|+%'):
        str = str.replace(ch, '')
    return ' '.join(str.split())


class Image:
    def __init__(self, file):
        self.BMPnums = BMPdata.getNumsBMP()
        self.file = file
        self.data = None
        self.mode = None
        self.detektImg()
        self.BitMapLines = self.readBitMap(self.data,
                                           self.tagBITMAPFILEHEADER.bfOffBits,
                                           self.width, self.height)

    @property
    def width(self):
        return self.tagBITMAPINFOHEADER.biWidth

    @property
    def height(self):
        return self.tagBITMAPINFOHEADER.biHeight

    def __repr__(self):
        msg = (
            f'{self.__class__.__module__}.{self.__class__.__name__} '
            f'mode={self.mode} '
            f'size={self.width}x{self.height} '
            f'at 0x{id(self):X}'
        )
        return msg

    def detektImg(self):
        '''
        Reading headers, set atr and verify it's the BMP-type
        '''
        self.readFile()
        self.readBMPHeaders()
        self.mode = 'RGB'
        if self.tagBITMAPFILEHEADER.bfType != b'BM':
            raise BMPdata.ImageTypeError()

    def readFile(self):
        with open(self.file, 'rb') as f:
            self.data = bytearray(f.read())

    def readBitMap(self, data, bfOffBits, biWidth, biHeight):
        padBytes = (4 - (biWidth * 3) % 4) % 4
        BitMapLines = []
        startLine = bfOffBits
        endLine = startLine + biWidth * 3
        for line in range(biHeight):
            BitMapLine = []
            for count, indx in enumerate(range(startLine, endLine, 3)):
                BitMapLine.append(BMPdata.RGBQUAD._make(
                                  struct.unpack_from('<BBB', data, indx)))
            BitMapLines.append(BitMapLine)
            startLine += biWidth * 3 + padBytes
            endLine += biWidth * 3 + padBytes
        return BitMapLines

    def readBMPHeaders(self):
        self.tagBITMAPFILEHEADER = BMPdata.BITMAPFILEHEADER._make(
                                   struct.unpack_from('<2sIHHI',
                                                      self.data,
                                                      0)
                                )
        self.tagBITMAPINFOHEADER = BMPdata.BITMAPINFOHEADER._make(
                                   struct.unpack_from('<ILLHHIILLII',
                                                      self.data,
                                                      14)
                                )

    def buildImage(self, BitMapFileHeader, BitMapInfoHeader, BitMapLines):
        dataImg = bytearray()
        padBytes = (2 - (BitMapInfoHeader.biWidth * 3) % 2) % 2
        templ = ['2s'] + list('IHHI')
        for x, byte in enumerate(BitMapFileHeader):
            dataImg += struct.pack(f"<{templ[x]}", byte)

        templ = list('ILLHHIILLII')
        for x, byte in enumerate(BitMapInfoHeader):
            dataImg += struct.pack(f"<{templ[x]}", byte)

        for line in BitMapLines:
            for color in line:
                dataImg += struct.pack("<BBB",
                                       color.Blue,
                                       color.Green,
                                       color.Red)
            if padBytes:
                dataImg += struct.pack("<B", 0)
        return dataImg

    def getBase64(self):
        img = self.buildImage(self.tagBITMAPFILEHEADER,
                              self.tagBITMAPINFOHEADER,
                              self.BitMapLines)
        return base64.b64encode(img)

    def getPPM(self):
        pass

    def addSymbol(self, image, X, Y, sybmol, alpha):
        BitMap = self.readBitMap(self.BMPnums[sybmol], 1, 9, 13)

        for line, _ in enumerate(BitMap):
            for colum, _ in enumerate(BitMap[line]):
                if BitMap[line][colum] != alpha:
                    image[line+Y][colum+X] = BitMap[line][colum]
