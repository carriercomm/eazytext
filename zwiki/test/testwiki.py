import unittest
import os
import difflib            as diff
from   random             import choice, randint, shuffle

from   nose.tools         import assert_equal

from   zwiki.zwlexer      import ZWLexer
from   zwiki.zwparser     import ZWParser
from   zwiki.test.testlib import ZWMARKUP, ZWMARKUP_RE, \
                                 gen_psep, gen_ordmark, gen_unordmark, \
                                 gen_headtext, gen_texts, gen_row, \
                                 gen_wordlist, gen_words, gen_linkwords, gen_links,\
                                 gen_macrowords, gen_macros, \
                                 gen_htmlwords, gen_htmls, \
                                 random_textformat, random_listformat, \
                                 random_bqformat, \
                                 random_tableformat, random_wikitext, random_wiki


stdfiles_dir    = os.path.join( os.path.split( __file__ )[0], 'stdfiles' )
rndfiles_dir    = os.path.join( os.path.split( __file__ )[0], 'rndfiles' )
samplefiles_dir = os.path.join( os.path.split( __file__ )[0], 'samplefiles' )
zwparser        = None
words           = None
links           = None
macros          = None
htmls           = None

def setUpModule() :
    global zwparser, words, links, macros, htmls
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
    print "Initialising htmls ..."
    htmlwords    = gen_htmlwords( maxlen=50, count=200 )
    htmls        = gen_htmls( htmlwords, 100 )
    
def tearDownModule() :
    pass

class TestWikiDumpsRandom( object ) :
    """Test cases to validate ZWiki random"""

    def _test_execute( self, type, testcontent, count, ref=''  ) :
        # The first character is forced to be a `A` to avoid having `@` as the
        # first character
        testcontent = 'A' + testcontent
        # Prepare the reference.
        ref        = ref or testcontent
        ref        = zwparser.wiki_preprocess( ref )
        props, ref = zwparser._wiki_properties( ref )

        # Characterize the generated testcontent set the wikiproperties
        wikiprops   = {}
        testcontent = ( "@ %s " % wikiprops ) + '\n' + testcontent
        
        # Test by comparing the dumps
        try :
            tu      = zwparser.parse( testcontent, debuglevel=0 )
            result  = tu.dump()[:-1]
        except :
            # open( 'testcontent', 'w' ).write( testcontent )
            tu     = zwparser.parse( testcontent, debuglevel=2 )
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

    def test_1_textformatting( self ) :
        """Testing by randomly injecting wiki text formatting markup"""
        print "Testing by randomly injecting wiki text formatting markup"
        newlines = [ '\n' ] * 5 
        testlist = [ random_textformat( words + newlines, links, macros, htmls, 200 ) 
                     for i in range(100) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'rnd_textformatting', t, testcount
            testcount += 1

    def test_2_listformatting( self ) :
        """Testing by randomly injecting wiki text formatting and list markup"""
        print "\nTesting by randomly injecting wiki text formatting and list markup"
        testlist = [ '#\n' ] + \
                   [ random_listformat( words, links, macros, htmls, '\n', 200 ) 
                     for i in range(100) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'rnd_listformatting', t, testcount
            testcount += 1

    def test_3_bquoteformatting( self ) :
        """Testing by randomly injecting wiki text formatting and list markup"""
        print "\nTesting by randomly injecting wiki text formatting and",
        print "blockquote markup"
        testlist = [ '#\n' ] + \
                   [ random_bqformat( words, links, macros, htmls, '\n', 200 ) 
                     for i in range(100) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'rnd_bquoteformatting', t, testcount
            testcount += 1

    def test_4_tableformatting( self ) :
        """Testing by randomly injecting wiki text formatting and table markup"""
        print "\nTesting by randomly injecting wiki text formatting and table markup"
        testlist = [ random_tableformat( words, links, macros, htmls, '\n', 200 ) 
                     for i in range(100) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'rnd_tableformatting', t, testcount
            testcount += 1

    def test_5_wikitext( self ) :
        """Testing by randomly generating wiki words and markups"""
        print "\nTesting by randomly generating wiki words and markups"
        testlist = [ random_wikitext( words, links, macros, htmls, 200 ) 
                     for i in range(500) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'rnd_wikitext', t, testcount
            testcount += 1

    def test_6_wiki( self ) :
        """Testing by randomly generating wiki"""
        print "\nTesting by randomly generating wiki"
        testlist = [ random_wiki( 1000 ) for i in range(500) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'rnd_wiki', t, testcount
            testcount += 1
