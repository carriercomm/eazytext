#! /usr/bin/env python

"""Module containing the Lexer for ZWiki"""

# -*- coding: utf-8 -*-

# Gotcha :
#   1. Enabling optimize screws up the order of regex match (while lexing)
#      Bug in PLY ???
# Notes  : None
# Todo   :
#   1. Due to ordering issues the following functions are created from
#      simple regex variables.


import re
import sys

import ply.lex
from   ply.lex import TOKEN

class ZWLexer( object ):
    """A lexer for the ZWiki markup.
        build() To build   
        input() Set the input text
        token() To get new tokens.
    The public attribute filename can be set to an initial filaneme, but the
    lexer will update it upon #line directives."""

    ## -------------- Internal auxiliary methods ---------------------

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
    
    ## --------------- Interface methods ------------------------------

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
        self.lexer = ply.lex.lex( module=self,
                                  reflags=re.MULTILINE | re.UNICODE,
                                  **kwargs
                                )

    def reset_lineno( self ):
        """ Resets the internal line number counter of the lexer."""
        self.lexer.lineno = 1

    def input( self, text ):
        """`text` to tokenise"""
        self.lexer.input( text )
    
    def token( self ):
        """Get the next token"""
        tok = self.lexer.token()
        return tok 

    # States

    states = (
               ( 'nowiki',    'exclusive' ),
               ( 'table',     'exclusive' ),
               ( 'bigtable',  'exclusive' ),
             )

    ## Tokens recognized by the ZWLexer

    tokens = (
        # RegEx tokens.
        'PIPE', 'ALPHANUM',  'SPECIALCHAR', 'SQR_OPEN', 'SQR_CLOSE',
        'PARAN_OPEN', 'PARAN_CLOSE', 'ANGLE_OPEN', 'ANGLE_CLOSE', 'HTTP_URI', 'WWW_URI',

        # Line markups
        'HORIZONTALRULE', 'HEADING',   'ORDLIST_START', 'UNORDLIST_START',
        'DEFINITION_START', 'BQUOTE_START', 'TABLE_CELLSTART',
        'BIGTABLE_OPEN', 'BIGTABLE_CLOSE', 'BIGTABLE_ROW', 'BIGTABLE_HEADCELL',
        'BIGTABLE_HEADCELLSTYLE', 'BIGTABLE_CELL', 'BIGTABLE_CELLSTYLE',
        'BIGTABLE_BREAK',

        # Block markups
        'NOWIKI_OPEN', 'NOWIKI_CLOSE', 'NOWIKI_CHARS', 'NOWIKI_SPECIALCHAR',

        # Special tokens
        'LINK', 'MACRO', 'HTML',
        'NEWLINE', 'ESCAPED',
        'ENDMARKER',
    )

    ## Rules for the lexer.

    def t_HORIZONTALRULE( self, t ):
        r'^-{4,}[ \t]*$'
        return t

    def t_HEADING( self, t ):
        r'^={1,5}[^=\n\r]+={0,5}$'
        return t

    def t_NOWIKI_OPEN( self, t ) :
        r'^{{{[ \t]*[a-zA-Z0-9_\-\.]*[ \t]*$'
        t.lexer.push_state('nowiki')
        return t

    def t_nowiki_NOWIKI_CLOSE( self, t ):
        r'^[ \t]*}}}$'
        t.lexer.pop_state()
        return t

    def t_nowiki_ENDMARKER( self, t ):  
        r'\<\{\<\{\}\>\}\>'
        return t

    def t_nowiki_NOWIKI_CHARS( self, t ):  
        r'[^{}\r\n]+'
        return t

    def t_nowiki_NEWLINE( self, t ):
        r'(\r?\n)|\r'
        return t

    def t_nowiki_NOWIKI_SPECIALCHAR( self, t ):  
        r'[{}]'
        return t

    def t_TABLE_CELLSTART( self, t ):
        r'^[ \t]*\|=?'
        t.lexer.push_state('table')
        return t

    def t_table_TABLE_CELLSTART( self, t ):
        r'[ \t]*\|=?'
        return t

    def t_table_NEWLINE( self, t ):
        r'(\r?\n)|\r'
        t.lexer.pop_state()
        return t

    def t_table_ESCAPED( self, t ):
        r'~.'
        t.value = t.value[1]
        return t

    def t_table_LINK( self, t ):
        r'\[\[[^\[\]\r\n]+\]\]'
        return t

    def t_table_MACRO( self, t ):
        r'\{\{[^\r\n]+\}\}'
        return t

    def t_table_HTML( self, t ):
        r"\[<[^\r\n]+>\]"
        return t

    def t_BIGTABLE_OPEN( self, t ):
        r'^[ \t]*\{\|.*$'
        t.lexer.push_state('bigtable')
        return t

    def t_bigtable_BIGTABLE_CLOSE( self, t ):
        r'^[ \t]*\|\}.*$'
        t.lexer.pop_state()
        return t

    def t_bigtable_ENDMARKER( self, t ):  
        r'\<\{\<\{\}\>\}\>'
        return t

    def t_bigtable_BIGTABLE_ROW( self, t ):
        r'^[ \t]*\|\-.*$'
        return t

    def t_bigtable_BIGTABLE_HEADCELLSTYLE( self, t ):
        r'^[ \t]*\|\|style.*\|'
        return t

    def t_bigtable_BIGTABLE_HEADCELL( self, t ):
        r'^[ \t]*\|\|'
        return t

    def t_bigtable_BIGTABLE_CELLSTYLE( self, t ):
        r'^[ \t]*\|style.*\|'
        return t

    def t_bigtable_BIGTABLE_CELL( self, t ):
        r'^[ \t]*\|[ ]{1}'
        return t

    def t_bigtable_BIGTABLE_BREAK( self, t ):
        r"^[ \t]*\n|[^\|\r\n]"
        t.lexer.pop_state()
        return t

    def t_bigtable_NEWLINE( self, t ):
        r'(\r?\n)|\r'
        return t

    def t_bigtable_ESCAPED( self, t ):
        r'~.'
        t.value = t.value[1]
        return t

    def t_bigtable_LINK( self, t ):
        r'\[\[[^\[\]\r\n]+\]\]'
        return t

    def t_bigtable_MACRO( self, t ):
        r'\{\{[^\r\n]+\}\}'
        return t

    def t_bigtable_HTML( self, t ):
        r"\[<[^\r\n]+>\]"
        return t

    def t_ORDLIST_START( self, t ):
        r'^[ \t]*\#{1,5}'
        return t

    def t_UNORDLIST_START( self, t ):
        r'^[ \t]*\*{1,5}'
        return t

    def t_DEFINITION_START( self, t ):
        r'^[ \t]*:[^\n\r]*::'
        return t

    def t_BQUOTE_START( self, t ):
        r'^[ \t]*\>{1,5}'
        return t

    def t_LINK( self, t ):
        r'\[\[[^\[\]\r\n]+\]\]'
        return t

    def t_MACRO( self, t ):
        r'\{\{[^\r\n]+\}\}'
        return t

    def t_HTML( self, t ):
        r"\[<[^\r\n]+>\]"
        return t

    def t_ESCAPED( self, t ):
        r'~.'
        t.value = t.value[1]
        return t

    def t_NEWLINE( self, t ):
        r'(\r?\n)|\r'
        return t

    def t_ENDMARKER( self, t ):  
        r'\<\{\<\{\}\>\}\>'
        return t

    # Complex regex
    http_schema    = r'http://'
    www_domain     = r'www\.'
    uri_reserved   = r':;/@&=,\?\#\+\$'
    uri_mark       = r"_!'\(\)\*\.\-"
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

    @TOKEN(http_uri)
    def t_bigtable_HTTP_URI( self, t ):
        return t

    @TOKEN(www_uri)
    def t_bigtable_WWW_URI( self, t ):
        return t

    # Tokens

    t_PIPE              = r'\|'
    t_ALPHANUM          = r'[a-zA-Z0-9]+'
    t_SQR_OPEN          = r'\['
    t_SQR_CLOSE         = r'\]'
    t_PARAN_OPEN        = r'\{'
    t_PARAN_CLOSE       = r'\}'
    t_ANGLE_OPEN        = r'\<'
    t_ANGLE_CLOSE       = r'\>'
    t_SPECIALCHAR       = r'[ `!@%&:;="/_, \^\'\#\*\.\?\+\\\(\)\$\-\t]+'
    
    t_table_ALPHANUM     = r'[a-zA-Z0-9]+'
    t_table_SQR_OPEN     = r'\['
    t_table_SQR_CLOSE    = r'\]'
    t_table_PARAN_OPEN   = r'\{'
    t_table_PARAN_CLOSE  = r'\}'
    t_table_ANGLE_OPEN   = r'\<'
    t_table_ANGLE_CLOSE  = r'\>'
    t_table_SPECIALCHAR  = r'[ `!@%&:;="/_, \^\'\#\*\.\?\+\\\(\)\$\-\t]+'

    t_bigtable_ALPHANUM     = r'[a-zA-Z0-9]+'
    t_bigtable_SQR_OPEN     = r'\['
    t_bigtable_SQR_CLOSE    = r'\]'
    t_bigtable_PARAN_OPEN   = r'\{'
    t_bigtable_PARAN_CLOSE  = r'\}'
    t_bigtable_ANGLE_OPEN   = r'\<'
    t_bigtable_ANGLE_CLOSE  = r'\>'
    t_bigtable_SPECIALCHAR  = r'[ `!@%&:;="/_, \^\'\#\*\.\?\+\\\(\)\$\-\t]+'

    def t_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_nowiki_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_table_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_bigtable_error( self, t ):
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
