import sys

# text type for BasicText
TEXT_ZWCHAR          = 'zwchar'
TEXT_ALPHANUM        = 'alphanum'
TEXT_SPECIALCHAR     = 'specialchar'
TEXT_HTTPURI         = 'httpuri'
TEXT_WWWURI          = 'wwwuri'
TEXT_ESCAPED         = 'escaped'
TEXT_PARAN           = 'paranthesis'
TEXT_SQRBRACKET      = 'squarebracket'
TEXT_ZWCHARPIPE      = 'zwcharpipe'
TEXT_ZWCHARLINEBREAK = 'zwcharlinebreak'
TEXT_EMPTY           = 'empty'

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
        if len( args ) == 1 :
            self.pragmas    = args[0]
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

    def __init__( self, formatted_texts, newline  ) :
        self.formattedtextlines = [ (formatted_texts, Newline(newline)) ]

    def appendline( self, formatted_texts, newline ) :
        self.formattedtextlines.append( (formatted_texts, Newline(newline)) )

    def children( self ) :
        return (self.formattedtextlines,)

    def dump( self ) :
        txt = ''.join([ ''.join([ fmttxt.dump()
                                 for fmttxt in formatted_texts ]) + newline.dump()
                       for formatted_texts, newline in self.formattedtextlines ])
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'textlines: ' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        linecount = 1
        for formatted_texts, newline in self.formattedtextlines :
            buf.write( lead + '(line %s)\n' % linecount )
            linecount += 1
            for fmttxt in formatted_texts :
                fmttxt.show( buf, offset + 2, attrnames, showcoord )
            newline.show( buf, offset + 2, attrnames, showcoord )


class TableRows( Node ) :
    """Wiki class to handle `table_rows` grammar."""

    def __init__( self, row, pipe=None, newline=None  ) :
        self.rows = [ (row, pipe, Newline(newline)) ]

    def appendrow( self, row, pipe=None, newline=None ) :
        self.rows.append( (row, pipe, Newline(newline)) )

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
        self.cells = [ (pipe, cell) ]

    def appendcell( self, pipe, cell ) :
        self.cells.append( ( pipe, cell ) )

    def children( self ) :
        return ( self.cells, )

    def dump( self ) :
        txt = ''.join([ pipe + ''.join([ t.dump() for t in fmttxts ])
                        for fmttxts, pipe in self.cells ])
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'table_cells: ' )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        cellcount = 1
        for fmttxts, pipe in self.cells :
            buf.write( lead + '(cell %s)\n' % cellcount )
            cellcount += 1
            for item in fmttxts :
                item.show( buf, offset + 2, attrnames, showcoord )


class Lists( Node ) :
    """Wiki class to handle `orderedlists` and `unorderedlists` grammar."""

    def __init__( self, list ) :
        self.list = [ list ]

    def appendlist( self, list ) :
        self.list.append( list )

    def children( self ) :
        return tuple(self.list)

    def dump( self ) :
        return ''.join([ c.dump() for c in self.list ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        if showcoord :
            buf.write( ' (at %s)' % self.coord )

        for c in self.children() :
            c.show( buf, offset + 2, attrnames, showcoord )


class List( Node ) :
    """Wiki class to handle `orderedlist` and `unorderedlist` grammar."""

    def __init__( self, listtype, listmarkup, formatted_texts, newline ) :
        self.listtype        = listtype
        self.formatted_texts = formatted_texts
        self.listmarkup      = listmarkup
        self.newline         = Newline( newline )

    def children( self ) :
        return ( self.listtype, self.formatted_texts, self.listmarkup,
                 self.newline )

    def dump( self ) :
        txt     =  self.listmarkup
        txt     += ''.join([ c.dump() for c in self.formatted_texts ])
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

        for fmttxt in self.formatted_texts :
            fmttxt.show( buf, offset + 2, attrnames, showcoord )


class FormattedText( Node ) :
    """Wiki class to handle `formatted_text` grammar."""

    def __init__( self, type, contlist  ) :
        self.type     = type
        self.contlist = contlist

    def children( self ) :
        return (self.type, self.contlist)

    def dump( self ) :
        types   = {
                    FORMAT_BOLD          : M_BOLD,
                    FORMAT_ITALIC        : M_ITALIC,
                    FORMAT_UNDERLINE     : M_UNDERLINE,
                    FORMAT_SUPERSCRIPT   : M_SUPERSCRIPT,
                    FORMAT_SUBSCRIPT     : M_SUBSCRIPT,
                    FORMAT_BOLDITALIC    : M_BOLDITALIC,
                    FORMAT_BOLDITALICUNDERLINE : M_BOLDITALICUNDERLINE,
                    FORMAT_NON           : '',
                    FORMAT_EMPTY         : '',
                  }
        txt     = types[self.type] + ''.join([ c.dump() for c in self.contlist ]) 
        txt    += types[self.type]
        return txt

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write( lead + 'formatted_text: %s ' % self.type )

        if showcoord :
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')

        for item in self.contlist :
            item.show( buf, offset + 2, attrnames, showcoord )


class Link( Node ) :
    """Wiki class to handle `link` grammer."""

    def __init__( self, link ) :
        self.link      = link

    def children( self ) :
        return ( self.link, )

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

    def dump( self ) :
        return (self.type == TEXT_ESCAPED and ('~'+self.text)) or self.text

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

    def dump( self ) :
        return self.newline

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ) :
        lead = ' ' * offset
        buf.write(lead + 'newline: ')
        buf.write('\n')


