# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

import logging, unittest, os, random
import difflib            as diff
from   random             import choice, randint, shuffle
from   os.path            import dirname, basename, join
from   os                 import listdir

from   nose.tools         import assert_equal

import eazytext
from   eazytext              import wiki_properties
from   eazytext.parser       import ETParser
from   eazytext.test.testlib import genseed

log      = logging.getLogger(__name__)
seed     = None
testdir  = basename( dirname( __file__ ))
testfile = basename( __file__ )
docdir   = join( dirname( dirname( dirname( __file__ ))), 'docs' )
docfiles = [ 'CHANGELOG', 'eazytext.etx', 'LICENSE', 'primer.etx',
             'ROADMAP', 'styleshortcuts.etx', 'gettingstarted.etx',
             'plugins.etx', 'README', 'skins.etx' ]
docfiles = [ join(docdir, f) for f in docfiles ]
             

def _loginfo( info ) :
    log.info( info )
    print info

def setUpModule() :
    global words, links, macros, htmls, seed

    seed    = genseed()
    random.seed( seed )
    
def tearDownModule() :
    pass

class TestWikiDumpsRandom( object ) :
    """Test cases to validate eazytext random"""

    def _test_execute( self, type, testcontent, count, ref=''  ) :
        # Initialising the parser
        etparser     = ETParser( lex_optimize=True, yacc_optimize=False )
        # The first character is forced to be a `A` to avoid having `@` as the
        # first character
        testcontent = 'A' + testcontent
        # Prepare the reference.
        ref        = ref or testcontent
        ref        = etparser._wiki_preprocess( ref )
        props, ref = wiki_properties( ref )

        # Characterize the generated testcontent set the wikiproperties
        wikiprops   = {}
        testcontent = ( "@ %s " % wikiprops ) + '\n' + testcontent
        
        # Test by comparing the dumps
        try :
            tu      = etparser.parse( testcontent, debuglevel=0 )
            result  = tu.dump()[:-1]
        except :
            # open( 'testcontent', 'w' ).write( testcontent )
            tu     = etparser.parse( testcontent, debuglevel=2 )
            result = tu.dump()[:-1]
        if result != ref :
            # open( 'result', 'w' ).write( result )
            # open( 'ref', 'w' ).write( ref )
            print ''.join(diff.ndiff( result.splitlines(1), ref.splitlines(1) ))
        assert result == ref, type+'... testcount %s'%count

    def test_0_file( self ) :
        """If file `ref` is available pick it and test it"""
        testlist  = []
        ref       = os.path.isfile( 'ref' ) and open( 'ref' ).read()
        ref and testlist.append( ref )
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'ref', t, testcount
            testcount += 1

    def test_1_docs( self ) :
        """Testing eazytext documents"""
        print "\nTesting eazytext documents"
        log.info( "Testing eazytext documents" )
        testcount = 1
        for f in docfiles :
            cont = open(f).read()
            yield self._test_execute, 'ezdocs', cont, testcount
            testcount += 1
