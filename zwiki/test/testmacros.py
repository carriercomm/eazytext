import unittest
import os
import difflib            as diff
from   random             import choice, randint, shuffle

from   nose.tools         import assert_equal, assert_raises, assert_true, \
                                 assert_false

from   zwiki.zwlexer      import ZWLexer
from   zwiki.zwparser     import ZWParser
from   zwiki.test.testlib import ZWMARKUP, ZWMARKUP_RE, \
                                 gen_psep, gen_ordmark, gen_unordmark, \
                                 gen_headtext, gen_texts, gen_row, \
                                 gen_wordlist, gen_words, gen_linkwords, gen_links,\
                                 gen_macrowords, gen_macros, \
                                 random_textformat, random_listformat, \
                                 random_tableformat, random_wikitext, random_wiki


stdfiles_dir    = os.path.join( os.path.split( __file__ )[0], 'stdfiles' )
rndfiles_dir    = os.path.join( os.path.split( __file__ )[0], 'rndfiles' )
samplefiles_dir = os.path.join( os.path.split( __file__ )[0], 'samplefiles' )
zwparser        = None
words           = None

def setUpModule() :
    global zwparser, words
    print "Initialising the parser ..."
    zwparser     = ZWParser( lex_optimize=True, yacc_debug=True,
                           yacc_optimize=False )
    print "Initialising wiki ..."
    alphanum = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    words    = [ ''.join([ choice( alphanum ) for i in range(randint(0, 20)) ])
                 for j in range( 1000 ) ]
    
def tearDownModule() :
    pass

class TestMacroDumpsRandom( object ) :
    """Test cases to validate Macro random"""

    def _test_execute( self, type, testcontent, count, ref='', cfunc=None  ) :
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
            tu     = zwparser.parse( testcontent, debuglevel=2 )
            result = tu.dump()[:-1]
        if result != ref :
            print ''.join(diff.ndiff( result.splitlines(1), ref.splitlines(1) ))
        assert result == ref, type+'... testcount %s'%count

        if cfunc :
            cfunc( ref, tu )

    def test_0_file( self ) :
        """If file `ref` is available pick it and test it"""
        testlist  = []
        ref       = os.path.isfile( 'ref' ) and open( 'ref' ).read()
        ref and testlist.append( ref )
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'ref', t, testcount
            testcount += 1

    def test_1_clear( self ) :
        """Testing the Clear() macro"""
        print "\nTesting the Clear() macro"
        testlist = [ '\n'.join([ gen_texts( words, [] , [],
                                            tc=5, pc=0, ec=0, lc=0, mc=0, fc=0,
                                            nopipe=True
                                          )
                                 for j in range(randint(0,10)) ])
                     for k in range(100) ]
        clear_macros = [ '{{ Clear() }}', '{{Clear() }}', '{{ Clear() }}' ]

        def clear_cfunc( ref, tu ) :
            html= tu.tohtml()
            assert_true( 'clear : both' in html,
                         'Fail Clear Macro : %s ' % html )

        testcount = 1
        for t in testlist :
            off = randint( 0, len(t) )
            t   = t.replace( '{', '' )
            t   = t.replace( '}', '' )
            t   = t[:off] + choice( clear_macros ) + t[off:]
            yield self._test_execute, 'macro_clear', t, testcount, '', \
                  clear_cfunc
            testcount += 1

    def test_2_span( self ) :
        """Testing the Span() macro"""
        print "\nTesting the Span() macro"
        testlist = [ '\n'.join([ gen_texts( words, [], [],
                                            tc=5, pc=0, ec=0, lc=0, mc=0, fc=0,
                                            nopipe=True
                                          )
                                 for j in range(randint(0,10)) ])
                     for k in range(100) ]
        span_macros = [ [ '{{ Span("Hello World") }}',
                          [ 'Hello World' ] ],
                        [ '{{ Span("How are you") }}',
                          [ 'How are you' ] ],
                        [ '{{ Span("With style", style={ "font-weight" : "bold"} ) }}',
                          [ 'With style', 'font-weight : bold' ] ] ,
                        [ '{{ Span("With kw styles", color="blue") }}',
                          [ 'With kw styles', 'color : blue' ] ]
                      ]

        def span_cfunc( macro_ref ) :
            def cfunc( ref, tu ) :
                html= tu.tohtml()
                for r in macro_ref :
                    assert_true( r in html, 'Fail Span Macro : %s ' % html )
            return cfunc

        testcount = 1
        for t in testlist :
            off = randint( 0, len(t) )
            m   = choice( span_macros )
            t   = t[:off] + m[0] + t[off:]
            yield self._test_execute, 'macro_span', t, testcount, '', \
                  span_cfunc( m[1] )
            testcount += 1

    def test_3_redirect( self ) :
        """Testing the Redirect() macro"""
        print "\nTesting the Redirect() macro"
        testlist = [ '\n'.join([ gen_texts( words, [] , [],
                                            tc=5, pc=0, ec=0, lc=0, mc=0, fc=0,
                                            nopipe=True
                                          )
                                 for j in range(randint(0,10)) ])
                     for k in range(100) ]
        redirect_macros = [ [ '{{ Redirect("Hello World") }}',
                              [ 'Hello World' ] ],
                            [ '{{ Redirect("/") }}',
                              [ '/' ] ],
                            [ '{{ Redirect("/hello/world") }}',
                              [ '/hello/world' ] ],
                          ]

        def redirect_cfunc( macro_ref ) :
            def cfunc( ref, tu ) :
                tu.tohtml()
                for r in macro_ref :
                    assert_true( r == tu.parser.zwparser.redirect,
                                 'Fail Redirect Macro' )
            return cfunc

        testcount = 1
        for t in testlist :
            m   = choice( redirect_macros )
            t   = m[0] + t
            yield self._test_execute, 'macro_redirect', t, testcount, '', \
                  redirect_cfunc( m[1] )
            testcount += 1

    def test_4_html( self ) :
        """Testing the Html() macro"""
        print "\nTesting the Html() macro"
        testlist = [ '\n'.join([ gen_texts( words, [], [],
                                            tc=5, pc=0, ec=0, lc=0, mc=0, fc=0,
                                            nopipe=True
                                          )
                                 for j in range(randint(0,10)) ])
                     for k in range(100) ]
        html_macros = [ [ '{{ Html("<table><tr><td>hello world</td></tr></table>") }}',
                          [ '<table><tr><td>hello world</td></tr></table>' ] ],
                      ]

        def html_cfunc( macro_ref ) :
            def cfunc( ref, tu ) :
                html= tu.tohtml()
                for r in macro_ref :
                    assert_true( r in html, 'Fail Html Macro : %s ' % html )
            return cfunc

        testcount = 1
        for t in testlist :
            off = randint( 0, len(t) )
            m   = choice( html_macros )
            t   = t[:off] + m[0] + t[off:]
            yield self._test_execute, 'macro_html', t, testcount, '', \
                  html_cfunc( m[1] )
            testcount += 1

    def test_5_toc( self ) :
        """Testing the Toc() macro"""
        print "\nTesting the Toc() macro"
        testlist = [ '\n'.join([ gen_texts( words, [], [],
                                            tc=5, pc=0, ec=0, lc=0, mc=0, fc=0,
                                            nopipe=True
                                          )
                                 for j in range(randint(0,10)) ])
                     for k in range(100) ]
        toc_macros = [ '{{ Toc( indent=1 ) }}', '{{Toc() }}',
                       '{{ Toc( indent=2 ) }}' ]
        testcount = 1

        def toc_cfunc( ref, tu ) :
            html= tu.tohtml()
            assert_true( 'name="TOC"' in html,
                         'Fail Toc Macro : %s ' % html )

        for t in testlist :
            t   = choice( toc_macros ) + t
            yield self._test_execute, 'macro_toc', t, testcount, '', \
                  toc_cfunc
            testcount += 1
