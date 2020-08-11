import PPMdata
import struct


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
        self.PPMnums = PPMdata.getNumsPPM()
        self.file = file
        self.data = None
        self.mode = 0
        self.type = ''
        self.width = 0
        self.height = 0
        self.OffBits = 0
        self.detektPPM()

    def __repr__(self):
        msg = (
            f'{self.__class__.__module__}.{self.__class__.__name__} '
            f'mode={self.mode} '
            f'size={self.width}x{self.height} '
            f'at 0x{id(self):X}'
        )
        return msg

    def detektPPM(self):
        '''
        Reading headers, set atr and verify it's the Px-type PPM
        '''
        self.readFile()
        self.readPPM()
        # 80 = 'P'
        if self.type[0] != 80:
            raise PPMdata.ImageTypeError()

    def readFile(self):
        with open(self.file, 'rb') as f:
            self.data = bytearray(f.read())

    def readPPM(self):
        self.type = struct.unpack_from('<2s', self.data, 0)[0]

        i = 2
        numParm = 0
        param = [b'']*3
        while True:
            i += 1
            if self.data[i] == 10 and numParm == 2:
                # complite
                break
            elif self.data[i] == 10 or self.data[i] == 32:
                # next param
                numParm += 1
                continue

            if self.data[3] > 47 and self.data[3] < 58:
                param[numParm] += struct.unpack_from('<c', self.data, i)[0]
            else:
                raise PPMdata.ImageReadError()

        self.OffBits = i + 1
        self.width = int(param[0])
        self.height = int(param[1])
        self.mode = int(param[2])
        self.BitMap = self.data[self.OffBits:]
        return i + 1

    def getPPM(self):
        Px = self.type
        Px += bytes(f'\n{self.width} {self.height}\n{self.mode}\n',
                    encoding='utf8')
        Px += self.BitMap
        return Px

    def addSymbol(self, image, X, Y, sybmol, alpha):
        BitMap = self.readBitMap(self.BMPnums[sybmol], 1, 9, 13)

        for line, _ in enumerate(BitMap):
            for colum, _ in enumerate(BitMap[line]):
                if BitMap[line][colum] != alpha:
                    image[line+Y][colum+X] = BitMap[line][colum]
