#! /usr/bin/env python

"""Module containing the Lexer for tokenizing text-markups"""

# -*- coding: utf-8 -*-

# Gotcha :
#   1. Enabling optimize screws up the order of regex match (while lexing)
#      Bug in PLY ???
# Notes  :
# Todo   :


import re
import sys

import ply.lex
from   ply.lex import TOKEN

class TextLexer( object ):
    """A lexer for the text markup.
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
               # ( 'nowiki', 'exclusive' ),
             )

    ## Tokens recognized by the TextLexer
    tokens = (
        'M_SPAN', 'M_BOLD', 'M_ITALIC', 'M_UNDERLINE', 'M_SUPERSCRIPT',
        'M_SUBSCRIPT', 'M_BOLDITALIC', 'M_BOLDUNDERLINE', 'M_ITALICUNDERLINE',
        'M_BOLDITALICUNDERLINE',
    )

    ## Rules for the lexer.

    def t_M_SPAN( self, t ) :
        r"``(\{.*\})?"
        print t
        return t

    def t_M_BOLDITALICUNDERLINE( self, t ) :
        "('/_|_/')(\{.*\})?"
        return t

    def t_M_BOLD( self, t ) :
        r"''(\{.*\})?"
        return t

    def t_M_ITALIC( self, t ) :
        r"//(\{.*\})?"
        return t

    def t_M_UNDERLINE( self, t ) :
        r"__(\{.*\})?"
        return t

    def t_M_SUPERSCRIPT( self, t ) :
        r"\^\^(\{.*\})?"
        return t

    def t_M_SUBSCRIPT( self, t ) :
        r",,(\{.*\})?"
        return t

    def t_M_BOLDITALIC( self, t ) :
        r"('/|/')(\{.*\})?"
        return t

    def t_M_ITALICUNDERLINE( self, t ) :
        r"(/_|_/)(\{.*\})?"
        return t

    def t_M_BOLDUNDERLINE( self, t ) :
        r"('_|_')(\{.*\})?"
        return t

    # Tokens
    t_M_SPCHAR  = r"['/_,`\{}^]"
    t_M_TEXT    = r"[^'/_,`\{}^]+"

    def t_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)


if __name__ == "__main__":
    def errfoo(msg, a, b):
        print msg
        sys.exit()
    
    text = open( 'zwiki' ).read()
    textlex = TextLexer( errfoo )
    textlex.build()
    textlex.input( text )
    
    while 1:
        tok = textlex.token()
        if not tok: break
        print "-", tok.value, tok.type, tok.lineno, textlex.filename, tok.lexpos
