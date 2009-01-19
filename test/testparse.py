import unittest
import os
import difflib        as diff
from   random         import choice, randint, shuffle
import re

from   nose.tools     import assert_equal

from   zwiki.zwlexer  import ZWLexer
from   zwiki.zwparser import ZWParser

stdfiles_dir    = os.path.join( os.path.split( __file__ )[0], 'stdfiles' )
rndfiles_dir    = os.path.join( os.path.split( __file__ )[0], 'rndfiles' )
samplefiles_dir = os.path.join( os.path.split( __file__ )[0], 'samplefiles' )
zwparser        = None

def setUpModule() :
    global zwparser
    zwparser = ZWParser( lex_optimize=True, yacc_debug=True, yacc_optimize=False )
    
def tearDownModule() :
    pass

alphanum     = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
zwchars      = "*#'/_^,=" 
escapedtext  = [ '~*', '~#', "~'", '~/', '~_' ]
zwmarkup     = [ "''", '//', '__', '^^', ',,', "'/", "'/_", '\\\\', '[[', ']]', '{{', '}}' ]
zwmarkup_re  = [ r"''", r'//', r'__', r'\^\^', r',,', r"'/", r"'/_", r'\\\\',
                 r'\[\[', r'\]\]', r'{{', r'}}' ]
sqrtext      = '[]'
parantext    = '{}'
nontbltext   = '|'
alltext      = zwchars + alphanum + ' ~`!@%&:;"<>.?+\\()$-\t'
simpletext   = alphanum + ' ~`!@%&:;"<>.?+\\()$-\t'

basictxtlist = [ ''.join([ choice(alltext) for i in range(randint(0,10)) ])
                     for i in range(200) ]
tabletxtlist = [ ''.join([ choice(alltext+(sqrtext*1)+(parantext*1))
                           for i in range(randint(0,10)) ])
                     for i in range(200) ]
macrotxtlist = [ ''.join([ choice(alltext+(sqrtext*1))
                           for i in range(randint(1,10)) ])
                     for i in range(200) ]
linktxtlist  = [ ''.join([ choice(alltext+(nontbltext*1)+(parantext*1))
                           for i in range(randint(1,10)) ])
                     for i in range(200) ]

uri_resrved  = r':;/@&=,\?\#\+\$'
uri_mark     = r"_!~'\(\)\*\.\-"
uri_escape   = r'%'
uri          = alphanum + uri_resrved + uri_mark + uri_escape

gen_psep     = lambda n : ''.join([ '\n' for i in range(randint(0,n)) ])
gen_link     = lambda   : '[[' + choice(linktxtlist) + ']]'
gen_macro    = lambda   : '{{' + choice(macrotxtlist) + '}}'
gen_httpuri  = lambda   : 'http://' + ''.join([ choice(uri)
                                                for i in range(randint(1,100))])
gen_wwwuri   = lambda   : 'www.' + ''.join([ choice(uri)
                                                for i in range(randint(1,100))])

def gen_formattedtext( tbltextc=0, textc=0, escc=0, linkc=0, macroc=0, fmttxtc=0 ) :
    alltxts = [ choice(tabletxtlist) for i in range(tbltextc) ] + \
              ([nontbltext] * textc) + \
              [ choice(escapedtext) for i in range(escc) ] +\
              [ gen_link() for i in range(linkc) ] + \
              [ gen_macro() for i in range(macroc) ]
    alltxts = [ re.sub( m, '', txt, 100 ) for txt in alltxts for m in zwmarkup_re + ['\n'] ]

    shuffle( alltxts )
    idxlist = range(len(alltxts))
    for i in range(fmttxtc) :
        idx = choice(idxlist)
        idxlist.remove(idx)
        markup   = choice(zwmarkup)
        alltxts[idx] = markup + ' ' + alltxts[idx]
        alltxts[idx] = alltxts[idx] + ' ' +  markup
    return ' '.join(alltxts)

def gen_textline( tbltextc=0, textc=0, escc=0, linkc=0, macroc=0, fmttxtc=0 ) :
    firstchoice = simpletext.replace(' ', '')
    firstchoice = simpletext.replace('\t', '')
    textline    = choice(firstchoice) + \
                  gen_formattedtext( tbltextc, textc, escc, linkc, macroc, fmttxtc )
    return textline

class TestDumpsValid( object ) :
    """Test cases to validate ZWiki lexer."""

    def _test_execute( self, type, testcontent, count ) :
        try :
            tu      = zwparser.parse( testcontent, debuglevel=0 )
            result  = tu.dump()[:-1]
        except :
            tu     = zwparser.parse( testcontent, debuglevel=2 )
            result = tu.dump()[:-1]
        if result != testcontent :
            print ''.join(diff.ndiff( result.splitlines(1), testcontent.splitlines(1) ))
        assert result == testcontent, type+'... testcount %s'%count

    #def test_heading( self ) :
    #    headmarkup= [ '=' , '==', '===', '====', '=====' ]
    #    testlist  = [ choice(headmarkup) + \
    #                  gen_formattedtext(1,1,1,1,1,3).replace('=','') + \
    #                  choice(headmarkup) + gen_psep(1)
    #                    for i in range(500) ]
    #    testcount = 1
    #    for t in testlist :
    #        yield self._test_execute, 'heading', t, testcount
    #        testcount += 1

    #def test_hrule( self ) :
    #    self._test_execute( 'horizontalrule', '----', 1 )

    #def test_option( self ) :
    #    testlist = [ '@options' + \
    #                 gen_formattedtext(4,5,2,2,3,3) + \
    #                 gen_psep(randint(0,3))
    #                 for i in range(500) ]
    #    testcount = 1
    #    for t in testlist :
    #        yield self._test_execute, 'pragma-options', t, testcount
    #        testcount += 1

    #def test_tag( self ) :
    #    testlist = [ '@tags' + \
    #                 gen_formattedtext(4,5,2,2,3,3) + \
    #                 gen_psep(randint(0,3))
    #                 for i in range(500) ]
    #    testcount = 1
    #    for t in testlist :
    #        yield self._test_execute, 'pragma-tags', t, testcount
    #        testcount += 1

    #def test_nowiki( self ) :
    #    testlist = [ '{{{\n' +
    #                 '\n'.join([ gen_formattedtext(2,3,1,2,3,3)
    #                                for i in range(randint(1,5)) ]) +\
    #                 '\n}}}\n' + \
    #                 gen_psep(randint(0,3))
    #                 for i in range(100) ]
    #    testcount = 1
    #    for t in testlist :
    #        yield self._test_execute, 'nowiki', t, testcount
    #        testcount += 1

    def test_textlines( self ) :
        testlist  = [ '\n'.join([ gen_textline(5,1,2,5,1,2)
                                    for i in range(randint(0,5)) ]) +\
                      gen_psep(randint(0,3))
                      for i in range(1000) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'textlines', t, testcount
            testcount += 1

    #def test_table( self ) :
    #    print ""
    #    tu  = zwparser.parse( table, debuglevel=0 )
    #    tu.show( showcoord=False )

    #def test_ordlists( self ) :
    #    print ""
    #    tu  = zwparser.parse( ordlists, debuglevel=2 )
    #    tu.show( showcoord=False )

    #def test_unordlists( self ) :
    #    print ""
    #    tu  = zwparser.parse( unordlists, debuglevel=0 )
    #    tu.show( showcoord=False )
