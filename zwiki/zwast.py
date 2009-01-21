import sys
import re

import zwiki.textformat as textformat

# text type for BasicText
TEXT_ZWCHARPIPE      = 'zwcharpipe'
TEXT_ALPHANUM        = 'alphanum'
TEXT_SPECIALCHAR     = 'specialchar'
TEXT_HTTPURI         = 'httpuri'
TEXT_WWWURI          = 'wwwuri'
TEXT_ESCAPED         = 'escaped'

# Format type for FormattedText
FORMAT_BOLD          = 'fmt_bold'
FORMAT_ITALIC        = 'fmt_italic'
FORMAT_UNDERLINE     = 'fmt_underline'
FORMAT_SUPERSCRIPT   = 'fmt_superscript'
FORMAT_SUBSCRIPT     = 'fmt_subscript'
FORMAT_BOLDITALIC    = 'fmt_bolditalic'
FORMAT_BOLDITALICUNDERLINE = 'fmt_bolditalicunderline'
FORMAT_NON           = 'fmt_non'
FORMAT_EMPTY         = 'fmt_empty'

# List Type
LIST_ORDERED         = 'ordered'
LIST_UNORDERED       = 'unordered'

# Markup
M_PIPE               = '|'
M_NOWIKI_OPEN        = '{{{'
M_NOWIKI_CLOSE       = '}}}'
M_MACROOPEN          = '{{'
M_MACROCLOSE         = '}}'
M_LINKOPEN           = '[['
M_LINKCLOSE          = ']]'
M_BOLD               = "''"
M_ITALIC             = "//"
M_UNDERLINE          = "__"
M_SUPERSCRIPT        = "^^"
M_SUBSCRIPT          = ",,"
M_BOLDITALIC         = "'/"
M_BOLDITALICUNDERLINE = "'/_"

class Node( object ):
    """Abstract base class for ZWiki AST nodes."""

    def children( self ):
        """A sequence of all children that are Nodes"""
        pass

    def tohtml( self ):
        """Translate the node and all the children nodes to html markup and
        return the content"""

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


class Wikipage( Node ):
    """Wiki class to handle `wikipage` grammar."""

    def __init__( self, *args  ) :
        if len( args ) == 1 and isinstance( args[0], Pragmas ) :
            self.pragmas    = args[0]
        elif len( args ) == 1 and isinstance( args[0], Paragraphs ) :
            self.paragraphs = args[0]
        elif len( args ) == 2 :
            self.pragmas    = args[0]
            self.paragraphs = args[1]

    def children( self ) :
        childnames = [ 'pragmas', 'paragraphs' ]
        nodes      = filter(
                        None,
                        [ getattr( self, attr, None ) for attr in childnames ]
                     )
        return tuple(nodes)

    def tohtml( self ):
        return ''.join([ c.tohtml() for c in self.children() ])

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'wikipage: ' )

        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        for c in self.children():
            c.show( buf, offset + 2, attrnames, showcoord )


class Paragraphs( Node ) :
    """Wiki class to handle `paragraphs` grammar."""

    def __init__( self, *args  ) :
        if len( args ) == 1 :
            self.paragraph_separator = args[0]
        elif len( args ) == 2 :
            self.paragraph           = args[0]
            self.paragraph_separator = args[1]
        elif len( args ) == 3 :
            self.paragraphs          = args[0]
            self.paragraph           = args[1]
            self.paragraph_separator = args[2]

    def children( self ) :
        childnames = [ 'paragraphs', 'paragraph', 'paragraph_separator' ]
        nodes      = filter(
                        None,
                        [ getattr( self, attr, None ) for attr in childnames ]
                     )
        return tuple(nodes)

    def tohtml( self ):
        return ''.join([ c.tohtml() for c in self.children() ])

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'paragraphs: ' )

        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        for c in self.children():
            c.show( buf, offset + 2, attrnames, showcoord )


class Paragraph( Node ) :
    """Wiki class to handle `paragraph` grammar."""

    def __init__( self, paragraph ) :
        self.paragraph = paragraph

    def children( self ) :
        return ( self.paragraph, )

    def tohtml( self ):
        return '<p>' + self.paragraph.tohtml() + '</p>'

    def dump( self ) :
        return self.paragraph.dump()

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write(lead + 'paragraph: ')

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        for c in self.children() :
            c.show( buf, offset + 2, attrnames, showcoord )


class Pragmas( Node ) :
    """Wiki class to handle `pragmas` grammar."""

    def __init__( self, pragma , newline ) :
        self.pragma  = pragma
        self.newline = Newline( newline )

    def children( self ) :
        return ( self.pragma, self.newline )

    def tohtml( self ) :
        return ''

    def dump( self ) :
        return self.pragma + self.newline.dump()

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'pragmas: `%s` ' % self.children()[:-1] )

        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class NoWiki( Node ) :
    """Wiki class to handle `nowikiblock` grammar."""

    def __init__( self, opennl, nowikilines, closenl  ) :
        self.opennewline  = Newline( opennl )
        self.nowikilines  = nowikilines
        self.closenewline = Newline( closenl )

    def children( self ) :
        return (self.nowikilines,)

    def tohtml( self ):
        return ''

    def dump( self ) :
        txt  = M_NOWIKI_OPEN + self.opennewline.dump()
        txt += self.nowikilines
        txt += M_NOWIKI_CLOSE + self.closenewline.dump()
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'nowikiblock: `%s` ' % self.nowikilines.split('\n')[0] )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class Heading( Node ) :
    """Wiki class to handle `heading` grammar."""

    def __init__( self, fulltext, newline ) :
        self.fulltext = fulltext
        self.newline  = Newline( newline )

    def children( self ) :
        return ( self.fulltext, self.newline )

    def tohtml( self ):
        l    = len(re.search( r'^={1,5}', self.fulltext ).group())
        html = '<h'+str(l)+'> ' + self.fulltext.strip('=') + \
               ' </h'+str(l)+'>' + \
               self.newline.tohtml()
        return html

    def dump( self ) :
        return self.fulltext + self.newline.dump()

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'heading: `%s` ' % self.children()[:-1] )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        self.newline.show( buf, offset + 2, attrnames, showcoord )


class HorizontalRule( Node ) :
    """Wiki class to handle `horizontalrule` grammar."""

    def __init__( self, hrule, newline ) :
        self.hrule   = hrule
        self.newline = Newline(newline)

    def children( self ) :
        return (self.hrule, self.newline)

    def tohtml( self ):
        return '<hr />'

    def dump( self ) :
        return self.hrule + self.newline.dump()

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'horizontalrule:' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        self.newline.show( buf, offset + 2, attrnames, showcoord )


class TextLines( Node ) :
    """Wiki class to handle `textlines` grammar."""

    def __init__( self, text_content, newline  ) :
        self.textlines = [ (text_content, Newline(newline)) ]

    def appendline( self, text_content, newline ) :
        self.textlines.append( (text_content, Newline(newline)) )

    def children( self ) :
        return (self.textlines,)

    def tohtml( self ) :
        html   = ''
        for text_content, newline in self.textlines :
            html += ''.join(textformat.process_text( text_content ))
            html += newline.tohtml()
        return html

    def dump( self ) :
        txt = ''.join([ ''.join([ text.dump()
                                 for text in text_content ]) + newline.dump()
                       for text_content, newline in self.textlines ])
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'textlines: ' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        linecount = 1
        for text_content, newline in self.textlines :
            buf.write( lead + '(line %s)\n' % linecount )
            linecount += 1
            for text in text_content :
                text.show( buf, offset + 2, attrnames, showcoord )
            newline.show( buf, offset + 2, attrnames, showcoord )


class TableRows( Node ) :
    """Wiki class to handle `table_rows` grammar."""

    def __init__( self, row, pipe=None, newline=None  ) :
        self.rows = [ (row, pipe, Newline(newline)) ]

    def appendrow( self, row, pipe=None, newline=None ) :
        self.rows.append( (row, pipe, Newline(newline)) )

    def tohtml( self ) :
        html    = '<table border=1>'
        maxcols = max([ row.totalcells() for row, pipe, newline in self.rows ])
        for row, pipe, newline in self.rows :
            html += '<tr>'
            html += row.tohtml( maxcols=maxcols )
            if newline :
                html += newline.tohtml()
            html += '</tr>'
        html   += '</table>'
        return html

    def children( self ) :
        return ( self.rows, )

    def dump( self ) :
        txt = ''
        for tcells, pipe, nl in self.rows :
            txt += tcells.dump()
            txt += pipe or ''
            txt += (nl and nl.dump()) or ''
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'table_rows: ' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        rowcount = 1
        for tablecells, pipe, nl in self.rows :
            buf.write( lead + '(row %s)\n' % rowcount )
            rowcount += 1
            tablecells.show( buf, offset + 2, attrnames, showcoord )
            nl and nl.show( buf, offset + 2, attrnames, showcoord )


class TableCells( Node ) :
    """Wiki class to handle `table_cells` grammar."""

    def __init__( self, pipe, cell  ) :
        self.cells     = [ (pipe, cell) ]

    def appendcell( self, pipe, cell ) :
        self.cells.append( ( pipe, cell ) )

    def children( self ) :
        return ( self.cells, )

    def totalcells( self ) :
        count = 0
        for pipe, cell in self.cells :
            for l in cell :
                if isinstance( cell, (Link,Macro,BasicText) ) :
                    count += 1
                    break
        return count

    def tohtml( self, maxcols ) :
        html = ''
        for pipe, cell in self.cells :
            html += '<td>'
            html += ''.join(textformat.process_text( cell ))
            html += '</td>'
        return html

    def dump( self ) :
        txt = ''.join([ pipe + ''.join([ t.dump() for t in txts ])
                        for pipe, txts in self.cells ])
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'table_cells: ' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        cellcount = 1
        for txts, pipe in self.cells :
            buf.write( lead + '(cell %s)\n' % cellcount )
            cellcount += 1
            for item in txts :
                item.show( buf, offset + 2, attrnames, showcoord )


class Lists( Node ) :
    """Wiki class to handle `orderedlists` and `unorderedlists` grammar."""

    def __init__( self, l ) :
        self.lists = [ l ]

    def appendlist( self, l ) :
        self.lists.append( l )

    def children( self ) :
        return (self.lists, )

    def tohtml( self ) :
        html         = ''
        closemarkups = []
        markups      = { '#' : ('<ol>', '</ol>'),
                         '*' : ('<ul>', '</ul>') }
        pm   = ''
        cm   = ''
        for l in self.lists :
            cm       = re.search( r'[\*\#]{1,5}$', l.listmarkup ).group()
            cmpmark  = cmp( len(pm), len(cm) )
            diffmark = abs(len(cm) - len(pm))
            if cmpmark > 0 :
                html += ''.join([ closemarkups.pop() for i in range(diffmark) ])
            elif cmpmark < 0 :
                for i in range(diffmark) :
                    html += markups[cm[0]][0]
                    closemarkups.append( markups[cm[0]][1] )
            html += l.tohtml()
            pm = cm
        html += ''.join([ closemarkups.pop() for i in range(len(closemarkups)) ])
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.lists ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        if showcoord :
            buf.write( ' (at %s)' % self.coord )

        for c in self.lists :
            c.show( buf, offset + 2, attrnames, showcoord )


class List( Node ) :
    """Wiki class to handle `orderedlist` and `unorderedlist` grammar."""

    def __init__( self, listtype, listmarkup, text_content, newline ) :
        self.listtype     = listtype
        self.listmarkup   = listmarkup
        self.text_content = text_content
        self.newline      = Newline( newline )

    def children( self ) :
        return ( self.listtype, self.listmarkup, self.text_content,
                 self.newline )

    def tohtml( self ) :
        html = '<li>'
        html += ''.join(textformat.process_text( self.text_content ))
        html += '</li>'
        return html

    def dump( self ) :
        txt     =  self.listmarkup
        txt     += ''.join([ c.dump() for c in self.text_content ])
        txt     += self.newline.dump()
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        if self.listtype == 'ordered' :
            buf.write( lead + 'orderedlist: `%s` ' % self.listmarkup )
        if self.listtype == 'unordered' :
            buf.write( lead + 'unorderedlist: `%s` ' % self.listmarkup )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        for t in self.text_content :
            t.show( buf, offset + 2, attrnames, showcoord )


class Link( Node ) :
    """Wiki class to handle `link` grammer."""

    def __init__( self, link ) :
        self.link      = link

    def children( self ) :
        return ( self.link, )

    def tohtml( self ) :
        tup  = self.link[2:-2].split( '|', 1 )
        text = (len(tup) == 2 and  tup[1]) or tup[0]
        href = tup[0]
        html = '<a href=' + href + '>' + text + '</a>'
        return html

    def dump( self ) :
        return self.link

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'link: `%s`' % self.link )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class Macro( Node ) :
    """Wiki class to handle `macro` grammer."""

    def __init__( self, macro  ) :
        self.macro = macro

    def children( self ) :
        return ( self.macro, )

    def tohtml( self ) :
        return ''

    def dump( self ) :
        return self.macro

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'macro: `%s`' % self.macro )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class BasicText( Node ) :
    """Wiki class to handle `basictext` grammar."""

    def __init__( self, type, text  ) :
        self.type = type
        self.text = text

    def children( self ) :
        return ( self.type, self.text )

    def tohtml( self ):
        self.text = self.text.replace( '\\\\', '<br/>' )
        res = self.text
        if self.type == TEXT_SPECIALCHAR :
            markups = textformat.parse_text( self.text )
            if markups :
                res =  (self.text, markups)
        elif self.type == TEXT_HTTPURI :
            res = '<a href=' + self.text + '>' + self.text + '</a>'
        elif self.type == TEXT_WWWURI :
            res = '<a href=' + self.text + '>' + self.text + '</a>'
        elif self.type == TEXT_ESCAPED :
            res = self.text[1]
        return res

    def dump( self ) :
        return self.text

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write(lead + 'basictext: `%s`' % self.text )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class ParagraphSeparator( Node ) :
    """Wiki class to handle `paragraph_separator` grammar."""

    def __init__( self, *args ) :
        self.newline             = None
        self.empty               = None
        self.paragraph_separator = None
        if len(args) == 1 :
            if args[0] == '\n' or args[0] == '\r\n' :
                self.newline = Newline( args[0] )
            elif isinstance( args[0], Empty ) :
                self.empty   = args[0]
        elif len(args) == 2 :
            self.paragraph_separator = args[0]
            self.newline             = Newline( args[1] )

    def children( self ) :
        childnames = [ 'newline', 'empty', 'paragraph_separator' ]
        nodes      = filter(
                        None,
                        [ getattr( self, attr, None ) for attr in childnames ]
                     )
        return tuple(nodes)

    def tohtml( self ) :
        html = ''
        for c in self.children() :
            html += c.tohtml()
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write(lead + 'paragraph_separator: ')

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        for c in self.children() :
            c.show( buf, offset + 2, attrnames, showcoord )


class Empty( Node ) :
    """Wiki class to handle `empty` grammar."""

    def __init__( self ) :
        pass

    def children( self ) :
        return ()

    def tohtml( self ):
        return ''

    def dump( self ) :
        return ''

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write(lead + 'empty: ')
        buf.write('\n')


class Newline( Node ) :
    """Wiki class to handle newline."""

    def __init__( self, newline ) :
        self.newline = newline

    def children( self ) :
        return ( self.newline, )

    def tohtml( self ):
        return self.newline

    def dump( self ) :
        return self.newline

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write(lead + 'newline: ')
        buf.write('\n')


