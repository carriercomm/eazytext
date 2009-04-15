import re
import sys
from   types    import StringType

import ply.yacc

from   zwlexer  import ZWLexer
from   zwast    import *

# TODO :
#   1. There are several if-elif statements which needs to have a default else
#      block (atleast to raise exception).

class Coord( object ):
    """ Coordinates of a syntactic element. Consists of:
        - File name
        - Line number
        - (optional) column number, for the Lexer
    """
    def __init__( self, file, line, column=None ):
        self.file = file
        self.line = line
        self.column = column

    def __str__( self ):
        str = "%s:%s" % (self.file, self.line)
        if self.column :
            str += ":%s" % self.column
        return str


class ParseError( Exception ):
    pass


class ZWParser( object ):
    def __init__(   self, 
                    lex_optimize=False,
                    lextab='zwiki.lextab',
                    lex_debug=False,
                    yacc_optimize=False,
                    yacctab='zwiki.yacctab',
                    yacc_debug=True
                ):
        """Create a new ZWParser.
        
        Some arguments for controlling the debug/optimization level of the
        parser are provided. The defaults are tuned for release/performance
        mode.
           
        The simple rules for using them are:
            *) When tweaking ZWParser/ZWLexer, set these to False
            *) When releasing a stable parser, set to True
            
        lex_optimize:
            Set to False when you're modifying the lexer. Otherwise, changes
            in the lexer won't be used, if some lextab.py file exists.
            When releasing with a stable lexer, set to True to save the
            re-generation of the lexer table on each run.
            
        lextab:
            Points to the lex table that's used for optimized mode. Only if
            you're modifying the lexer and want some tests to avoid
            re-generating the table, make this point to a local lex table file
            (that's been earlier generated with lex_optimize=True)
            
        yacc_optimize:
            Set to False when you're modifying the parser. Otherwise, changes
            in the parser won't be used, if some parsetab.py file exists.
            When releasing with a stable parser, set to True to save the
            re-generation of the parser table on each run.
            
        yacctab:
            Points to the yacc table that's used for optimized mode. Only if
            you're modifying the parser, make this point to a local yacc table
            file.
                        
        yacc_debug:
            Generate a parser.out file that explains how yacc built the parsing
            table from the grammar."""
        self.zwlex    = ZWLexer( error_func=self._lex_error_func )
        self.zwlex.build(
            optimize=lex_optimize, lextab=lextab, debug=lex_debug )
        self.tokens   = self.zwlex.tokens
        self.zwparser = ply.yacc.yacc( module=self, 
                                       debug=yacc_debug,
                                       optimize=yacc_optimize,
                                       tabmodule=yacctab
                        )
    
    def preprocess( self, text ) :
        """The text to be parsed is pre-parsed to remove the fix unwanted
        side effects in the parser.
        Return the preprossed text"""
        # Replace escaped new lines.
        text = re.sub( r'~+\n', '\n', text )
        if text and text[-1] == '~' : 
            text = text[:-1]
        return text

    def parse( self, text, filename='', debuglevel=0 ):
        """Parses C code and returns an AST.
        
        text:
            A string containing the C source code
        
        filename:
            Name of the file being parsed (for meaningful error messages)
        
        debuglevel:
            Debug level to yacc"""
        self.zwlex.filename = filename
        self.zwlex.reset_lineno()
        text += '\n'
        # Pre-process the text.
        text = self.preprocess( text )
        return self.zwparser.parse( text, lexer=self.zwlex, debug=debuglevel )
    
    # ------------------------- Private functions -----------------------------

    def _lex_error_func( self, msg, line, column ):
        self._parse_error( msg, self._coord( line, column ))
    
    def _coord( self, lineno, column=None ):
        return Coord( file=self.zwlex.filename, 
                      line=lineno,
                      column=column
               )
    
    def _parse_error(self, msg, coord):
        raise ParseError("%s: %s" % (coord, msg))

    def _printparse( self, p ) :
        print p[0], "  : ",
        for i in range(1,len(p)) :
            print p[i],
        print

    # ---------- Precedence and associativity of operators --------------------

    precedence = (
        ( 'left', 'PREC_LINK', 'PREC_MACRO', ),
    )
    
    def p_wikipage( self, p ):                          # WikiPage
        """wikipage             : pragmas
                                | pragmas paragraphs
                                | paragraphs"""
        if len(p) == 2 :
            p[0] = Wikipage( p[1] )
        elif len(p) == 3 :
            p[0] = Wikipage( p[1], p[2] )
        else :
            raise ParseError( "unexpected rule-match for wikipage")

    def p_paragraphs( self, p ):                        # Paragraphs
        """paragraphs           : paragraph paragraph_separator
                                | paragraphs paragraph paragraph_separator
                                | paragraph_separator"""
        if len(p) == 2 :
            p[0] = Paragraphs( p[1] )
        elif len(p) == 3 :
            p[0] = Paragraphs( p[1], p[2] )
        elif len(p) == 4 :
            p[0] = Paragraphs( p[1], p[2], p[3] )
        else :
            raise ParseError( "unexpected rule-match for paragraphs")

    def p_paragraph( self, p ):                         # Paragraph
        """paragraph            : nowikiblock
                                | heading
                                | horizontalrule
                                | table_rows
                                | orderedlists
                                | unorderedlists
                                | textlines"""
        p[0] = Paragraph( p[1] )

    def p_pragmas( self, p ):                           # Pragmas
        """pragmas              : OPTIONS NEWLINE
                                | TAGS NEWLINE"""
        p[0] = Pragmas( p[1], p[2] )

    def p_nowiki( self, p ):                            # NoWiki
        """nowikiblock          : NOWIKI_OPEN NEWLINE nowikilines NOWIKI_CLOSE NEWLINE"""
        p[0] = NoWiki( p[2], p[3], p[5] )

    def p_nowikilines( self, p ):
        """nowikilines          : nowikicontent NEWLINE
                                | empty NEWLINE
                                | nowikilines nowikicontent NEWLINE
                                | nowikilines empty NEWLINE"""
        if len(p) == 3 and isinstance( p[1], Empty ):
            p[0] = p[2]
        elif len(p) == 3 :
            p[0] = p[1] + p[2]
        elif len(p) == 4 and isinstance( p[2], Empty ):
            p[0] = p[1] + p[3]
        elif len(p) == 4 :
            p[0] = p[1] + p[2] + p[3]
        else :
            raise ParseError( "unexpected rule-match for nowikilines")

    def p_nowikicontent( self, p ):
        """nowikicontent        : NOWIKI_CHARS
                                | NOWIKI_SPECIALCHAR
                                | nowikicontent NOWIKI_CHARS
                                | nowikicontent NOWIKI_SPECIALCHAR"""
        if len(p) == 2 :
            p[0] = p[1]
        elif len(p) == 3 :
            p[0] = p[1] + p[2]
        else :
            raise ParseError( "unexpected rule-match for nowikicontent")

    def p_heading( self, p ):                           # Heading
        """heading              : HEADING NEWLINE"""
        p[0] = Heading( p[1], p[2] )

    def p_horizontalrule( self, p ):                    # HorizontalRule
        """horizontalrule       : HORIZONTALRULE NEWLINE"""
        p[0] = HorizontalRule( p[1], p[2] )

    def p_textlines( self, p ) :                        # Textlines
        """textlines            : text_contents NEWLINE
                                | textlines text_contents NEWLINE"""
        if len(p) == 3 :
            p[0] = TextLines( p[1], p[2] )
        elif len(p) == 4 and isinstance( p[1], TextLines ) :
            p[1].appendline( p[2], p[3] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for textlines")

    def p_table_rows_1( self, p ):
        """table_rows           : table_cells NEWLINE
                                | table_cells TABLE_CELLSTART NEWLINE
                                | table_rows table_cells NEWLINE
                                | table_rows table_cells TABLE_CELLSTART NEWLINE"""
        if len(p) == 3 and isinstance( p[1], TableCells ):
            p[0] = TableRows( p[1], newline=p[2] )
        elif len(p) == 4 and isinstance( p[1], TableCells ):
            p[0] = TableRows( p[1], p[2], p[3] )
        elif len(p) == 4 and isinstance( p[1], TableRows ) \
                         and isinstance( p[2], TableCells ) :
            p[1].appendrow( p[2], newline=p[3] )
            p[0] = p[1]
        elif len(p) == 5 and isinstance( p[1], TableRows ) \
                         and isinstance( p[2], TableCells ) :
            p[1].appendrow( p[2], p[3], p[4] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for table_rows_1")

    def p_table_rows_2( self, p):
        """table_rows           : TABLE_CELLSTART NEWLINE
                                | table_rows TABLE_CELLSTART NEWLINE"""
        if len(p) == 3 :
            p[0] = TableRows( TableCells( p[1], Empty() ), newline=p[2] )
        elif len(p) == 4 :
            p[1].appendrow( TableCells( p[2], Empty() ), newline=p[3] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for table_rows_2")

    def p_table_cells( self, p ):                       # TableCells
        """table_cells          : TABLE_CELLSTART text_contents
                                | TABLE_CELLSTART empty
                                | table_cells TABLE_CELLSTART empty
                                | table_cells TABLE_CELLSTART text_contents"""
        if len(p) == 3 and isinstance( p[2], Empty ) :
            p[0] = TableCells( p[1], p[2] )
        elif len(p) == 3 :
            p[0] = TableCells( p[1], p[2] )
        elif len(p) == 4 and isinstance( p[3], Empty ) :
            p[1].appendcell( p[2], p[3] )
            p[0] = p[1]
        elif len(p) == 4 :
            p[1].appendcell( p[2], p[3] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for table_cells")

    def p_orderedlists( self, p ):                      # Lists
        """orderedlists : orderedlist
                        | orderedlists orderedlist"""
        if len(p) == 2 and isinstance( p[1], List ) :
            p[0] = Lists( p[1] )
        elif len(p) == 3 and isinstance( p[1], Lists ) \
                         and isinstance( p[2], List ) :
            p[1].appendlist( p[2] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for orderedlists")

    def p_orderedlist( self, p ):                       # List
        """orderedlist : ORDLIST_START text_contents NEWLINE
                       | ORDLIST_START empty NEWLINE"""
        p[0] = List( LIST_ORDERED, p[1], p[2], p[3] )

    def p_unorderedlists( self, p ):                    # Lists
        """unorderedlists       : unorderedlist
                                | unorderedlists unorderedlist"""
        if len(p) == 2 and isinstance( p[1], List ) :
            p[0] = Lists( p[1] )
        elif len(p) == 3 and isinstance( p[1], Lists ) \
                         and isinstance( p[2], List ):
            p[1].appendlist( p[2] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for unorderedlists")

    def p_unorderedlist( self, p ):                     # List
        """unorderedlist        : UNORDLIST_START text_contents NEWLINE
                                | UNORDLIST_START empty NEWLINE"""
        p[0] = List( LIST_UNORDERED, p[1], p[2], p[3] )

    def p_text_contents( self, p ) :                    # TextContents
        """text_contents        : basictext
                                | link
                                | macro
                                | text_contents basictext
                                | text_contents link
                                | text_contents macro"""
        if len(p) == 2 and isinstance( p[1], (Link,Macro,BasicText) ):
            p[0] = TextContents( p[1] ) 
        elif len(p) == 3 and isinstance( p[1], TextContents ) \
                         and isinstance( p[2], (Link,Macro,BasicText) ) :
            p[1].appendcontent( p[2] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for text_contents")

    def p_link( self, p ):                              # Link
        """link                 : LINK %prec PREC_LINK"""
        p[0] = Link( p[1] )

    def p_macro( self, p ):                             # Macro
        """macro                : MACRO %prec PREC_MACRO"""
        p[0] = Macro( p[1] )

    def p_basictext_1( self, p ):
        """basictext            : PIPE"""
        p[0] = BasicText( TEXT_ZWCHARPIPE, p[1] )

    def p_basictext_2( self, p ):
        """basictext            : ALPHANUM"""
        p[0] = BasicText( TEXT_ALPHANUM, p[1] )

    def p_basictext_3( self, p ):
        """basictext            : SPECIALCHAR
                                | SQR_OPEN
                                | SQR_CLOSE
                                | PARAN_OPEN
                                | PARAN_CLOSE"""
        p[0] = BasicText( TEXT_SPECIALCHAR, p[1] )

    def p_basictext_4( self, p ):
        """basictext            : HTTP_URI"""
        p[0] = BasicText( TEXT_HTTPURI, p[1] )

    def p_basictext_5( self, p ):
        """basictext            : WWW_URI"""
        p[0] = BasicText( TEXT_WWWURI, p[1] )

    def p_basictext_6( self, p ):
        """basictext            : ESCAPED"""
        p[0] = BasicText( TEXT_ESCAPED, p[1] )

    def p_paragraph_seperator( self, p ):                   # ParagraphSeparator
        """paragraph_separator  : NEWLINE
                                | paragraph_separator NEWLINE
                                | empty"""
        if len(p) == 2 :
            p[0] = ParagraphSeparator( p[1] ) 
        elif len(p) == 3 :
            p[0] = ParagraphSeparator( p[1], p[2] ) 
        else :
            raise ParseError( "unexpected rule-match for paragraph_separator" )

    def p_empty( self, p ):
        'empty : '
        p[0] = Empty()
        
    def p_error( self, p ):
        column = self.zwlex._find_tok_column( p )
        if p:
            self._parse_error( 'before: %s ' % p.value, self._coord(p.lineno, column) )
        else:
            self._parse_error( 'At end of input', '' )


if __name__ == "__main__":
    import pprint
    import time
    
    t1     = time.time()
    parser = ZWParser( lex_optimize=True, yacc_debug=True, yacc_optimize=False )
    print time.time() - t1
    
    buf = ''' 
        int (*k)(int);
    '''
    
    # set debuglevel to 2 for debugging
    t = parser.parse( buf, 'x.c', debuglevel=0 )
    t.show( showcoord=True )
