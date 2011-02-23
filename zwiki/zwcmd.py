#! /usr/bin/env python

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Command line execution"""

# -*- coding: utf-8 -*-

# Gotcha : None
#   1. Bug in PLY ???
#   Enabling optimize screws up the order of regex match (while lexing)
#       zwparser = ZWParser( yacc_debug=True )
# Notes  : None
# Todo   : None

import unittest
import os
import difflib        as diff
from   random         import choice, randint, shuffle
import re
from   optparse       import OptionParser
from   os.path        import isfile

from   zwiki.zwparser import ZWParser
from   zwiki          import VERSION

def _option_parse() :
    '''Parse the options and check whether the semantics are correct.'''
    parser = OptionParser(usage="usage: %prog [options] filename")
    parser.add_option( '-o', '--outfile', dest='ofile', default=None,
                       help='Output html file to store translated result' )
    parser.add_option( '-d', action='store_true', dest='dump',
                       help='Dump translation' )
    parser.add_option( '-l', dest='debuglevel', default='0',
                       help='Debug level for PLY parser' )
    parser.add_option( '--version', action='store_true', dest='version',
                       help='Version information of the package' )

    options, args   = parser.parse_args()

    return options, args

def main() :
    options, args = _option_parse()
    zwparser = ZWParser( obfuscatemail=True )
    tu = None
    if options.version :
        print VERSION
    if args and isfile( args[0] ) :
        ifile = args[0]
        wikitext = open( ifile ).read()
        debuglevel = int(options.debuglevel)
        print "Parsing ...",
        tu = zwparser.parse( wikitext, debuglevel=debuglevel )
        print "Done"
    if tu and options.dump :
        print tu.dump()
    elif tu :
        ofile = options.ofile or (os.path.splitext(ifile)[0] + '.html')
        print "Translation ...",
        html = '<html><body>' + tu.tohtml() + '</body></html>'
        print "Done"
        open( ofile, 'w' ).write( html )

if __name__ == '__main__' :
    main()
