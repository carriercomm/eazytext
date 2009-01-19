#! /usr/bin/env python

import re
import sys

import ply.lex
from   ply.lex import TOKEN

class ZWLexer( object ):
    """A lexer for the ZWiki markup. After building it, set the input text with
    input(), and call token() to get new tokens.
        
    The public attribute filename can be set to an initial filaneme, but the
    lexer will update it upon #line directives."""

    def __init__( self, error_func=None ):
        """ Create a new Lexer.
        
        error_func:
            An error function. Will be called with an error message, line
            and column as arguments, in case of an error during lexing."""
        self.error_func = error_func
        self.filename = ''

    def build( self, **kwargs ):
        """ Builds the lexer from the specification. Must be called after the
        lexer object is created. 
            
        This method exists separately, because the PLY manual warns against
        calling lex.lex inside __init__"""
        self.lexer = ply.lex.lex(object=self, reflags=re.MULTILINE, **kwargs)

    def reset_lineno( self ):
        """ Resets the internal line number counter of the lexer."""
        self.lexer.lineno = 1

    def input( self, text ):
        self.lexer.input(text)
    
    def token( self ):
        g = self.lexer.token()
        return g

    ## Internal auxiliary methods
    def _error( self, msg, token ):
        location = self._make_tok_location( token )
        self.error_func and self.error_func( msg, location[0], location[1] )
        self.lexer.skip( 1 )
        print "error: %s %s" % (msg, token)
    
    def _find_tok_column( self, token ):
        i = token.lexpos
        while i > 0:
            if self.lexer.lexdata[i] == '\n': break
            i -= 1
        return (token.lexpos - i) + 1
    
    def _make_tok_location( self, token ):
        return ( token.lineno, self._find_tok_column(token) )
    
    # States
    states = (
               ( 'nowiki', 'exclusive' ),
               ( 'table',  'exclusive' ),
             )

    ## All the tokens recognized by the lexer
    tokens = (
        # RegEx tokens.
        'PIPE',  'STAR', 'POUND', 'SINGLEQUOTE',  'FORWARDSLASH', 'BACKSLASH', 'UNDERSCORE',
        'XOR', 'COMMA', 'SQR_OPEN', 'SQR_CLOSE', 'PARAN_OPEN',
        'PARAN_CLOSE', 'ALPHANUM',  'SPECIALCHAR', 'HTTP_URI', 'WWW_URI',

        # Pragmas
        'OPTIONS', 'TAGS',

        # Line markups
        'HORIZONTALRULE', 'HEADING',   'ORDLIST_START', 'UNORDLIST_START',

        # Block markups
        'NOWIKI_OPEN', 'NOWIKI_CLOSE', 'NOWIKI_CHARS', 'NOWIKI_SPECIALCHAR',

        # Text markups
        'LINEBREAK',  'BOLD', 'ITALIC', 'UNDERLINE', 'SUPERSCRIPT', 'SUBSCRIPT',
        'BOLDITALIC', 'BOLDITALICUNDERLINE',

        # Special tokens
        'TABLE_ROWSTART', 'TABLE_ROWEND', 'TABLE_CELLSTART',

        'LINK', 'MACRO',

        'NEWLINE', 'ESCAPED',
    )

    ## Rules for the lexer.
    def t_OPTIONS( self, t ):
        r'^@options.*$'
        return t

    def t_TAGS( self, t ):
        r'^@tags.*$'
        return t

    def t_ESCAPED( self, t ):
        r'~.'
        t.value = t.value[1]
        return t

    def t_HORIZONTALRULE( self, t ):
        r'^-{4,}[ \t]*$'
        return t

    def t_HEADING( self, t ):
        r'^={1,5}[^=\n\r]+={0,5}$'
        return t

    def t_NOWIKI_OPEN( self, t ) :
        r'^{{{$'
        t.lexer.push_state('nowiki')
        return t

    def t_nowiki_NOWIKI_OPEN( self, t ):
        r'^{{{$'
        return t

    def t_nowiki_NOWIKI_CHARS( self, t ):  
        r'[^{}\r\n]+'
        return t

    def t_nowiki_NOWIKI_CLOSE( self, t ):
        r'^}}}$'
        t.lexer.pop_state()
        return t

    def t_nowiki_NOWIKI_SPECIALCHAR( self, t ):  
        r'[{}]'
        return t

    def t_TABLE_ROWSTART( self, t ):
        r'^[ \t]*\|'
        t.lexer.push_state('table')
        return t

    def t_table_TABLE_CELLSTART( self, t ):
        r'[ \t]*\|'
        return t

    def t_table_TABLE_ROWEND( self, t ):
        r'$'
        t.lexer.pop_state()
        return t

    def t_table_LINK( self, t ):
        r'\[\[[^\[\]\r\n]+\]\]'
        return t

    def t_table_MACRO( self, t ):
        r'\{\}[^\{\}\r\n]+\}\}'
        return t

    def t_table_LINEBREAK( self, t ):
        r"\\\\"
        return t

    def t_table_BOLD( self, t ):
        r"''"
        return t

    def t_table_ITALIC( self, t ):
        r"//"
        return t

    def t_table_UNDERLINE( self, t ):
        r"__"
        return t

    def t_table_SUPERSCRIPT( self, t ):
        r"\^\^"
        return t

    def t_table_SUBSCRIPT( self, t ):
        r",,"
        return t

    def t_table_BOLDITALIC( self, t ):
        r"'/"
        return t

    def t_table_BOLDITALICUNDERLINE( self, t ):
        r"'/_"
        return t

    def t_ORDLIST_START( self, t ):
        r'^[ \t]*\*{1,5}'
        return t

    def t_UNORDLIST_START( self, t ):
        r'^[ \t]*\#{1,5}'
        return t

    def t_LINK( self, t ):
        r'\[\[[^\[\]\r\n]+\]\]'
        return t

    def t_MACRO( self, t ):
        r'\{\}[^\{\}\r\n]+\}\}'
        return t

    def t_LINEBREAK( self, t ):
        r"\\\\"
        return t

    def t_BOLD( self, t ):
        r"''"
        return t

    def t_ITALIC( self, t ):
        r"//"
        return t

    def t_UNDERLINE( self, t ):
        r"__"
        return t

    def t_SUPERSCRIPT( self, t ):
        r"\^\^"
        return t

    def t_SUBSCRIPT( self, t ):
        r",,"
        return t

    def t_BOLDITALIC( self, t ):
        r"'/"
        return t

    def t_BOLDITALICUNDERLINE( self, t ):
        r"'/_"
        return t

    def t_ANY_NEWLINE( self, t ):
        r'(\r?\n)|\r'
        return t

    # Tokens
    t_PIPE         = r'\|'
    t_STAR         = r'\*'
    t_POUND        = r'\#'
    t_SINGLEQUOTE  = r"'"
    t_FORWARDSLASH = r'/'
    t_BACKSLASH    = r'\\'
    t_UNDERSCORE   = r'_'
    t_XOR          = r'\^'
    t_COMMA        = r','
    t_SQR_OPEN     = r'\['
    t_SQR_CLOSE    = r'\]'
    t_PARAN_OPEN   = r'\{'
    t_PARAN_CLOSE  = r'\}'
    t_ALPHANUM     = r'[a-zA-Z0-9]+'
    t_SPECIALCHAR  = r'[ ~`!@%&:;="<> \.\?\+\\\(\)\$\-\t]+'
    
    t_table_STAR         = r'\*'
    t_table_POUND        = r'\#'
    t_table_SINGLEQUOTE  = r"'"
    t_table_FORWARDSLASH = r'/'
    t_table_BACKSLASH    = r'\\'
    t_table_UNDERSCORE   = r'_'
    t_table_XOR          = r'\^'
    t_table_COMMA        = r','
    t_table_SQR_OPEN     = r'\['
    t_table_SQR_CLOSE    = r'\]'
    t_table_PARAN_OPEN   = r'\{'
    t_table_PARAN_CLOSE  = r'\}'
    t_table_ALPHANUM     = r'[a-zA-Z0-9]+'
    t_table_SPECIALCHAR  = r'[ ~`!@%&:;="<> \.\?\+\\\(\)\$\-\t]+'

    # Complex regex
    http_schema    = r'http://'
    www_domain     = r'www\.'
    uri_reserved   = r':;/@&=,\?\#\+\$'
    uri_mark       = r"_!~'\(\)\*\.\-"
    uri_escape     = r'%'
    http_uri       = http_schema + r'[a-zA-Z0-9' + uri_escape + uri_reserved + uri_mark + r']+'
    www_uri        = www_domain + r'[a-zA-Z0-9' + uri_escape + uri_reserved + uri_mark + r']+'

    @TOKEN(http_uri)
    def t_HTTP_URI( self, t ):
        return t

    @TOKEN(www_uri)
    def t_WWW_URI( self, t ):
        return t

    @TOKEN(http_uri)
    def t_table_HTTP_URI( self, t ):
        return t

    @TOKEN(www_uri)
    def t_table_WWW_URI( self, t ):
        return t

    def t_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_nowiki_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_table_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)



if __name__ == "__main__":
    def errfoo(msg, a, b):
        print msg
        sys.exit()
    
    text = "hello"
    zwlex = ZWLexer( errfoo )
    zwlex.build()
    zwlex.input(text)
    
    while 1:
        tok = zwlex.token()
        if not tok: break
        print "-", tok.value, tok.type, tok.lineno, zwlex.filename, tok.lexpos
        

