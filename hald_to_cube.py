import math
import sys
from optparse import OptionParser

from PIL import Image

def main():

    opt_parser = OptionParser(usage='%prog [options] input.[png|tif]')
    opts, args = opt_parser.parse_args()

    if len(args) != 1:
        opt_parser.print_usage()
        exit(1)

    inimage = args[0]
    name = inimage.split(".")[0]
    outcube = f"{name}.cube"
    
    in_ = Image.open(inimage)
    w, h = in_.size
    if not w == h:
        print('HALD input is not square.', file=sys.stderr)
        exit(2)
    
    steps = int(round(math.pow(w, 1/3)))
    if not steps ** 3 == w:
        print(f'HALD input size is invalid: {w} is not a cube.', file=sys.stderr)

    print(f'{steps} steps -> {steps**6} values', file=sys.stderr)
    
    # Assume that we are going from 8 bits to 10.
    out = open(outcube, 'w')
    out.write('#Created by: hald_to_cube.py\n')
    #out.write('#Copyright: Copyright 2012 Adobe Systems Inc.\n')
    out.write(f'TITLE "{args[0]}"\n')
    out.write('\n')
    #out.write('#LUT size\n')
    out.write(f'LUT_3D_SIZE {steps ** 2}\n')
    out.write('\n')
    #out.write('#data domain\n')
    out.write('DOMAIN_MIN 0.0 0.0 0.0\n')
    out.write('DOMAIN_MAX 1.0 1.0 1.0\n')

    if False:
        steps1 = steps + 1
        steps3 = steps ** 2 * (steps + 1)
        steps5 = steps ** 4 * (steps + 1)
        data = list(in_.getdata())
        def lookup(ri, gi, bi):
            return data[
                ri * steps1 + gi * steps3 + bi * steps5
            ]
        for bi in range(steps):
            for gi in range(steps):
                for ri in range(steps):
                    r, g, b = lookup(ri, gi, bi)[:3]
                    out.write('%f %f %f\n' % (r / 255.0, g / 255.0, b / 255.0))
    else:
        for pixel in list(in_.getdata()):
            try:
                r, g, b = pixel[:3]
                out.write('%f %f %f\n' % (r / 255.0, g / 255.0, b / 255.0))
            except TypeError:
                bw = pixel
                out.write('%f %f %f\n' % (bw / 255.0, bw / 255.0, bw / 255.0))


if __name__ == '__main__':
    main()
