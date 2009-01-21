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
specialchar  = ' ~`!@%&:;"<>_,^\'.?+\\()$-\t'
zwchars      = "*#=-|" 
pipechar     = '|'
escchar      = '~'
linkchars    = '[]'
macrochars   = '{}'

zwmarkup     = [ "''", '//', '__', '^^', ',,', "'/", "'/_", '\\\\', '[[', ']]', '{{', '}}' ]
zwmarkup_re  = [ r"''", r'//', r'__', r'\^\^', r',,', r"'/", r"'/_", r'\\\\',
                 r'\[\[', r'\]\]', r'{{', r'}}' ]

gen_psep     = lambda n : ''.join([ '\n' for i in range(randint(0,n)) ])
pseps        = [ gen_psep(i) for i in range(10) ]

ordmarklist  = [ '*', '**', '***', '****', '*****' ]
gen_ordmark  = lambda : choice(ordmarklist)

unordmarklist  = [ '#', '##', '###', '####', '#####' ]
gen_unordmark= lambda : choice(unordmarklist)

uri_resrved  = r':;/@&=,\?\#\+\$'
uri_mark     = r"_!~'\(\)\*\.\-"
uri_escape   = r'%'
uri          = alphanum + uri_resrved + uri_mark + uri_escape
gen_httpuri  = lambda   : 'http://' + ''.join([ choice(uri)
                                                for i in range(randint(1,100))])
gen_wwwuri   = lambda   : 'www.' + ''.join([ choice(uri)
                                                for i in range(randint(1,100))])

linktext     = alphanum + specialchar + zwchars + macrochars
linktxtlist  = [ ''.join([ choice( linktext ) for i in range(randint(1,50)) ])
                                              for i in range(200) ]
gen_link     = lambda   : '[[' + choice( linktxtlist ) + ']]' + ' '
links        = [ gen_link() for i in range(1000) ]

macrotext    = alphanum + specialchar + zwchars + linkchars
macrotxtlist = [ ''.join([ choice( macrotext ) for i in range(randint(1,50)) ])
                                               for i in range(200) ]
gen_macro    = lambda   : '{{' + choice( macrotxtlist ) + '}}' + ' '
macros       = [ gen_macro() for i in range(1000) ]



alltext      = alphanum + specialchar + zwchars + linkchars + macrochars
alltxtlist   = [ ''.join([ choice( alltext ) for i in range(randint(0,20)) ])
                                             for i in range(200) ]
gen_headtext = lambda : choice( alltxtlist ).replace( '=', '' )

def gen_word() :
    txt = choice( alltxtlist )
    for m in zwmarkup_re + [ '\n' ]  :
        txt = re.sub( m, '', txt, 10 ) 
    return txt + ' '

words        = [ gen_word() for i in range(2000) ] + \
               [ gen_httpuri() for i in range(100) ] + \
               [ gen_wwwuri() for i in range(100) ]

gen_fmtwords = lambda m, w, : m + ' ' + w + ' ' + m + ' '

def gen_texts( tc=1, pc=1, ec=1, lc=1, mc=1, fc=0, nopipe=True ) :
    # Generate contents
    wordlist  = [ choice(words) for i in range(tc) ]
    pwordlist = []
    for i in range(pc) :
        w = choice(words)
        pwordlist.append( w[:i] + pipechar + w[i:] )
    ewordlist = []
    for i in range(ec) :
        w = choice(words)
        ewordlist.append( w[:i] + escchar + w[i:] )
    linklist  = [ choice(links) for i in range(lc) ]
    macrolist = [ choice(macros) for i in range(mc) ]
    fwordlist = [ gen_fmtwords(
                    choice(zwmarkup),
                    ''.join([ choice(words) for j in range(randint(0,200)) ])
                  ) for i in range(fc) ]
    # Aggregate, shuffle and join contents
    texts = wordlist + pwordlist + ewordlist + linklist + macrolist + fwordlist
    shuffle(texts)
    texts = ''.join( texts )
    # Remove the pipe if present as the first character
    if nopipe :
        texts = choice(alphanum) + texts[0:]
    # Make ~ as ~~ if found at the end.
    if escchar and texts[-1] == escchar :
        texts = texts + escchar
    return texts

gen_cellstart = lambda : ' ' * randint(0,3) + '|' + ' ' * randint(0,3)

def gen_cell():
    wordlist  = [ choice(words) for i in range(randint(0,5)) ]
    ewordlist = []
    for i in range(randint(0,2)) :
        w = choice(words)
        ewordlist.append( w[:i] + escchar + w[i:] )
    linklist  = [ choice(links) for i in range(randint(0,2)) ]
    macrolist = [ choice(macros) for i in range(randint(0,2)) ]
    fwordlist = [ gen_fmtwords(
                    choice(zwmarkup),
                    ''.join([ choice(words) for j in range(randint(0,200)) ])
                  ) for i in range(randint(0,2)) ]
    # Aggregate, shuffle, join contents
    cell = [ w.replace('|', '') for w in wordlist + ewordlist + fwordlist ] +\
           linklist + macrolist
    shuffle( cell )
    cell = ''.join( cell )
    # Make ~ as ~~ if found at the end.
    if escchar and cell and cell[-1] == escchar :
        cell = cell + escchar
    return gen_cellstart() + cell 

gen_row     = lambda : ''.join([ gen_cell() for i in range(randint(0,4)) ]) + gen_cellstart()

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

    def test_heading( self ) :
        headmarkup= [ '=' , '==', '===', '====', '=====' ]
        testlist  = [ choice(headmarkup) + gen_headtext() +
                      choice(headmarkup) + gen_psep(1)
                        for i in range(1000) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'heading', t, testcount
            testcount += 1

    def test_hrule( self ) :
        self._test_execute( 'horizontalrule', '----', 1 )

    def test_option( self ) :
        testlist = [ '@options' +
                     ''.join([ choice(words) + '=' + choice(words) + ' ' for i in range(10) ]) +
                     gen_psep(randint(0,3))
                        for i in range(1000) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'pragma-options', t, testcount
            testcount += 1

    def test_tag( self ) :
        testlist = [ '@tags' +
                     ''.join([ choice(words) +', ' for i in range(10) ]) +
                     gen_psep(randint(0,3))
                        for i in range(1000) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'pragma-tags', t, testcount
            testcount += 1

    def test_nowiki( self ) :
        testlist = [ '{{{\n' +
                     '\n'.join([ choice(words) for i in range(randint(1,5)) ]) +
                     '\n}}}\n' + gen_psep(randint(0,3))
                        for i in range(1000) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'nowiki', t, testcount
            testcount += 1

    def test_textlines( self ) :
        testlist  = [ '\n'.join([ gen_texts( 5,1,2,1,1,1 )
                                    for j in range(randint(0,10)) ]) +
                      gen_psep(randint(0,3)) for i in range(1000) ]  +\
                    [ '\n'.join([ gen_texts( 5,1,2,1,1,0 )
                                    for j in range(randint(0,10)) ]) +
                      choice(zwmarkup) + ' ' +
                      '\n'.join([ gen_texts( 5,1,2,1,1,0 )
                                    for j in range(randint(0,10)) ]) +
                      choice(zwmarkup) + ' ' 
                      '\n'.join([ gen_texts( 5,1,2,1,1,0 )
                                    for j in range(randint(0,10)) ])
                      for i in range(10) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'textlines', t, testcount
            testcount += 1

    def test_table( self ) :
        testlist  = [ '\n'.join([ gen_row() for j in range(randint(0,10)) ]) +
                      gen_psep(randint(0,3)) for i in range(1000) ] 
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'table', t, testcount
            testcount += 1

    def test_ordlists( self ) :
        testlist  = [ '\n'.join([ gen_ordmark() + gen_texts( 5,1,2,1,1,1 )
                                    for j in range(randint(0,10)) ]) +
                      gen_psep(randint(0,3)) for i in range(1000) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'ordlists', t, testcount
            testcount += 1

    def test_unordlists( self ) :
        testlist  = [ '\n'.join([ gen_unordmark() + gen_texts( 5,1,2,1,1,1 )
                                    for j in range(randint(0,10)) ]) +
                      gen_psep(randint(0,3)) for i in range(1000) ]
        testcount = 1
        for t in testlist :
            yield self._test_execute, 'unordlists', t, testcount
            testcount += 1
