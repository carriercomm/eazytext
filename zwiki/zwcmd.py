#! /usr/bin/env python

"""Module to execute the zwiki from command line"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import unittest
import os
import difflib        as diff
from   random         import choice, randint, shuffle
import re
from   optparse       import OptionParser

from   zwiki.zwparser import ZWParser

basedir      = os.path.split( os.path.abspath(__file__) )[0]
testdir      = os.path.join( basedir, 'test' )
stdfiles     = os.path.join( testdir, 'stdfiles' )
get_stdfiles = lambda : [ os.path.join( stdfiles, f )
                            for f in os.listdir( stdfiles ) ]

DTD = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
"""

def _option_parse() :
    '''Parse the options and check whether the semantics are correct.'''
    parser  = OptionParser(usage="usage: %prog [options] cmd")
    options, args   = parser.parse_args()

    not args and parser.print_help()

    return options, args

def main() :
    options, args = _option_parse()
    # Bug in PLY ???
    #   Enabling optimize screws up the order of regex match (while lexing)
    # zwparser = ZWParser( yacc_debug=True )
    zwparser = ZWParser()
    if args[0] == 'teststd' :
        stdfiles = get_stdfiles()
        for f in stdfiles :
            if os.path.splitext(f)[1] not in [ '.txt', '.wiki' ] :
                continue
            wikitext = open( f ).read()
            tu       = zwparser.parse( wikitext, debuglevel=0 )
            html     = tu.tohtml()
            open( os.path.splitext( f )[0] + '.html', 'w' ).write( html )
    else :
        file     = args[0]
        wikitext = open( file ).read()
        tu       = zwparser.parse( wikitext, debuglevel=0 )
        html     = DTD + '<html><body>' + tu.tohtml() + '</body></html>'
        open( os.path.splitext( file )[0] + '.html', 'w' ).write( html )
        # print tu.dump()

if __name__ == '__main__' :
    main()
