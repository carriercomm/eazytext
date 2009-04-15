#! /usr/bin/env python

import unittest
import os
import difflib        as diff
from   random         import choice, randint, shuffle
import re
from   optparse       import OptionParser

from   zwiki.zwlexer  import ZWLexer
from   zwiki.zwparser import ZWParser

basedir      = os.path.split( os.path.abspath(__file__) )[0]
testdir      = os.path.join( basedir, 'test' )
stdfiles     = os.path.join( testdir, 'stdfiles' )
get_stdfiles = lambda : [ os.path.join( stdfiles, f )
                            for f in os.listdir( stdfiles ) ]

def _option_parse() :
    '''Parse the options and check whether the semantics are correct.'''
    parser  = OptionParser(usage="usage: %prog [options] cmd")
    options, args   = parser.parse_args()

    not args and parser.print_help()

    return options, args

def main() :
    options, args = _option_parse()
    if args[0] == 'teststd' :
        zwparser = ZWParser( lex_optimize=True, yacc_debug=True, yacc_optimize=False )
        stdfiles = get_stdfiles()
        for f in stdfiles :
            if os.path.splitext(f)[1] not in [ '.txt', '.wiki' ] :
                continue
            wikitext = open( f ).read()
            tu       = zwparser.parse( wikitext, debuglevel=0 )
            html     = tu.tohtml()
            open( os.path.splitext( f )[0] + '.html', 'w' ).write( html )

if __name__ == '__main__' :
    main()
