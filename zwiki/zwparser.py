"""Module containing the parser for ZWiki"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#
#   ( Testing )
#
#   * Unit test case for the following function,
#       split_style()
#   * All the macros, zwext and ZWParser should be tested for style.
#   * Add test cases for extensions.
#   * Test case for escaping new lines as '\\n'
#
#   ( features - core )
#
#   * Links,
#       * Shortcuts for image links (that would otherwise require the image
#         macro )
#       * Shortcuts for image macro
#   * Provide support for media wiki like table markup.
#       {| styles
#       | cell-content
#       |+ caption
#       |-
#       | styles | cell-content
#   * Support merging table cells like (refer wiki-dot).
#   * Provision for creating templates using properties. These templates can
#     be pulled.
#     All macros and extensions should accept css properties as keyword
#     arguments. To define a standard styling template for a wiki page.
#     add a property name `[macro|extension]style` in the wikipage property.
#     This is called style templating.
#   * Backlinks, Pingbacks (Linkbacks )
#   * Hide email-address feature.
#   * Meta tagging support.
#   * Printable pages.
#   * Should we add the concept of variables and namespace ?
#
#   ( features - macros )
#
#   * User addable title for Toc macro. And make it closable.
#   * For Toc() macro add numbering feature.
#   * Image Macro. Supporting integration with external links / sites.
#   * Image Gallery (refer wiki-dot for more info).
#   * Notes Macro
#   * Math Macro (and extensions).
#   * Footnote macro.
#   * Bibliography macro.
#   * How long ago Macro.
#   * Include macro to include pages from another wiki page.
#
#   ( features - extensions )
#
#   * Collapsible page contents, using zwextensions.
#   * Code zwextensions.
#   * Math zwextensions (and  macros).
#   * Tab viewing wiki contents.
#   * Mako to be integrated with zwiki as an extension.
#
#   ( features - zeta )
#
#   * Zeta tagging support.
#   * Zeta Attachment support.
#   * Links,
#       * Zetalinks
#
#
#   * Explore the possible addition of `indentation` feature, like,
#       :some text          < one level indentation >
#       ::some text         < two level indentation >
#      while the indentation offset is configurable in the wiki style.
#      NOTE : indentation is not a feature of html. But can/should be achieved
#             via CSS
#
# Other features,
#   * Automatic intrasite-user, intersite-project, intrasite-wiki linking.
#   * Automatic intrasite-user, intersite-project, intersite-wiki linking.
#   * Social bookmarking.
#   * Flash support.
#   * Check out http://meta.wikimedia.org/wiki/Help:Variable and add them as
#     macros
#   * When an ENDMARKER is detected by any grammar other than `wikipage`, it
#     can be indicated to the user, via translated HTML.


import re
import sys
from   types    import StringType

import ply.yacc

from   zwiki.zwlexer  import ZWLexer
from   zwiki.zwast    import *
from   zwiki          import escape_htmlchars, split_style

html_chars = [ '"', "'", '&', '<', '>' ]
ENDMARKER  = '<{<{}>}>'

# Default Wiki page properties
wiki_css = {
    'white-space' : 'normal'
}

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
                    app=None,
                    style=None,
                    lex_optimize=False,
                    lextab='zwiki.lextab',
                    lex_debug=False,
                    yacc_optimize=False,
                    yacctab='zwiki.yacctab',
                    yacc_debug=False,
                ):
        """Create a new ZWParser.
        
        Some arguments for controlling the debug/optimization level of the
        parser are provided. The defaults are tuned for release/performance
        mode.
           
        The simple rules for using them are:
            *) When tweaking ZWParser/ZWLexer, set these to False
            *) When releasing a stable parser, set to True

        app:
            Application object that provides the standard objects to be used
            by ZWiki.
                name    should indicate the application name. Supported
                        applications are,
                            'zeta'
            For more information refer to the ZWiki documentation.

        style:
            A dictionary containing CSS styling properties. When available,
            it will be used instead of the default `wiki_css` property.
            
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
        self.app      = app
        self.zwlex    = ZWLexer( error_func=self._lex_error_func )
        self.zwlex.build(optimize=lex_optimize, lextab=lextab, debug=lex_debug)
        self.tokens   = self.zwlex.tokens
        self.parser   = ply.yacc.yacc( module=self, 
                                       debug=yacc_debug,
                                       optimize=yacc_optimize,
                                       tabmodule=yacctab
                        )
        self.parser.zwparser = self
        self.style    = style
        self.debug    = lex_debug or yacc_debug
    
    def is_matchinghtml( self, text ) :
        """Check whether html special characters are present in the document."""
        return [ ch for ch in html_chars if ch in text ]

    def wiki_preprocess( self, text ) :
        """The text to be parsed is pre-parsed to remove the fix unwanted
        side effects in the parser.
        Return the preprossed text"""
        # Replace `~ ESCAPEd new lines`.
        text = re.compile( r'~+\n', re.MULTILINE | re.UNICODE ).sub('\n', text)
        text = text.rstrip( '~' )   # Remove trailing ESCAPE char
        # Replace `\ ESCAPEd new lines'.
        text = text.replace( '\\\n', '' )
        return text

    def _wiki_properties( self, text ) :
        """Parse the wiki properties"""
        props = []
        textlines = text.split('\n')
        for i in range(len( textlines )) :
            if len( textlines[i] ) and textlines[i][0] == '@' :
                props.append( textlines[i][1:] )
                continue
            break;
        text = '\n'.join( textlines[i:] )
        try :
            props = eval( ''.join( props ) )
        except :
            props = {}
        return props, text

    def parse( self, text, filename='', debuglevel=0 ):
        """Parses C code and returns an AST.
        
        text:
            A string containing the Wiki text
        
        filename:
            Name of the file being parsed (for meaningful error messages)
        
        debuglevel:
            Debug level to yacc"""

        # Initialize
        self.zwlex.filename = filename
        self.zwlex.reset_lineno()
        self.redirect     = None
        self.text         = text
        self.wiki_css     = {}
        self.macroobjects = []  # ZWMacro objects detected while parsing
        self.zwextobjects = []  # ZWExtension objects detected while parsing
        self.predivs      = []  # <div> elements prepend before wikipage
        self.postdivs     = []  # <div> elements append after wikipage

        d_style, s_style = split_style( self.style )
        d_style and self.wiki_css.update( d_style )
        self.style       = s_style or ''
        if not d_style and not s_style :
            self.wiki_css.update( wiki_css )

        props, text      = self._wiki_properties( text )
        d_style, s_style = split_style( props )
        d_style and self.wiki_css.update( d_style )
        if s_style :
            self.style += '; ' + s_style + '; '

        # Pre-process the text.
        self.pptext = self.wiki_preprocess( text )

        # parse and get the Translation Unit
        self.pptext += '\n' + ENDMARKER
        self.tu = self.parser.parse( self.pptext,
                                     lexer=self.zwlex, debug=debuglevel )
        return self.tu

    # ---------------------- Interfacing with Core ----------------------

    def regmacro( self, macroobject ) :
        """Register the Macro node with the parser, so that pre and post html
        processing can be done."""
        self.macroobjects.append( macroobject )

    def onprehtml_macro( self ) :
        """Before tohtml() method is called on the Node tree, all the
        registered macroobject's on_prehtml() method will be called."""
        [ m.on_prehtml() for m in self.macroobjects ]
        
    def onposthtml_macro( self ) :
        """After tohtml() method is called on the Node tree, all the
        registered macroobject's on_posthtml() method will be called."""
        [ m.on_posthtml() for m in self.macroobjects ]

    # ---------------------- Interfacing with Extension Core ------------------

    def regzwext( self, zwextobject ) :
        """Register the NoWiki node with the parser, so that pre and post html
        processing can be done."""
        self.zwextobjects.append( zwextobject )
    
    def onprehtml_zwext( self ) :
        """Before tohtml() method is called on the Node tree, all the
        registered zwextobject's on_prehtml() method will be called."""
        [ zwe.on_prehtml() for zwe in self.zwextobjects ]
        
    def onposthtml_zwext( self ) :
        """After tohtml() method is called on the Node tree, all the
        registered zwextobject's on_posthtml() method will be called."""
        [ zwe.on_posthtml() for zwe in self.zwextobjects ]

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
        ( 'left', 'PREC_LINK', 'PREC_MACRO', 'PREC_HTML' ),
    )
    
    def p_wikipage( self, p ):                          # WikiPage
        """wikipage             : paragraphs
                                | paragraphs ENDMARKER"""
        if len(p) == 2 :
            p[0] = Wikipage( p.parser, p[1] )
        elif len(p) == 3 :
            p[0] = Wikipage( p.parser, p[1] )
        else :
            raise ParseError( "unexpected rule-match for wikipage")

    def p_paragraphs( self, p ):                        # Paragraphs
        """paragraphs           : paragraph paragraph_separator
                                | paragraphs paragraph paragraph_separator
                                | paragraph_separator"""
        if len(p) == 2 :
            p[0] = Paragraphs( p.parser, p[1] )
        elif len(p) == 3 :
            p[0] = Paragraphs( p.parser, p[1], p[2] )
        elif len(p) == 4 :
            p[0] = Paragraphs( p.parser, p[1], p[2], p[3] )
        else :
            raise ParseError( "unexpected rule-match for paragraphs")

    def p_paragraph( self, p ):                         # Paragraph
        """paragraph            : nowikiblock
                                | heading
                                | horizontalrule
                                | table_rows
                                | orderedlists
                                | unorderedlists
                                | definitionlists
                                | blockquotes
                                | textlines"""
        p[0] = Paragraph( p.parser, p[1] )

    def p_nowiki( self, p ):                            # NoWiki
        """nowikiblock          : NOWIKI_OPEN NEWLINE nowikilines NOWIKI_CLOSE NEWLINE
                                | NOWIKI_OPEN NEWLINE nowikilines ENDMARKER"""
        if len(p) == 6 :
            p[0] = NoWiki( p.parser, p[1], p[2], p[3], p[4], p[5] )
        elif len(p) == 5 : 
            p[0] = NoWiki( p.parser, p[1], p[2], p[3], p[4], skip=True )

    def p_nowikilines( self, p ):
        """nowikilines          : empty
                                | NEWLINE
                                | nowikicontent NEWLINE
                                | nowikilines NEWLINE
                                | nowikilines nowikicontent NEWLINE"""
        if len(p) == 2 and isinstance( p[1], Empty ):
            p[0] = ''
        elif len(p) == 2 :
            p[0] = p[1]
        elif len(p) == 3 :
            p[0] = p[1] + p[2]
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
        p[0] = Heading( p.parser, p[1], p[2] )

    def p_horizontalrule( self, p ):                    # HorizontalRule
        """horizontalrule       : HORIZONTALRULE NEWLINE"""
        p[0] = HorizontalRule( p.parser, p[1], p[2] )

    def p_textlines( self, p ) :                        # Textlines
        """textlines            : text_contents NEWLINE
                                | textlines text_contents NEWLINE"""
        if len(p) == 3 :
            p[0] = TextLines( p.parser, p[1], p[2] )
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
            p[0] = TableRows( p.parser, p[1], newline=p[2] )
        elif len(p) == 4 and isinstance( p[1], TableCells ):
            p[0] = TableRows( p.parser, p[1], p[2], p[3] )
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
            p[0] = TableRows( p.parser,
                              TableCells( p.parser, p[1], Empty( p.parser ) ),
                              newline=p[2]
                            )
        elif len(p) == 4 :
            p[1].appendrow( TableCells( p.parser, p[2], Empty( p.parser ) ),
                            newline=p[3] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for table_rows_2")

    def p_table_cells( self, p ):                       # TableCells
        """table_cells          : TABLE_CELLSTART text_contents
                                | TABLE_CELLSTART empty
                                | table_cells TABLE_CELLSTART empty
                                | table_cells TABLE_CELLSTART text_contents"""
        if len(p) == 3 and isinstance( p[2], Empty ) :
            p[0] = TableCells( p.parser, p[1], p[2] )
        elif len(p) == 3 :
            p[0] = TableCells( p.parser, p[1], p[2] )
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
            p[0] = Lists( p.parser, p[1] )
        elif len(p) == 3 and isinstance( p[1], Lists ) \
                         and isinstance( p[2], List ) :
            p[1].appendlist( p[2] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for orderedlists")

    def p_orderedlist( self, p ):                       # List
        """orderedlist : ORDLIST_START text_contents NEWLINE
                       | ORDLIST_START empty NEWLINE"""
        p[0] = List( p.parser, LIST_ORDERED, p[1], p[2], p[3] )

    def p_unorderedlists( self, p ):                    # Lists
        """unorderedlists       : unorderedlist
                                | unorderedlists unorderedlist"""
        if len(p) == 2 and isinstance( p[1], List ) :
            p[0] = Lists( p.parser, p[1] )
        elif len(p) == 3 and isinstance( p[1], Lists ) \
                         and isinstance( p[2], List ):
            p[1].appendlist( p[2] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for unorderedlists")

    def p_unorderedlist( self, p ):                     # List
        """unorderedlist        : UNORDLIST_START text_contents NEWLINE
                                | UNORDLIST_START empty NEWLINE"""
        p[0] = List( p.parser, LIST_UNORDERED, p[1], p[2], p[3] )

    def p_definitionlists( self, p ):                    # Definitions
        """definitionlists      : definitionlist
                                | definitionlists definitionlist"""
        if len(p) == 2 and isinstance( p[1], Definition ) :
            p[0] = Definitions( p.parser, p[1] )
        elif len(p) == 3 and isinstance( p[1], Definitions ) \
                         and isinstance( p[2], Definition ):
            p[1].appendlist( p[2] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for definitionlists")

    def p_definitionlist( self, p ):                     # Definition
        """definitionlist       : DEFINITION_START text_contents NEWLINE
                                | DEFINITION_START empty NEWLINE"""
        p[0] = Definition( p.parser, p[1], p[2], p[3] )

    def p_blockquotes( self, p ):                       # BQuotes
        """blockquotes          : blockquote
                                | blockquotes blockquote"""
        if len(p) == 2 and isinstance( p[1], BQuote ) :
            p[0] = BQuotes( p.parser, p[1] )
        elif len(p) == 3 and isinstance( p[1], BQuotes ) \
                         and isinstance( p[2], BQuote ):
            p[1].appendlist( p[2] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for blockquotes")

    def p_blockquote( self, p ):                        # BQuote
        """blockquote           : BQUOTE_START text_contents NEWLINE
                                | BQUOTE_START empty NEWLINE"""
        p[0] = BQuote( p.parser, p[1], p[2], p[3] )

    def p_text_contents( self, p ) :                    # TextContents
        """text_contents        : basictext
                                | link
                                | macro
                                | html
                                | text_contents basictext
                                | text_contents link
                                | text_contents macro
                                | text_contents html"""
        if len(p) == 2 and isinstance( p[1], (Link,Macro,Html,BasicText) ):
            p[0] = TextContents( p.parser, p[1] ) 
        elif len(p) == 3 and isinstance( p[1], TextContents ) \
                         and isinstance( p[2], (Link,Macro,Html,BasicText) ) :
            p[1].appendcontent( p[2] )
            p[0] = p[1]
        else :
            raise ParseError( "unexpected rule-match for text_contents")

    def p_link( self, p ):                              # Link
        """link                 : LINK %prec PREC_LINK"""
        p[0] = Link( p.parser, p[1] )

    def p_macro( self, p ):                             # Macro
        """macro                : MACRO %prec PREC_MACRO"""
        p[0] = Macro( p.parser, p[1] )

    def p_html( self, p ):                             # Html
        """html                 : HTML %prec PREC_HTML"""
        p[0] = Html( p.parser, p[1] )

    def p_basictext_1( self, p ):
        """basictext            : PIPE"""
        p[0] = BasicText( p.parser, TEXT_ZWCHARPIPE, p[1] )

    def p_basictext_2( self, p ):
        """basictext            : ALPHANUM"""
        p[0] = BasicText( p.parser, TEXT_ALPHANUM, p[1] )

    def p_basictext_3( self, p ):
        """basictext            : SPECIALCHAR
                                | SQR_OPEN
                                | SQR_CLOSE
                                | PARAN_OPEN
                                | PARAN_CLOSE
                                | ANGLE_OPEN
                                | ANGLE_CLOSE"""
        p[0] = BasicText( p.parser, TEXT_SPECIALCHAR, p[1] )

    def p_basictext_4( self, p ):
        """basictext            : HTTP_URI"""
        p[0] = BasicText( p.parser, TEXT_HTTPURI, p[1] )

    def p_basictext_5( self, p ):
        """basictext            : WWW_URI"""
        p[0] = BasicText( p.parser, TEXT_WWWURI, p[1] )

    def p_basictext_6( self, p ):
        """basictext            : ESCAPED"""
        p[0] = BasicText( p.parser, TEXT_ESCAPED, p[1] )

    def p_paragraph_seperator( self, p ):                   # ParagraphSeparator
        """paragraph_separator  : NEWLINE
                                | paragraph_separator NEWLINE
                                | empty"""
        if len(p) == 2 :
            p[0] = ParagraphSeparator( p.parser, p[1] ) 
        elif len(p) == 3 :
            p[0] = ParagraphSeparator( p.parser, p[1], p[2] ) 
        else :
            raise ParseError( "unexpected rule-match for paragraph_separator" )

    def p_empty( self, p ):
        'empty : '
        p[0] = Empty( p.parser )
        
    def p_error( self, p ):
        if p:
            column = self.zwlex._find_tok_column( p )
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
