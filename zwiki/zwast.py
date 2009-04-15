import sys
import re

# Todo :
#   1. Add unicode support
#   2. Fix the heading bug
#   3. Add support for bold_underline, italic_underline, bold_italic_underline
#      and update the document.

# text type for BasicText
TEXT_ZWCHARPIPE      = 'zwcharpipe'
TEXT_ALPHANUM        = 'alphanum'
TEXT_SPECIALCHAR     = 'specialchar'
TEXT_SPECIALCHAR_LB  = 'linebreak'
TEXT_HTTPURI         = 'httpuri'
TEXT_WWWURI          = 'wwwuri'
TEXT_ESCAPED         = 'escaped'
TEXT_LINK            = 'link'
TEXT_MACRO           = 'macro'

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

ref2markups  = [ M_BOLD, M_ITALIC, M_UNDERLINE, M_SUPERSCRIPT, M_SUBSCRIPT,
                 M_BOLDITALIC ]
ref3markups  = [ M_BOLDITALICUNDERLINE ]
markup2type  = {
                 M_BOLD                : FORMAT_BOLD,
                 M_ITALIC              : FORMAT_ITALIC,
                 M_UNDERLINE           : FORMAT_UNDERLINE,
                 M_SUPERSCRIPT         : FORMAT_SUPERSCRIPT,
                 M_SUBSCRIPT           : FORMAT_SUBSCRIPT,
                 M_BOLDITALIC          : FORMAT_BOLDITALIC,
                 M_BOLDITALICUNDERLINE : FORMAT_BOLDITALICUNDERLINE,
               }
markup2html   = { 
        "''"  : ('<strong>','</strong>' ),
        '//'  : ('<em>','</em>' ),
        '__'  : ('<u>','</u>' ),
        '^^'  : ('<sup>','</sup>' ),
        ',,'  : ('<sub>','</sub>' ),
        "'/"  : ('<strong><em>','</em></strong>' ),
        "'/_" : ('<strong><em><u>','</u></em></strong>' ),
}

# ---------------------- Helper Class objects --------------

class Content( object ) :
    """The whole of wiki text is parsed and encapulated as lists of Content
    objects."""
    def __init__( self, text, type=None, html=None ) :
        self.text = text
        self.type = type
        self.html = html

    def __repr__( self ) :
        return "Console<'%s','%s','%s'>" % (self.text, self.type, self.html )

def process_textcontent( contents ) :
    for i in range(len(contents)) :
        beginmarkup_cont = contents[i]
        if beginmarkup_cont.html or \
           beginmarkup_cont.type == TEXT_SPECIALCHAR:
            continue
        for j in range( i+1, len(contents) ) :
            endmarkup_cont = contents[j]
            if endmarkup_cont.type == beginmarkup_cont.type :
                # Found the markup pair.
                beginmarkup_cont.html = markup2html[ beginmarkup_cont.text ][0]
                endmarkup_cont.html   = markup2html[ endmarkup_cont.text ][1]
                break;
        else :
            beginmarkup_cont.html = beginmarkup_cont.text
    return

def parse_text( text ) :
    """Parse the text for wiki text markup and valid text content and return a
    list of content object"""
    contents = []
    i = 0
    while i < len(text) :
        ch2 = text[i:i+2]
        ch3 = text[i:i+3]
        if ch2 in ref2markups :
            contents.append( Content( ch2, markup2type[ch2] ))
            i += 2
        elif ch3 in ref3markups :
            contents.append( Content( ch3, markup2type[ch3] ))
            i += 3
        else :
            contents.append( Content( text[i], TEXT_SPECIALCHAR, text[i] ))
            i += 1
    return contents

# ---------------------- Exception classes ----------------

class ZWASTError( Exception ):
    pass


# ---------------------- AST class nodes -------------------

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
    """class to handle `wikipage` grammar."""

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
    """class to handle `paragraphs` grammar."""

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
    """class to handle `paragraph` grammar."""

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
    """class to handle `pragmas` grammar."""

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
    """class to handle `nowikiblock` grammar."""

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
    """class to handle `heading` grammar."""

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
    """class to handle `horizontalrule` grammar."""

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
    """class to handle `textlines` grammar."""

    def __init__( self, textcontents, newline  ) :
        self.textlines = [ (textcontents, Newline(newline)) ]

    def appendline( self, textcontents, newline ) :
        self.textlines.append( (textcontents, Newline(newline)) )

    def children( self ) :
        return (self.textlines,)

    def tohtml( self ) :
        # Process the text contents and convert them into html
        contents = []
        [ contents.extend( item.contents )
          for textcontents, nl in self.textlines 
          for item in textcontents.textcontents ]
        process_textcontent( contents )
        html   = ''
        for textcontents, newline in self.textlines :
            html += textcontents.tohtml()
            html += newline.tohtml()
        return html

    def dump( self ) :
        txt = ''.join([ ''.join([ item.dump()
                                  for item in textcontents.textcontents ]) +\
                        newline.dump()
                        for textcontents, newline in self.textlines ])
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'textlines: ' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        linecount = 1
        for textcontent, newline in self.textlines :
            buf.write( lead + '(line %s)\n' % linecount )
            linecount += 1
            textcontent.show( buf, offset + 2, attrnames, showcoord )
            newline.show( buf, offset + 2, attrnames, showcoord )


class TableRows( Node ) :
    """class to handle `table_rows` grammar."""

    def __init__( self, row, pipe=None, newline=None  ) :
        """`row` is table_cells"""
        self.rows = [ (row, pipe, Newline(newline)) ]

    def appendrow( self, row, pipe=None, newline=None ) :
        self.rows.append( (row, pipe, Newline(newline)) )

    def tohtml( self ) :
        html    = '<table border=1>'
        for row, pipe, newline in self.rows :
            html += '<tr>' + row.tohtml() + \
                    ( newline and newline.tohtml() ) or '' + \
                    '</tr>'
        html   += '</table>'
        return html

    def children( self ) :
        return self.rows

    def dump( self ) :
        return ''.join(
            [ row.dump() + (pipe or '') + (nl and nl.dump()) or ''
              for row, pipe, nl in self.rows ]
        )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'table_rows: ' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        rowcount = 1
        for row, pipe, nl in self.rows :
            buf.write( lead + '(row %s)\n' % rowcount )
            rowcount += 1
            row.show( buf, offset + 2, attrnames, showcoord )
            nl and nl.show( buf, offset + 2, attrnames, showcoord )


class TableCells( Node ) :
    """class to handle `table_cells` grammar."""

    def __init__( self, pipe, cell  ) :
        """`cell` can be `Empty` object or `TextContents` object"""
        self.cells     = [ (pipe, cell) ]

    def appendcell( self, pipe, cell ) :
        self.cells.append( ( pipe, cell ) )

    def children( self ) :
        return ( self.cells, )

    def totalcells( self ) :
        return sum([ 1
                for pipe, cell in self.cells if isinstance( cell, TextContents )
               ])

    def tohtml( self ) :
        # Process the text contents and convert them into html
        contents = []
        [ contents.extend( item.contents )
          for pipe, cell in self.cells if isinstance( cell, TextContents )
                                       for item in cell.textcontents ]
        process_textcontent( contents )
        return ''.join(
            [ '<td>' + cell.tohtml() + '</td>' for pipe, cell in self.cells ]
        )

    def dump( self ) :
        return ''.join(
            [ pipe + cell.dump() for pipe, cell in self.cells ]
        )

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
    """class to handle `orderedlists` and `unorderedlists` grammar."""

    def __init__( self, l ) :
        self.listitems = [ l ]

    def appendlist( self, l ) :
        self.listitems.append( l )

    def children( self ) :
        return self.listitems

    def tohtml( self ) :
        html         = ''
        closemarkups = []   # Stack to manage nested list.
        markups      = { '#' : ('<ol>', '</ol>'),
                         '*' : ('<ul>', '</ul>') }
        pm   = ''
        cm   = ''
        for l in self.listitems :
            cm       = re.search( r'[\*\#]{1,5}$', l.listmarkup ).group()
            cmpmark  = cmp( len(pm), len(cm) )  # -1 or 0 or 1
            diffmark = abs( len(cm) - len(pm))  # 0 or 1
            if cmpmark > 0 :
                # previous list markup (pm) is one level deeper, so end the list
                html += ''.join([ closemarkups.pop() for i in range(diffmark) ])
            elif cmpmark < 0 :
                # current list markup (cm) is one level deeper, open a new list
                for i in range(diffmark) :
                    html += markups[cm[0]][0]
                    closemarkups.append( markups[cm[0]][1] )
            html += l.tohtml()
            pm = cm
        html += ''.join([ closemarkups.pop() for i in range(len(closemarkups)) ])
        return html

    def dump( self ) :
        return ''.join([ c.dump() for c in self.listitems ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        if showcoord :
            buf.write( ' (at %s)' % self.coord )

        for c in self.listitems :
            c.show( buf, offset + 2, attrnames, showcoord )


class List( Node ) :
    """class to handle `orderedlist` and `unorderedlist` grammar."""

    def __init__( self, listtype, listmarkup, listitem, newline ) :
        self.listtype     = listtype
        self.listmarkup   = listmarkup
        if isinstance( listitem, Empty ) :
            self.empty        = listitem
            self.textcontents = None
        elif isinstance( listitem, TextContents ) :
            self.textcontents = listitem
            self.empty        = None
        else :
            raise ZWASTError( "Unknown `listitem` for List() node" )
        self.newline      = Newline( newline )

    def children( self ) :
        return ( self.listtype, self.listmarkup, self.textcontents,
                 self.newline )

    def tohtml( self ) :
        # Process the text contents and convert them into html
        if self.textcontents :
            contents = []
            [ contents.extend( item.contents )
              for item in self.textcontents.textcontents ]
            process_textcontent( contents )
            html = '<li>' + self.textcontents.tohtml() + '</li>'
        elif self.empty :
            html = '<li>' + self.empty.tohtml() + '</li>'
        else :
            raise ZWASTError( "tohtml() : No listitem available for List() node" )
        return html

    def dump( self ) :
        if self.textcontents :
            dump = self.listmarkup + self.textcontents.dump()  + \
                   self.newline.dump()
        elif self.empty :
            dump = self.listmarkup + self.empty.dump()  + self.newline.dump()
        else :
            raise ZWASTError( "dump() : No listitem available for List() node" )
        return dump

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

        if self.textcontents :
            self.textcontents.show()
        elif self.empty :
            self.empty.show()
        else :
            raise ZWASTError( "show() : No listitem available for List() node" )


class TextContents( Node ) :
    """class to handle `textcontents` grammar."""
    def __init__( self, item  ) :
        # item is Link or Macro or BasicText
        self.textcontents = [ item ]

    def appendcontent( self, item ) :
        # item is Link or Macro or BasicText
        self.textcontents.append( item )

    def children( self ) :
        return self.textcontents

    def tohtml( self ) :
        return ''.join([ item.tohtml() for item in self.textcontents ])

    def dump( self ) :
        return ''.join([ item.dump() for item in self.textcontents ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'textcontent: ' )
        if showcoord :
            buf.write( ' (at %s)' % self.coord )

        for textcontent in self.textcontents :
            textcontent.show( buf, offset + 2, attrnames, showcoord )


class Link( Node ) :
    """class to handle `link` grammer."""

    def __init__( self, link ) :
        # Convert the link to html.
        # TODO: Later implement a fullfledged link processor
        tup  = link[2:-2].split( '|', 1 )
        text = (len(tup) == 2 and  tup[1]) or tup[0]
        href = tup[0]
        html = '<a href=' + href + '>' + text + '</a>'
        self.contents = [ Content( link, TEXT_LINK, html ) ]

    def children( self ) :
        return self.contents

    def tohtml( self ) :
        return ''.join([ c.html for c in self.contents ])

    def dump( self ) :
        return ''.join([ c.text for c in self.contents ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'link: ' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class Macro( Node ) :
    """class to handle `macro` grammer."""

    def __init__( self, macro  ) :
        # TODO : Implement the macro engine.
        html = macro
        self.contents = [ Content( macro, TEXT_MACRO, html ) ]

    def children( self ) :
        return self.contents

    def tohtml( self ) :
        return ''.join([ c.html for c in self.contents ])

    def dump( self ) :
        return ''.join([ c.html for c in self.contents ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'macro: `%s`' % self.macro )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class BasicText( Node ) :
    """class to handle `basictext` grammar."""

    def __init__( self, type, text  ) :
        # self.contents as list of Content object
        if type == TEXT_SPECIALCHAR :
            self.contents = []
            linebreaks    = text.split( '\\\\' )
            if len(linebreaks) >= 1 :
                self.contents.extend( parse_text( linebreaks[0] ))
            for text in linebreaks[1:] :
                self.contents.append(
                    Content( '\\\\', TEXT_SPECIALCHAR_LB, '<br/>' )
                )
                self.contents.extend( parse_text( text ))
        elif type == TEXT_HTTPURI :
            self.contents = [ Content(
                                text, type, '<a href='+text+ '>' + text + '</a>'
                              )
                            ]
        elif type == TEXT_WWWURI :
            self.contents = [ Content(
                                text, type, '<a href='+text+ '>' + text + '</a>'
                              )
                            ]
        else : # TEXT_ZWCHARPIPE, TEXT_ALPHANUM, TEXT_ESCAPED
            self.contents = [ Content( text, type, text ) ]

    def children( self ) :
        return self.contents

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
        buf.write(lead + 'basictext :' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')


class ParagraphSeparator( Node ) :
    """class to handle `paragraph_separator` grammar."""

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
        return ''.join([ c.tohtml() for c in self.children() ])

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
    """class to handle `empty` grammar"""

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
    """class to handle `newline` grammer"""

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


