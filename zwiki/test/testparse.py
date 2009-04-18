import unittest
import os
import difflib              as diff
from   random               import choice, randint, shuffle

from   nose.tools           import assert_equal

from   zwiki.zwlexer        import ZWLexer
from   zwiki.zwparser       import ZWParser
from   zwiki.test.testlib   import ZWMARKUP, ZWMARKUP_RE, UNICODE, \
                                   gen_psep, gen_ordmark, gen_unordmark, \
                                   gen_headtext, gen_texts, gen_row, \
                                   gen_wordlist, gen_words, gen_linkwords, gen_links,\
                                   gen_macrowords, gen_macros, gen_xwikinames

stdfiles_dir    = os.path.join( os.path.split( __file__ )[0], 'stdfiles' )
rndfiles_dir    = os.path.join( os.path.split( __file__ )[0], 'rndfiles' )
samplefiles_dir = os.path.join( os.path.split( __file__ )[0], 'samplefiles' )
zwparser        = None
words           = None
links           = None
macros          = None
xwikinames      = None


def setUpModule() :
    global zwparser, words, links, macros, xwikinames
    print "Initialising the parser ..."
    zwparser     = ZWParser( lex_optimize=True, yacc_debug=True,
                           yacc_optimize=False )
    print "Initialising wiki ..."
    wordlist     = gen_wordlist( maxlen=20, count=200 )
    words        = gen_words( wordlist, count=200, huri_c=10, wuri_c=10 )
    print "Initialising links ..."
    linkwords    = gen_linkwords( maxlen=50, count=200 )
    links        = gen_links( linkwords, 100 )
    print "Initialising macros ..."
    macrowords   = gen_macrowords( maxlen=50, count=200 )
    macros       = gen_macros( macrowords, 100 )
    print "Initialising wiki extension names ..."
    xwikinames   = gen_xwikinames( 100 )
    
def tearDownModule() :
    pass

class TestDumpsValid( object ) :
    """Test cases to validate ZWiki parser."""

    def _test_execute( self, type, testcontent, count ) :
        testcontent = zwparser.preprocess( testcontent )
        try :
            tu      = zwparser.parse( testcontent, debuglevel=0 )
            result  = tu.dump()[:-1]
        except :
            tu     = zwparser.parse( testcontent, debuglevel=2 )
            result = tu.dump()[:-1]
        if result != testcontent :
            print ''.join(diff.ndiff( result.splitlines(1), testcontent.splitlines(1) ))
        assert result == testcontent, type+'... testcount %s'%count

    def test_1_heading( self ) :
        """Testing heading markup"""
        print "Testing heading markup"
        headmarkup= [ '=' , '==', '===', '====', '=====' ]
        testlist  = [ choice(headmarkup) + gen_headtext( words ) +
                      choice( headmarkup + [ '' ] ) + gen_psep(3)
                        for i in range(50) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'heading', t, testcount
            testcount += 1

    def test_2_hrule( self ) :
        """Testing horizontal rule markup"""
        print "\nTesting horizontal rule markup"
        self._test_execute( 'horizontalrule', '----', 1 )

    def test_3_option( self ) :
        """Testing pragmas - options"""
        print "\nTesting pragmas - options"
        options  = ''.join([ choice(words) + '=' + choice(words) + ' '
                             for i in range(10) ])
        testlist = [ '@options' + options + gen_psep(randint(0,3))
                     for i in range(100) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'pragma-options', t, testcount
            testcount += 1

    def test_4_tag( self ) :
        """Testing pragmas - tags"""
        print "\nTesting pragmas - tags"
        tags      = ''.join([ choice(words) +', ' for i in range(10) ])
        testlist  = [ '@tags' + tags + gen_psep(randint(0,3))
                      for i in range(100) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'pragma-tags', t, testcount
            testcount += 1

    def test_5_wikix( self ) :
        """Testing wiki extension markup""" 
        print "\nTesting wiki extension markup"
        wikix_cont = '\n'.join([ choice(words) for i in range(randint(1,20)) ])
        testlist   = [ '{{{' + choice(xwikinames) + '\n' + wikix_cont + \
                       '\n}}}\n' + gen_psep(randint(0,3))
                       for i in range(1000) ]
        testcount  = 1
        for t in testlist :
            yield self._test_execute, 'wikix', t, testcount
            testcount += 1

    def test_6_escapenewline( self ) :
        """Testing wiki text containing `~~\\n`"""
        print "\nTesting wiki text containing `~~\\n`"
        testlist = [ 'hello ~~\nworld' ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'escapenewline', t, testcount
            testcount += 1

    def test_7_lastcharesc( self ) :
        """Testing wiki text with last char as `~`"""
        print "\nTesting wiki text with last char as `~`"
        testlist = [ 'hello world~' ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'lastcharesc', t, testcount
            testcount += 1

    def test_8_textlines( self ) :
        """Testing textlines"""
        print "\nTesting textlines"
        testlist  = [ '\n'.join([ gen_texts(
                                    words, links, macros,
                                    tc=5, pc=1, ec=2, lc=1, mc=1, fc=1,
                                    nopipe=True
                                  )
                                  for j in range(randint(0,10)) ]) +
                      gen_psep(randint(0,3)) for i in range(100) ]  +\
                    [ '\n'.join([ gen_texts(
                                    words, links, macros,
                                    tc=5, pc=1, ec=2, lc=1, mc=1, fc=0,
                                    nopipe=True
                                  )
                                  for j in range(randint(0,10)) ]) +
                      choice(ZWMARKUP) + ' ' +
                      '\n'.join([ gen_texts(
                                    words, links, macros,
                                    tc=5, pc=1, ec=2, lc=1, mc=1, fc=0,
                                    nopipe=True
                                  )
                                  for j in range(randint(0,10)) ]) +
                      choice(ZWMARKUP) + ' ' 
                      '\n'.join([ gen_texts(
                                    words, links, macros,
                                    tc=5, pc=1, ec=2, lc=1, mc=1, fc=0,
                                    nopipe=True
                                  )
                                  for j in range(randint(0,10)) ])
                      for i in range(10) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'textlines', t, testcount
            testcount += 1

    def test_9_table( self ) :
        """Testing tables"""
        print "\nTesting tables"
        testlist  = [ '\n'.join([ gen_row( words, links, macros )
                                  for j in range(randint(0,10)) ]) +
                      gen_psep(randint(0,3)) for i in range(100) ] 
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'table', t, testcount
            testcount += 1

    def test_A_ordlists( self ) :
        """\nTesting ordered list"""
        print "\nTesting ordered list"
        testlist  = [ '\n'.join([ gen_ordmark() + \
                                  gen_texts(
                                    words, links, macros,
                                    tc=5, pc=1, ec=2, lc=1, mc=1, fc=1,
                                    nopipe=True
                                  )
                                  for j in range(randint(0,10)) ]) +
                      gen_psep(randint(0,3)) for i in range(100) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'ordlists', t, testcount
            testcount += 1

    def test_B_unordlists( self ) :
        """Testing unordered list"""
        print "\nTesting unordered list"
        testlist  = [ '\n'.join([ gen_unordmark() + \
                                  gen_texts(
                                    words, links, macros,
                                    tc=5, pc=1, ec=2, lc=1, mc=1, fc=1,
                                    nopipe=True
                                  )
                                  for j in range(randint(0,10)) ]) +
                      gen_psep(randint(0,3)) for i in range(100) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'unordlists', t, testcount
            testcount += 1

    def test_C_unicode( self ) :
        """Testing unicoded test"""
        print "\nTesting unicoded text"
        testlist = [ '' ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'unordlists', t, testcount
            testcount += 1
