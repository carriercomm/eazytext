# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Module containing Node definition for all non-teminals and translator
functions for translating the text to HTML.

The AST tree is constructed according to the grammar. From the root
non-terminal use the children() method on every node to walk through the tree,
the only exceptions are,
  * `nowikilines` and `nowikicontent` rules are not available, in the AST
    tree.
  * `basictext`, though is a non-terminal with many alternative terminals,
  * does not differentiate it.

To walk throug the AST,
  * parse() the text, which returns the root non-terminal
  * Use children() method on every non-terminal node.
  * Use _terms and _nonterms attribute to get lists of terminals and
    non-terminals for every node.
"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#   1. Add unicode support
#   2. Add ismatched() method.
#   3. For links that open in new window, append a character that would say
#      so.
#   4. Remove old Textlexer based parsing.

import sys
import re
from   random       import randint
from   os.path      import basename, abspath, dirname, join, isdir, isfile
import types

from   eazytext.macro        import build_macro
from   eazytext.extension    import build_ext
from   eazytext              import escape_htmlchars, split_style, \
                                    obfuscatemail, lhtml
from   eazytext.stylelookup  import styleparser 
import eazytext.ttags        as tt

# text type for BasicText, note that non-markup text must begin with 1000
TEXT_TOKEN               = 1000
TEXT_CHARPIPE            = 1001    #'charpipe'
TEXT_ALPHANUM            = 1002    #'alphanum'
TEXT_SPECIALCHAR         = 1003    #'specialchar'
TEXT_SPECIALCHAR_LB      = 1004    #'linebreak'
TEXT_HTTPURI             = 1005    #'httpuri'
TEXT_WWWURI              = 1006    #'wwwuri'
TEXT_ESCAPED             = 1007    #'escaped'
TEXT_LINK                = 1008    #'link'
TEXT_MACRO               = 1009    #'macro'
TEXT_HTML                = 1010    #'html'
TEXT_NEWLINE             = 1011    #'newline'
# text type for BasicText, note that markup text must begin with 2000
TEXT_MARKUP              = 1000
TEXT_M_SPAN                = 2001  #'m_span'
TEXT_M_BOLD                = 2002  #'m_bold'
TEXT_M_ITALIC              = 2003  #'m_italic'
TEXT_M_UNDERLINE           = 2004  #'m_underline'
TEXT_M_SUBSCRIPT           = 2005  #'m_subscript'
TEXT_M_SUPERSCRIPT         = 2006  #'m_superscript'
TEXT_M_BOLDITALIC          = 2007  #'m_bolditalic'
TEXT_M_BOLDUNDERLINE       = 2008  #'m_boldunderline'
TEXT_M_ITALICUNDERLINE     = 2009  #'m_italicunderline'
TEXT_M_BOLDITALICUNDERLINE = 2010  #'m_bolditalicunderline'

# List Type
LIST_ORDERED        = 'ordered'
LIST_UNORDERED      = 'unordered'

# Markup
M_PIPE              = '|'
M_PIPEHEAD          = '|='

FORMAT_NON          = 'fmt_non'
FORMAT_EMPTY        = 'fmt_empty'
FORMAT_BTABLE       = 'fmt_bt'
FORMAT_BTABLESTYLE  = 'fmt_btstyle'

templtdir = join( dirname(__file__), 'templates' )

html_templates = {
    TEXT_M_SPAN : [
        '<span class="etmark" style="%s">',
        '</span>', ],
    TEXT_M_BOLD : [
        '<strong class="etmark" style="%s">',
        '</strong>', ],
    TEXT_M_ITALIC : [
        '<em class="etmark" style="%s">',
        '</em>', ],
    TEXT_M_UNDERLINE : [
        '<u class="etmark" style="%s">',
        '</u>', ],
    TEXT_M_SUPERSCRIPT : [
        '<sup class="etmark" style="%s">',
        '</sup>', ],
    TEXT_M_SUBSCRIPT : [
        '<sub class="etmark" style="%s">',
        '</sub>', ],
    TEXT_M_BOLDITALIC : [
        '<strong class="etmark" style="%s"><em class="etmark">',
        '</em></strong>', ],
    TEXT_M_BOLDUNDERLINE : [
        '<strong class="etmark" style="%s"><u class="etmark">',
        '</u></strong>', ],
    TEXT_M_ITALICUNDERLINE : [
        '<em class="etmark" style="%s"><u class="etmark">',
        '</u></em>', ],
    TEXT_M_BOLDITALICUNDERLINE : [
    '<strong class="etmark" style="%s"><em class="etmark"><u class="etmark">',
    '</u></em></strong>' ]
}
def markup2html( type_, mtext, steed ) :
    if steed == 0 :
        return html_templates[type_][0] % styleparser( mtext[2:] )
    else :
        return html_templates[type_][1]

class ASTError( Exception ):
    pass

class Content( object ) :
    """The whole of wiki text is parsed and encapulated as lists of Content
    objects."""
    def __init__( self, parser, text, type=None, html=None ) :
        self.parser = parser
        self.text   = text
        self.type   = type
        self._html  = html

    def _gethtml( self ) :
        attr = self._html
        return attr() if hasattr(attr, '__call__') else attr

    def _sethtml( self, value ) :
        self._html = value

    def __repr__( self ) :
        return "Content<'%s','%s','%s'>" % (self.text, self.type, self.html )

    html = property( _gethtml, _sethtml )

def process_textcontent( contents ) :
    """From the list of content objects (tokenized), construct the html
    page."""
    count = len(contents)
    for i in range( count ) :
        beginmarkup_cont = contents[i]
        if beginmarkup_cont.html or \
           ( TEXT_TOKEN < beginmarkup_cont.type < TEXT_MARKUP ) :
            continue
        for j in range( i+1, count ) :
            endmarkup_cont = contents[j]
            if (endmarkup_cont.type == beginmarkup_cont.type) and (j != i+1)  :
                # Found the markup pair, with some text in between
                beginmarkup_cont.html = markup2html( beginmarkup_cont.type,
                                                     beginmarkup_cont.text,
                                                     0
                                                   )
                endmarkup_cont.html   = markup2html( endmarkup_cont.type,
                                                     endmarkup_cont.text,
                                                     1
                                                   )
                # All the markups in between should be self contained between
                # i and j
                process_textcontent( contents[i+1:j] )
                break;
        else :
            beginmarkup_cont.html = beginmarkup_cont.text

    return

# ------------------- AST Nodes (Terminal and Non-Terminal) -------------------

class Terminal( object ) :
    """Abstract base class for EazyText AST terminal nodes."""

    def __init__( self, parser, terminal='', **kwargs ) :
        self.parser = parser
        self.terminal = terminal
        [ setattr( self, k, v ) for k,v in kwargs.items() ]

    def children( self ) :
        """Empty tuple of children"""
        return tuple()

    def tohtml( self ):
        """Translate the node and all the children nodes to html markup and
        return the content"""
        return self.terminal

    def ismatched( self ) :
        """This interface should return a boolean indicating whether the html
        generated by this node is matched. If a node expects that the html
        might be mismatched.
        After replacing etree with lxml mismatched elements are automatically
        taken care."""
        return True

    def dump( self ):
        """Simply dump the contents of this node and its children node and
        return the same."""
        return self.terminal

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        """ Pretty print the Node and all its attributes and children
        (recursively) to a buffer.
            
        file:   
            Open IO buffer into which the Node is printed.
        
        offset: 
            Initial offset (amount of leading spaces) 
        
        attrnames:
            True if you want to see the attribute names in name=value pairs.
            False to only see the values.
        
        showcoord:
            Do you want the coordinates of each Node to be displayed.
        """
        lead = ' ' * offset
        buf.write(lead + '<%s>: %r' % (self.__class__.__name__, self.terminal))
        buf.write('\n')


class Node( object ):       # Non-terminal
    """Abstract base class for EazyText AST non-terminalnodes."""

    def children( self ):
        """List of all child nodes of type ``Nodes``"""
        pass

    def tohtml( self ):
        """Translate the node and all the children nodes to html markup and
        return the content"""

    def ismatched( self ) :
        """This interface should return a boolean indicating whether the html
        generated by this node is matched. If a node expects that the html
        might be mismatched.
        After replacing etree with lxml mismatched elements are automatically
        taken care."""
        return True

    def dump( self ):
        """Simply dump the contents of this node and its children node and
        return the same."""

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        """ Pretty print the Node and all its attributes and children
        (recursively) to a buffer.
            
        file:   
            Open IO buffer into which the Node is printed.
        
        offset: 
            Initial offset (amount of leading spaces) 
        
        attrnames:
            True if you want to see the attribute names in name=value pairs.
            False to only see the values.
        
        showcoord:
            Do you want the coordinates of each Node to be displayed."""
        pass

    def terminals( self ) :
        """Return a list of terminal nodes"""
        return getattr( self, '_terms', [] )

    def non_terminals( self ) :
        """Return a list of non-terminal nodes"""
        return getattr( self, '_nonterms', [] )

    def _multiline_contents( self, lines=None, contents=None, html=False ) :
        # Process wiki text content spanning across multiple `lines`
        lines = [] if lines==None else lines
        contents = [] if contents == None else contents
        [ contents.extend( textcontents.listcontents(contents=[]) )
          for textcontents, nl in lines
          if isinstance(textcontents, TextContents)
        ]
        process_textcontent( contents )
        # Translate to html content.
        if html :
            html = ''.join([
                textcontents.tohtml()+nl.tohtml() for textcontents, nl in lines
            ])
            return html
        else :
            return None


# ------------------- Non-terminal classes ------------------------

class Wikipage( Node ):
    """class to handle `wikipage` grammar."""

    # Class etpage or etblk
    template = """<div class="%s" style="%s">
                    %s
                    %s
                    %s
                    %s
                </div>"""

    def __init__( self, parser, paragraphs ) :
        self.parser     = parser
        self.paragraphs = paragraphs
        # terminals and non-terminals
        self._terms = []
        self._nonterms = [ self.paragraphs ]

    def children( self ) :
        return tuple(self._nonterms)

    def tohtml( self ):
        etparser = self.parser.etparser
        # Call the registered prehtml methods.
        etparser.onprehtml_macro()
        etparser.onprehtml_ext()
        # Generate HTML from childrens
        etparser.html  = ''.join([ c.tohtml() for c in self.children() ])
        # Call the registered posthtml methods.
        etparser.onposthtml_macro()
        etparser.onposthtml_ext()

        # Sort prehtmls and posthtmls based on the weight
        allhtmls = sorted( etparser.prehtmls + etparser.posthtmls,
                           key=lambda x : x[0] )
        prehtmls = filter( lambda x : x[0] < 0, allhtmls )
        posthtmls = filter( lambda x : x[0] >= 0, allhtmls )

        # Join them together
        prehtmls = ''.join( map( lambda x : x[1], prehtmls ))
        posthtmls = ''.join( map( lambda x : x[1], posthtmls ))

        # Final html
        skin = '' if etparser.skin == None else etparser.skin
        etparser.html = self.template % (
                            'etblk' if etparser.nested else 'etpage',
                            etparser.styleattr,
                            '' if etparser.nested else skin,
                            prehtmls,
                            etparser.html,
                            posthtmls
                        )
        return etparser.html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        # Show this non-terminal
        lead = ' ' * offset
        buf.write( lead + '-->wikipage: ' )
        # Show co-ordinates
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        # Show children
        [ c.show(buf, offset+5, attrnames, showcoord) for c in self.children() ]


class Paragraphs( Node ) :
    """class to handle `paragraphs` grammar."""

    template = None

    def __init__( self, parser, *args  ) :
        self.parser = parser
        self.paragraphs = self.paragraph = self.paragraph_separator = None
        if len( args ) == 1 :
            self.paragraph_separator = args[0]
        elif len( args ) == 2 :
            self.paragraph = args[0]
            self.paragraph_separator = args[1]
        elif len( args ) == 3 :
            self.paragraphs = args[0]
            self.paragraph = args[1]
            self.paragraph_separator = args[2]
        # terminals and non-terminals
        self._terms = []
        self._nonterms = args

    def children( self ) :
        return tuple(self._nonterms)

    def tohtml( self ):
        return ''.join([ c.tohtml() for c in self.children() ])

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        [ c.show(buf, offset, attrnames, showcoord) for c in self.children() ]


class Paragraph( Node ) :
    """class to handle `paragraph` grammar."""

    template = None

    def __init__( self, parser, paragraph ) :
        self.parser = parser
        self.paragraph = paragraph
        # terminals and non-terminals
        self._terms = []
        self._nonterms = [self.paragraph]

    def children( self ) :
        return tuple(self._nonterms)

    def tohtml( self ):
        return ''.join([ c.tohtml() for c in self.children() ])

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write(lead + 'paragraph: ')
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]


class NoWiki( Node ) :
    """class to handle `nowikiblock` grammar."""
    def __init__( self, parser, opennowiki, opennl, nowikilines,
                  closenowiki=None, closenl=None, skip=False  ) :
        self.parser, self.skip = parser, skip
        self.xparams = xparams = filter(
            None,
            [ x.strip(' \t') for x in opennowiki[3:].strip( ' \t' ).split(' ') ]
        )
        self.xwikiname = xparams and xparams.pop(0) or ''
        self.opennowiki = NOWIKI_OPEN( parser, opennowiki )
        self.opennewline = NEWLINE( parser, opennl )
        self.nowikilines = NOWIKILINES( parser, nowikilines )
        if self.skip :
            self.closenowiki = EMPTY( parser )
            self.closenewline = EMPTY( parser )
        else :
            self.closenowiki = NOWIKI_CLOSE( parser, closenowiki )
            self.closenewline = NEWLINE( parser, closenl )
            self.wikixobject = build_ext( self, nowikilines )
        self.text = self.dump()
        # terminals and non-terminals
        self._terms = [ self.opennowiki, self.opennewline, self.nowikilines,
                        self.closenowiki, self.closenewline ]
        self._nonterms = []

    def children( self ) :
        return ( self.opennowiki, self.opennewline, self.nowikilines,
                 self.closenowiki, self.closenewline )

    def tohtml( self ):
        html = '' if self.skip else self.wikixobject.tohtml()
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        line = self.text.split('\n')
        text = line[0][:20] if line else ''
        buf.write( lead + "nowikiblock: '%s ...'" % text )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class Heading( Node ) :
    """class to handle `heading` grammar."""

    template = """
    <h%s class="etsec" style="%s">
      %s
      <a name="%s"></a>
      <a class="etseclink" href="#%s" title="Link to this section">&#9875;</a>
    </h%s>
    """
    def _parsemarkup( self, markup ) :
        """Convert the header markup into respective level. Note that, header
        markup can be specified with as ={1,5} or h[1,2,3,,4,5]"""
        markup = markup.lstrip( ' \t' )
        off = markup.find( '{' )
        if off > 0 :
            markup = markup[:off]
            style = styleparser( markup[off:] )
        else :
            markup = markup
            style = ''

        if '=' in markup :
            level = len(markup)
        elif markup[0] in 'hH' :
            level = int(markup[1])
        else :
            level = 5
        return markup, level, style

    def __init__( self, parser, markup, textcontents, newline ) :
        self.parser = parser
        self.markup = HEADING( parser, markup )
        self.textcontents = textcontents
        self.newline = NEWLINE( parser, newline )
        _markup, self.level, self.style = self._parsemarkup(markup)
        # terminals and non-terminals
        self._terms = [ self.markup, self.newline ]
        self._nonterms = [ self.textcontents ]

    def children( self ) :
        return ( self.markup, self.textcontents, self.newline )

    def tohtml( self ):
        l = self.level
        contents = self.textcontents.listcontents( contents=[] )
        process_textcontent( contents )
        html = self.textcontents.tohtml().strip(' \t=')
        text = ''.join( lhtml.fromstring(html).xpath( '//text()' ) )
        html = self.template % ( l, self.style, html, text, text, l )
        html += self.newline.tohtml()
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'heading: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]


class HorizontalRule( Node ) :
    """class to handle `horizontalrule` grammar."""

    template = '<hr class="ethorz"/>'

    def __init__( self, parser, hrule, newline ) :
        self.parser = parser
        self.hrule = HORIZONTALRULE( parser, hrule )
        self.newline = NEWLINE( parser, newline )
        # terminals and non-terminals
        self._terms = [ self.hrule, self.newline ]
        self._nonterms = []

    def children( self ) :
        return tuple(self._terms)

    def tohtml( self ):
        return self.template

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'horizontalrule:' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]


class TextLines( Node ) :
    """class to handle `textlines` grammar."""

    template = '<p class="ettext"> %s </p>'

    def __init__( self, parser, textlines=None, textcontents=None, newline=None ) :
        self.parser = parser
        self.textlines, self.textcontents = textlines, textcontents
        self.newline = NEWLINE( parser, newline )
        # terminals and non-terminals
        self._terms = [ self.newline ]
        self._nonterms = []
        self.textlines and self._nonterms.append( self.textlines )
        self._nonterms.append( textcontents )

    def children( self ) :
        return tuple(self._nonterms + self._terms)

    def tohtml( self ) :
        # Combine text lines, process the text contents and convert them to html
        lines = self.multilines()
        html = self._multiline_contents( lines=lines, html=True )
        return self.template % html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'textline: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def multilines( self, lines=None ) :
        lines = [] if lines==None else lines
        lines = self.textlines.multilines( lines=lines 
                ) if self.textlines else lines
        lines.append( (self.textcontents, self.newline) )
        return lines


class BtableRows( Node ) :
    """class to handle `btablerows` grammar"""

    tbl_template = '<table class="etbtbl sortable" cellspacing="0px" ' + \
                   ' cellpadding="5px" style="%s">'
    row_template = '  <tr class="etbtbl" style="%s">'
    hdrcell_template = '<th class="etbtbl" style="%s"> %s </th>'
    cell_template = '<td class="etbtbl" style="%s"> %s </td>'

    def __init__( self, parser, row, rows=None ) :
        self.parser = parser
        self.rows = rows
        self.row = row
        # terminals and non-terminals
        self._terms = []
        self._nonterms = []
        self.rows and self._nonterms.append( self.rows )
        self._nonterms.append( self.row )

    def children( self ) :
        return tuple(self._nonterms)

    def tohtml( self ) :
        html, rows = '', self.deeprows( rows=[] )
        closerow   = []     # Stack to manage rows
        closetable = []     # Stack to manage table
        for row in rows :
            mrkup = row.markuptxt().lstrip( ' \t' )[:3]
            style = row.style()
            if mrkup == '||{' :     # open table
                html += self.tbl_template % style
                closetable.append( '</table>' )
            elif mrkup == '||-' :   # Row
                if closerow : html += closerow.pop()
                html += self.row_template % style
                closerow.append( '</tr>' )
            elif mrkup == '||=' :   # header cell
                html += self.hdrcell_template % ( style, row.tohtml() )
            elif mrkup == '|| ' :   # Cell
                html += self.cell_template % ( style, row.tohtml() )
            elif mrkup == '||}' :   # close table
                pass
        html += ''.join( closerow ) if closerow else ''
        html += ''.join( closetable ) if closetable else ''
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'btablerows: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write( '\n' )
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def deeprows( self, rows=None ) :
        rows = [] if rows == None else []
        rows = self.rows.deeprows( rows=rows ) if self.rows else rows
        rows.append( self.row )
        return rows


class BtableRow( Node ) :
    """class to handle `btablerow` grammar"""

    template = None

    def __init__( self, parser, *args ) :
        self.parser = parser
        self.rowstartline = self.row = self.textcontents = self.newline = None
        # terminals and non-terminals
        self._terms = []
        self._nonterms = []
        if len(args) == 1 :
            self.rowstartline = args[0]
            self._nonterms.append( self.rowstartline )
        elif len(args) == 3 :
            self.row, self.textcontents = args[:2]
            self.newline = NEWLINE( parser, args[2] )
            self._terms.append( self.newline )
            self._nonterms.extend([ self.row, self.textcontents ])

    def children( self ) :
        return tuple(self._nonterms + self._terms)

    def tohtml( self ) :
        html = self._multiline_contents( lines=self.rowline(), html=True )
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'btablerow: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write( '\n' )
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def rowline( self, lines=None ) :
        lines = [] if lines==None else lines
        if self.row :
            lines = self.row.rowline( lines=lines )
            lines.append( (self.textcontents, self.newline) )
        elif self.rowstartline :
            lines.append( self.rowstartline.rowline() )
        else :
            raise Exception( "unexpected rule-match for btablerow")
        return lines

    def markuptxt( self ) :
        rs, r = self.rowstartline, self.row
        return rs.markuptxt() if rs else r.markuptxt()

    def style( self ) :
        rs, r = self.rowstartline, self.row
        return rs.style() if rs else r.style()


class BtableRowStartline( Node ) :
    """class to handle `btablerow_start_line` grammar"""

    template = None

    def __init__( self, parser, markup, textcontents, newline,
                  term=None ) :
        self.parser = parser
        if term == FORMAT_BTABLESTYLE :
            self.markup = BTABLE_START( parser, markup )
        elif term == FORMAT_BTABLE :
            self.markup = BTABLESTYLE_START( parser, markup )
        self.textcontents = textcontents if textcontents else EMPTY( parser )
        self.newline = NEWLINE( parser, newline )
        # terminals and non-terminals
        self._terms = [self.markup, self.newline]
        self._nonterms = [self.textcontents]

    def children( self ) :
        return ( self.markup, self.textcontents, self.newline )

    def tohtml( self ) :
        return ''

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'btablerow_start_line: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write( '\n' )
        # Show children
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def rowline( self ) :
        return (self.textcontents, self.newline)

    def markuptxt( self ) :
        return self.markup.dump()

    def style( self ) :
        style = ''
        markup = self.markup.dump()
        if isinstance( markup, BTABLESTYLE_START ) :
            style = markup.lstrip( ' \t' )[3:].lstrip( ' \t' )
            style = styleparser( style.rstrip( '| \t' ) )
        return style


class TableRows( Node ) :
    """class to handle `table_rows` grammar."""
    tbl_template = '<table class="ettbl sortable" cellspacing="0" ' + \
                   'cellpadding="5px"> %s </table>'
    tr_template = '<tr class="ettbl"> %s </tr>'

    def __init__( self, parser, rows=None, cells=None, markup=None,
                  newline=None ) :
        self.parser = parser
        self.rows, self.cells = rows, cells
        # terminals and non-terminals
        self._terms = []
        self._nonterms = []
        if markup :     # `markup` is pipe+style
            self.markup = TABLE_CELLSTART( parser, markup )
            self._terms.append( self.markup )
        if newline :
            self.newline = NEWLINE( parser, newline )
            self._terms.append( self.newline )

    def children( self ) :
        attrs = [ 'rows', 'cells', 'markup', 'newline' ]
        children = [ getattr(self, a) for a in attrs if getattr(self, a, None) ]
        return tuple(children)

    def tohtml( self ) :
        html, rows = '', self.deeprows( rows=[] )
        for cells, newline in rows :
            row = cells.tohtml() + newline.tohtml()
            html += self.tr_template % row
        html = self.tbl_template % html
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'table_rows: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        # Show children
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def deeprows( self, rows=None ) :
        rows = [] if rows == None else rows
        rows = self.rows.deeprows( rows=rows ) if self.rows else rows
        rows.append( (self.cells, self.newline) ) if self.cells else None
        return rows


class TableCells( Node ) :
    """class to handle `table_cells` grammar."""
    RIGHTALIGN = '$'
    hdrcell_template = '<th class="ettbl" colspan="%s" style="%s"> %s </th>'
    cell_template = '<td class="ettbl" colspan="%s" style="%s"> %s </td>'

    def __init__( self, parser, cells=None, markup=None, textcontents=None ) :
        """`cell` can be `Empty` object or `TextContents` object"""
        self.parser = parser
        self.markup = TABLE_CELLSTART( parser, markup ) # `markup` is pipe+style
        self.textcontents = textcontents
        self.cells = cells
        # Magic code to handle empty tables. Touch with care !!
        if isinstance( textcontents, EMPTY ) :
            self.colspan, self.carrycol = 0, 1
            if self.cells :
                self.carrycol += self.cells.carrycol
        else :
            self.carrycol, self.colspan = 0, 1
            if self.cells :
                self.colspan += self.cells.carrycol
        # terminals and non-terminals
        self._terms = [ self.markup ]
        self._nonterms = [self.cells] if self.cells else []
        self._nonterms.append( self.textcontents )

    def children( self ) :
        return ( self.cells, self.markup, self.textcontents
               ) if self.cells else ( self.markup, self.textcontents )

    def tohtml( self ) :
        html = ''
        if self.cells :
            html += self.cells.tohtml()
        # Contents
        if isinstance( self.textcontents, TextContents ) :
            contents = self.textcontents.listcontents( contents=[] )
        if isinstance( self.textcontents, EMPTY ) :
            contents = []
        if contents :
            style, markup = '', self.markup.dump().strip()
            # Handle right-alignemnt markup
            chtml = contents[-1].html
            if chtml and (chtml[-1] == self.RIGHTALIGN) :
                style +=  'text-align : right; '
                contents[-1].html = chtml[:-1]
            # process style and text markups.
            process_textcontent( contents )
            style_, tmpl = (
                styleparser(markup[2:]), self.hdrcell_template 
            ) if markup[:2] == M_PIPEHEAD else (
              styleparser(markup[1:]), self.cell_template
            )
            style += style_
            html += tmpl % ( self.colspan, style, self.textcontents.tohtml() )
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'table_cells: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]


class MixedLists( Node ) :
    """class to handle `orderedlists` and `unorderedlists` grammar."""

    patt = re.compile( r'[\*\#]{1,5}$', re.MULTILINE | re.UNICODE )
    list_styletype = {
        '#' : ['decimal', 'lower-roman', 'lower-alpha'],
        '*' : ['disc', 'disc', 'disc' ]
    }
    template = {
        '#' : ('<ol class="et" style="list-style-type: %s;">', '</ol>'),
        '*' : ('<ul class="et" style="list-style-type: %s;">', '</ul>')
    }

    def __init__( self, parser, mixedlists=None, nlist=None ) :
        self.parser = parser
        self.mixedlists, self.nlist = mixedlists, nlist
        # terminals and non-terminals
        self._terms = []
        self._nonterms = [ self.mixedlists ] if self.mixedlists else []
        self._nonterms.append( self.nlist )

    def children( self ) :
        return tuple(self._nonterms)

    def tohtml( self ) :
        closemarkups = []   # Stack to manage nested list.
        html = pm = cm = ''
        lists = self.deeplists( lists=[] )
        for nlist in lists :
            markup = nlist.markuptxt()
            cm = re.search( self.patt, markup ).group()
            cmpmark = cmp( len(pm), len(cm) )  # -1 or 0 or 1
            diffmark = abs( len(cm) - len(pm))  # 0 to 4
            if cmpmark > 0 :
                # previous list markup (pm) one level deeper, end the list
                html += ''.join([closemarkups.pop() for i in range(diffmark)])
            elif cmpmark < 0 :
                # current list markup (cm) one level deeper, open a new list
                for i in range(diffmark) :
                    style = self.list_styletype[ cm[0] ][ len(markup)%3 ]
                    html += self.template[ cm[0] ][ 0 ] % style
                    closemarkups.append( self.template[cm[0]][1] )
            html += nlist.tohtml()
            pm = cm
        closemarkups.reverse()
        html += ''.join( closemarkups )
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'mixedlists: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def deeplists( self, lists=None ) :
        lists = [] if lists == None else []
        lists = self.mixedlists.deeplists( lists=lists
                ) if self.mixedlists else lists
        lists.append( self.nlist )
        return lists


class List( Node ) :
    """class to handle `orderedlist` and `unorderedlist` grammar."""
    template = '<li class="et" style="%s"> %s </li>'

    def __init__( self, parser, *args ) :
        self.parser = parser
        self.beginlist = self.nlist = self.textcontents = self.newline = None
        # terminals and non-terminals
        self._terms = []
        self._nonterms = []
        if len(args) == 1 :
            self.beginlist = args[0]
            self._nonterms.append( self.beginlist )
        elif len(args) == 3 :
            self.nlist, self.textcontents = args[0], args[1]
            self.newline = NEWLINE( parser, args[2] )
            self._terms.append( self.newline )
            self._nonterms.extend([ self.nlist, self.textcontents ])

    def children( self ) :
        return tuple(self._nonterms + self._terms)

    def tohtml( self ) :
        # Combine text lines, process the text contents and convert them to html
        html = self._multiline_contents( lines=self.listlines(), html=True )
        html = self.template % ( self.style(), html )
        return html


    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'list: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def listlines( self, lines=None ) :
        lines = [] if lines==None else lines
        if self.nlist :
            lines = self.nlist.listlines( lines=lines )
            lines.append( (self.textcontents, self.newline) )
        elif self.beginlist :
            lines.append( self.beginlist.line() )
        else :
            raise Exception( "unexpected rule-match for list")
        return lines

    def style( self ) :
        if self.nlist :
            return self.nlist.style()
        elif self.beginlist :
            return self.beginlist.style()

    def listtype( self ) :
        if self.nlist :
            return self.nlist.listtype()
        elif self.beginlist :
            return self.beginlist.listtype()

    def markuptxt( self ) :
        if self.nlist :
            return self.nlist.markuptxt()
        elif self.beginlist :
            return self.beginlist.markuptxt()


class ListBegin( Node ) :
    """class to handle `orderedlistbegin` and `unorderedlistbegin` grammar."""

    def __init__( self, parser, ltype, markup, textcontents, newline ) :
        self.parser = parser
        self.ltype = ltype
        if ltype == LIST_ORDERED :
            self.markup = ORDLIST_START( parser, markup )
        elif ltype == LIST_UNORDERED :
            self.markup = UNORDLIST_START( parser, markup )
        self.textcontents = textcontents
        self.newline = NEWLINE( parser, newline )
        # terminals and non-terminals
        self._terms = [ self.markup, self.newline ]
        self._nonterms = [ self.textcontents ]

    def children( self ) :
        return ( self.markup, self.textcontents, self.newline )

    def tohtml( self ) :
        return ''

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'listbegin: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def line( self ) :
        return (self.textcontents, self.newline)

    def style( self ) :
        markup = self.markup.dump().strip( ' \t' )
        off = markup.find('{')
        style = off > 0 and styleparser( markup[off:] ) or ''
        return style

    def listtype( self ) :
        return self.ltype

    def markuptxt( self ) :
        return self.markup.dump()


class Definitions( Node ) :
    """class to handle `definitionlists` grammar."""
    template = '<dl class="et"> %s </dl>' 

    def __init__( self, parser, defns=None, defn=None ) :
        self.parser = parser
        self.defns, self.defn = defns, defn
        # terminals and non-terminals
        self._terms = []
        self._nonterms = [ self.defns ] if self.defns else []
        self._nonterms.append( self.defn )

    def children( self ) :
        return tuple(self._nonterms)

    def tohtml( self ) :
        defs = self.deepdefs( defs=[] )
        html = self.template % '\n'.join([ defn.tohtml() for defn in defs ])
        return html

    def dump( self ) :
        defs = self.deepdefs( defs=[] )
        return ''.join([ defn.dump() for defn in defs ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'definitions: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def deepdefs( self, defs=None ) :
        defs = [] if defs == None else defs
        defs = self.defns.deepdefs( defs=defs ) if self.defns else defs
        defs.append( self.defn )
        return defs


class Definition( Node ) :
    """class to handle `definitionlist` grammar."""
    template = '<dt class="et"><b> %s </b></dt> <dd class="et"> %s </dd>'

    def __init__( self, parser, *args ) :
        self.parser = parser
        self.begindef = self.defn = self.textcontents = self.newline = None
        # terminals and non-terminals
        self._terms = []
        self._nonterms = []
        if len(args) == 1 :
            self.begindef = args[0]
            self._nonterms.append( self.begindef )
        elif len(args) == 3 :
            self.defn, self.textcontents = args[0], args[1]
            self.newline = NEWLINE( parser, args[2] )
            self._nonterms.extend( [self.defn, self.textcontents] )
            self._terms.append( self.newline )

    def children( self ) :
        return tuple(self._nonterms + self._terms)

    def tohtml( self ) :
        # Combine text lines, process the text contents and convert them to html
        lines = self.deflines( lines=[] )
        dd = self._multiline_contents( lines=lines, html=True )
        html = self.template % ( escape_htmlchars( self.dt() ), dd )
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'definition: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def deflines( self, lines=None ) :
        lines = [] if lines==None else lines
        if self.defn :
            lines = self.defn.deflines( lines=lines )
            lines.append( (self.textcontents, self.newline) )
        elif self.begindef :
            lines.append( self.begindef.line() )
        else :
            raise Exception( "unexpected rule-match for definition")
        return lines

    def dt( self ) :
        if self.defn :
            return self.defn.dt()
        elif self.begindef :
            return self.begindef.dt()

    def markuptxt( self ) :
        return defn.markuptxt() if self.defn else self.begindef.markuptxt()


class DefinitionBegin( Node ) :
    """class to handle `definitionbegin` grammar."""
    def __init__( self, parser, markup, textcontents, newline ) :
        self.parser = parser
        self.markup = DEFINITION_START( parser, markup )
        self.textcontents = textcontents
        self.newline = NEWLINE( parser, newline )
        # terminals and non-terminals
        self._terms = [ self.markup, self.newline]
        self._nonterms = [ self.textcontents ]

    def children( self ) :
        return ( self.markup, self.textcontents, self.newline )

    def tohtml( self ) :
        return ''

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'definitionbegin: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def line( self ) :
        return (self.textcontents, self.newline)

    def dt( self ) :
        return self.markup.dump().strip( ' \t' )[1:-2]

    def markuptxt( self ) :
        return self.markup.dump()


class BQuotes( Node ) :
    """class to handle `blockquotes` grammar."""
    patt = re.compile( r'[\>]{1,5}$', re.MULTILINE | re.UNICODE )
    template = '<blockquote class="et %s">'

    def __init__( self, parser, bquotes=None, bquote=None ) :
        self.parser = parser
        self.bquotes, self.bquote = bquotes, bquote
        # terminals and non-terminals
        self._terms = []
        self._nonterms = [ self.bquotes ] if bquotes else []
        self._nonterms.append( self.bquote )

    def children( self ) :
        return tuple( self._nonterms )

    def _extendcontents( self, bq, contents ) :
        # Collect the contents that spans across muliple lines of same block
        # level. 'contents' is the accumulator
        if hasattr( bq, 'textcontents' ) :
            contents = bq.textcontents.listcontents( contents=contents )
        return contents

    def _processcontents( self, contents ) :
        # Process the accumulated contents
        process_textcontent( contents )
        html = ''.join([ cont.html for cont in contents ])
        return html

    def tohtml( self ) :
        html = pm = cm   = ''
        closemarkups = []   # Stack to manage nested list.
        contents = []
        bquotes = self.deepquotes( quotes=[] )
        for i in range(len(bquotes)) :
            cls = (i == 0) and 'firstlevel' or 'innerlevel'
            bquote = bquotes[i]
            cm = re.search( self.patt, bquote.markuptxt() ).group()
            cmpmark = cmp( len(pm), len(cm) )  # -1 or 0 or 1
            diffmark = abs( len(cm) - len(pm))  # 0 or 1

            if cmpmark > 0 :
                # previous bquote markup (pm) is one or more level deeper,
                # so end the blockquote(s)
                # And, process the accumulated content
                html += self._processcontents( contents )
                contents = []
                html += ''.join([closemarkups.pop() for i in range(diffmark)])

            elif cmpmark < 0 :
                # current bquote markup (cm) is one or more level deeper, 
                # open new blockquote(s)
                # And, process the accumulated content
                html += self._processcontents( contents )
                contents = []

                for j in range(diffmark-1) :
                    html += self.template % ''
                    closemarkups.append( '</blockquote>' )
                html += self.template % cls
                closemarkups.append( '</blockquote>' )
            self._extendcontents( bquote, contents )
            contents.append( Content(self.parser, '\n', TEXT_NEWLINE, '<br/>') )
            pm = cm

        # Pop-out the last new-line (<br/>)
        contents.pop( -1 ) if contents[-1].html == '<br/>' else None
        html += self._processcontents( contents )
        closemarkups.reverse()
        html += ''.join( closemarkups )
        return html

    def dump( self ) :
        bquotes = self.deepquotes( quotes=[] )
        return ''.join([ bq.dump() for bq in bquotes ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'bquotes: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def deepquotes( self, quotes=None ) :
        quotes = [] if quotes == None else quotes
        quotes = self.bquotes.deepquotes( quotes=quotes
                ) if self.bquotes else quotes
        quotes.append( self.bquote )
        return quotes


class BQuote( Node ) :
    """class to handle `blockquote` grammar."""

    def __init__( self, parser, markup, textcontents, newline ) :
        self.parser = parser
        self.markup = BQUOTE_START( parser, markup )
        self.textcontents = textcontents
        self.newline = NEWLINE( parser, newline )
        # terminals and non-terminals
        self._terms = [ self.markup, self.newline ]
        self._nonterms = [ self.textcontents ]

    def children( self ) :
        return ( self.markup, self.textcontents, self.newline )

    def tohtml( self ) :
        return ''

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'bquote: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]

    def markuptxt( self ) :
        return self.markup.dump()


class TextContents( Node ) :
    """class to handle `textcontents` grammar."""

    template = None

    def __init__( self, parser, textcontents=None, textcontent=None ) :
        # item can be Link or Macro or Html or BasicText
        self.parser = parser
        self.textcontents, self.textcontent = textcontents, textcontent
        # terminals and non-terminals
        self._terms = []
        self._nonterms = [ self.textcontents ] if self.textcontents else []
        self._nonterms.append( self.textcontent )

    def children( self ) :
        return tuple( self._nonterms )

    def tohtml( self ) :
        htmls, x = [], self
        while True :
            htmls.append( x.textcontent.tohtml() )
            if not x.textcontents : break
            x = x.textcontents
        htmls.reverse()
        html = ''.join( htmls )
        return html

    def dump( self ) :
        txts, x = [], self
        while True :
            txts.append( x.textcontent.dump() )
            if not x.textcontents : break
            x = x.textcontents
        txts.reverse()
        txt = ''.join( txts )
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        [ c.show(buf, offset, attrnames, showcoord) for c in self.children() ]

    def listcontents( self, contents=None ) :
        contents = [] if contents == None else contents
        contents = self.textcontents.listcontents( contents=contents 
                   ) if self.textcontents else contents
        contents.extend( self.textcontent.contents )
        return contents


class Link( Node ) :
    """class to handle `link` grammer.
    There are special links, 
        * - Open in new window,
        # - Create an anchor
        + - Image
    """
    l_template = '<a class="etlink" target="%s" href="%s">%s</a>'
    a_template = '<a class="etlink anchor" name="%s">%s</a>'
    img_template = '<img class="et" src="%s" alt="%s" style="%s"/>'

    def __init__( self, parser, link ) :
        self.parser, app = parser, parser.etparser.app

        # parse the text
        tup  = link[2:-2].split( '|', 1 )
        href = tup and tup.pop(0).strip(' \t') or ''
        text = tup and escape_htmlchars(tup.pop(0)).strip(' \t') or ''

        # parse the href and for special notations
        html   =''
        prefix = href[:1]

        if prefix == '*' :              # Link - Open in new window
            html = self.l_template % ( '_blank', href[1:], text or href[1:] )

        elif href[:1] == '#' :          # Link - Anchor 
            n = 'name="%s"' % href[1:]
            html = self.a_template % (n, text or href[1:] )

        elif prefix == '+' :            # Link - Image (actually no href)
            style = 'float: left;' if href[1:2] == '<' else (
                    'float: right;' if href[1:2] == '>' else ''
                    )
            src = href[1:].strip( '<>' )
            html = self.img_template % ( src, text or src, style )

        elif app and (app.name == 'zeta' and prefix == '@') :
                                        # Link - InterZeta or ZetaLinks
            from eazytext.zetawiki import parse_link2html
            html = parse_link2html( parser.etparser, href, text )

        elif href[:6] == "mailto" :     # Link - E-mail
            if self.parser.etparser.obfuscatemail :
                href = "mailto" + obfuscatemail(href[:6])
                text = obfuscatemail(text or href[:6]) 
            html = self.l_template % ( '', href, text )

        else :
            html = self.l_template % ( '', href, text or href )

        self.contents = [ Content( parser, link, TEXT_LINK, html ) ]
        self.link = LINK( parser, link )
        # terminals and non-terminals
        self._terms = [ self.link ]
        self._nonterms = []

    def children( self ) :
        return tuple(self._terms)

    def tohtml( self ) :
        return ''.join([ c.html for c in self.contents ])

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'link: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]


class Macro( Node ) :
    """class to handle `macro` grammer."""

    template = None     # no wrapper with `macro` & <macroname> classes

    def __init__( self, parser, macro  ) :
        self.parser = parser
        self.text = macro
        self.macroobject = build_macro( self, macro )
        self.contents = [
            Content( parser, macro, TEXT_MACRO, self.macroobject.tohtml )
        ]
        self.macro = MACRO( parser, macro )
        # terminals and non-terminals
        self._terms = [ self.macro ]
        self._nonterms = []

    def children( self ) :
        return tuple( self._terms )

    def tohtml( self ) :
        return ''.join([ c.html for c in self.contents ])

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'macro: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]


class Html( Node ) :
    """class to handle `html` grammer."""

    def __init__( self, parser, html_text ) :
        self.parser = parser
        self.text = html_text
        self.html = html_text[2:-2]
        self.html = tt.parsetag( self.html )
        self.contents = [ Content( parser, self.text, TEXT_HTML, self.html ) ]
        self.htmlterm = HTML(parser, html_text)
        # terminals and non-terminals
        self._terms = [ self.htmlterm ]
        self._nonterms = []

    def children( self ) :
        return tuple( self._terms )

    def tohtml( self ) :
        html = ''.join([ c.html for c in self.contents ])
        try :
            if html and self.parser.etparser.stripscript :
                e = lhtml.fromstring( html )
                [ es.getparent().remove(es) for es in e.xpath( '//script' ) ]
                html = lhtml.tostring(e)
        except :
            if self.parser.etparser.debug : raise
            html = escape_htmlchars( html )
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'html: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]


class BasicText( Node ) :
    """class to handle `basictext` grammar."""

    httpuri_template = '<a class="ethttpuri" href="%s"> %s </a>'
    wwwuri_template = '<a class="etwwwuri" href="http://%s"> %s </a>'

    def __init__( self, parser, type, text ) :
        self.parser = parser
        # self.contents as list of Content object

        if type == TEXT_SPECIALCHAR :
            self.contents = []
            virtuallines = text.split( '\\\\' )
            self.contents.append(
                Content( parser, virtuallines[0], TEXT_SPECIALCHAR,
                         escape_htmlchars( virtuallines[0] ))
            )
            for line in virtuallines[1:] :
                self.contents.append(
                    Content( parser, '\\\\', TEXT_SPECIALCHAR_LB, '<br/>' )
                )
                self.contents.append( Content( parser, line, TEXT_SPECIALCHAR,
                                               escape_htmlchars(line) ))

        elif type == TEXT_HTTPURI :
            self.contents = [ Content( parser, text, type,
                                       self.httpuri_template % (text, text)
                              )
                            ]

        elif type == TEXT_WWWURI :
            self.contents = [ Content( parser, text, type,
                                       self.wwwuri_template % (text,text)
                              )
                            ]
        
        elif type > 2000 :
            self.contents = [ Content( parser, text, type ) ]

        else : # TEXT_CHARPIPE, TEXT_ALPHANUM, TEXT_ESCAPED
            self.contents = [ Content( parser, text, type, text ) ]
        # terminals and non-terminals
        self._terms = [ BASICTEXT( parser, terminal=text ) ]
        self._nonterms = []

    def children( self ) :
        return tuple(self._terms)

    def tohtml( self ):
        return ''.join([ c.html for c in self.contents ])

    def dump( self ) :
        text = ''
        for c in self.contents :
            text += [ c.text, '~' + c.text ][ c.type == TEXT_ESCAPED ]
        return text

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write(lead + 'basictext: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [ c.show(buf, offset+2, attrnames, showcoord) for c in self.children() ]


class ParagraphSeparator( Node ) :
    """class to handle `paragraph_separator` grammar."""

    def __init__( self, parser, *args ) :
        self.parser  = parser
        self.newline = self.empty = self.paragraph_separator = None
        if len(args) == 1 :
            if args[0] == '\n' or args[0] == '\r\n' :
                self.newline = NEWLINE( parser, args[0] )
            elif isinstance( args[0], EMPTY ) :
                self.empty   = args[0]
        elif len(args) == 2 :
            self.paragraph_separator = args[0]
            self.newline             = NEWLINE( parser, args[1] )

    def children( self ) :
        childnames = [ 'newline', 'empty', 'paragraph_separator' ]
        nodes      = filter(
                        None,
                        [ getattr( self, attr, None ) for attr in childnames ]
                     )
        return tuple(nodes)

    def tohtml( self ) :
        return ''.join([ c.tohtml() for c in self.children() ])

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        #lead = ' ' * offset
        #buf.write(lead + 'paragraph_separator: ')

        #if showcoord :
        #    buf.write( ' (at %s)' % self.coord )
        #buf.write('\n')

        #for c in self.children() :
        #    c.show( buf, offset + 2, attrnames, showcoord )
        pass

#-------------------------- AST Terminals -------------------------

class EMPTY( Terminal ) :
    pass
class NEWLINE( Terminal ) :
    pass
class NOWIKI_OPEN( Terminal ) :
    pass
class NOWIKI_CLOSE( Terminal ) :
    pass
class NOWIKILINES( Terminal ) :
    pass
class HEADING( Terminal ) :
    pass
class HORIZONTALRULE( Terminal ) :
    pass
class BTABLE_START( Terminal ) :
    pass
class BTABLESTYLE_START( Terminal ) :
    pass
class TABLE_CELLSTART( Terminal ) :
    pass
class ORDLIST_START( Terminal ) :
    pass
class UNORDLIST_START( Terminal ) :
    pass
class DEFINITION_START( Terminal ) :
    pass
class BQUOTE_START( Terminal ) :
    pass
class LINK( Terminal ) :
    pass
class MACRO( Terminal ) :
    pass
class HTML( Terminal ) :
    pass
class BASICTEXT( Terminal ) :
    pass
