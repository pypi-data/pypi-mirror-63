#Copyright © 2020 Noel Kaczmarek
import json


FILE_HEADER_SIZE = 64


class Shard:
    def __init__(self, file):
        self.file = file

    def create(self, index, size, offset, data):
        self.index = index
        self.size = size
        self.offset = offset
        self.data = data
        self.header = self.generateHeader()

    def read(self):
        with open(self.file, 'rb') as f:
            f.seek(FILE_HEADER_SIZE, 0)
            content = f.read(FILE_HEADER_SIZE + self.size)
            f.close()

        return content

    def write(self, **kwargs):
        with open(self.file, 'wb') as f:
            f.seek(0, 0)

            if kwargs.get('write_header', True):
                f.write(self.header)
            f.seek(FILE_HEADER_SIZE, 0)
            f.write(self.data)
            f.close()
    
    def readHeader(self):
        with open(self.file, 'rb') as f:
            self.header = f.read(FILE_HEADER_SIZE)
            f.close()

        header = self.header.decode().split('}')[0] + '}'
        header = json.loads(header)
        self.index = header['index']
        self.size = header['size']
        self.offset = header['offset']

    def generateHeader(self):
        return json.dumps({'index': self.index, 'size': self.size, 'offset': self.offset}).encode('utf-8')