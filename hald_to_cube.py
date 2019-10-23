import sys
import math
from optparse import OptionParser

from PIL import Image

from pprint import pprint


class Pixel():
    pass

class Array3D():
    
    def __init__(self, size):
        self.size = size
        self.entries = self.size**3
        self.color = None
        self.x = [[[None for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]
        self.reset()

    def append(self, y):
        self.x[self.i][self.j][self.k] = y
        if None == self.color:
            if isinstance(y, int):
                self.color = False
            else:
                self.color = True
        self.increment()    
    
    def increment(self):
        if (self.size-1) == self.k and (self.size-1) == self.j and (self.size-1) == self.i:
            self.reset()
        elif (self.size-1) == self.j and (self.size-1) == self.i:
            self.j = 0
            self.i = 0
            self.k += 1
        elif (self.size-1) == self.i:
            self.i = 0
            self.j += 1
        else:
            self.i += 1
    
    def reset(self):
        self.i = 0
        self.j = 0
        self.k = 0
    
    def pop(self):
        w = self.x[self.i][self.j][self.k]
        self.increment()
        return w
    
class Hald():

    def __init__(self, infile):
        self.filename = infile
        f = Image.open(self.filename)
        self.w, self.h = f.size
        print(self.w,self.h)
        
        if not self.w == self.h:
            raise Exception('HALD input is not square.')
        
        self.steps = int(round(math.pow(self.w, 1/3)))
        if not self.steps ** 3 == self.w:
            raise Exception(f'HALD input size is invalid: {self.w} is not a cube.')
            
        self.lut_size = self.steps ** 2
        self.data = list(f.getdata())
        
        self.p = Array3D(self.lut_size)
        for pixel in self.data:
            self.p.append(pixel)

        print(self.p.x[0][0])
    
    def writeCube(self):
        
        name = self.filename.split(".")[0]
        outcube = f"{name}.cube"
    
        print(f'{self.steps} steps -> {self.p.entries} values', file=sys.stderr)
    
        # Assume that we are going from 8 bits to 10.
        out = open(outcube, 'w')
        out.write('#Created by: hald_to_cube.py\n')
        #out.write('#Copyright: Copyright 2012 Adobe Systems Inc.\n')
        out.write(f'TITLE "{self.filename}"\n')
        out.write('\n')
        #out.write('#LUT size\n')
        out.write(f'LUT_3D_SIZE {self.steps ** 2}\n')
        out.write('\n')
        #out.write('#data domain\n')
        out.write('DOMAIN_MIN 0.0 0.0 0.0\n')
        out.write('DOMAIN_MAX 1.0 1.0 1.0\n')

        for i in range(self.p.entries):
            pixel = self.p.pop()
            if self.p.color:
                r, g, b = pixel[:3]
            else:
                r = g = b = pixel
            #print(pixel)
            out.write(f'{r / 255.0} {g / 255.0} {b / 255.0}\n')
        
def main():

    opt_parser = OptionParser(usage='%prog [options] input.[png|tif]')
    opts, args = opt_parser.parse_args()

    if len(args) != 1:
        opt_parser.print_usage()
        exit(1)

    inimage = args[0]
    
    h = Hald(inimage)
    h.writeCube()

if __name__ == '__main__':
    main()
