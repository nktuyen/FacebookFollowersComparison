import os
import sys
import optparse

if __name__=="__main__":
    parser: optparse.OptionParser = optparse.OptionParser('%prog [options] url1 url2')
    parser.add_option('-v', '--verbose', action='store_false', help='Verbose')
    
    opts, args = parser.parse_args()
    print(args, opts)