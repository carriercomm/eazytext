# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   :
#   1. Add TOC with pos='inline'


import xml.etree.ElementTree as et

from   zwiki.macro           import ZWMacro

alphanum    = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
random_word = lambda : ''.join([ choice(alphanum) for i in range(4) ])

style       = "list-style-type : none; marker-offset : 10px"
pos_style   = {
        'top'   : '',
        'left'  : 'position : relative; float : left;',
        'right' : 'position : relative; float : right;',
}

htags       = {
    'h1' : 'margin-left : 2px;',
    'h2' : 'margin-left : 1em;',
    'h3' : 'margin-left : 2em;',
    'h4' : 'margin-left : 3em;',
    'h5' : 'margin-left : 4em;',
}
def _maketoc( node, toc_div ) :
    for n in node.getchildren() :
        if n.tag in htags :
            item      = n.makeelement( 'div', { 'style' : htags[n.tag] } )
            text      = n.getchildren()[0].get( 'name' ) 
            link      = item.makeelement( 'a', { 'href' : '#'+text } )
            link.text = text
            item.append( link )
            toc_div.append( item )
        _maketoc( n, toc_div )
    return

class Toc( ZWMacro ) :
    """Implements Toc() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.pos     = kwargs.get( 'pos', 'top' )
        self.width   = kwargs.get( 'width', '' )
        self.color   = kwargs.get( 'color', '' )
        self.bg      = kwargs.get( 'bg', '' )

    def _make_toc( self, htmltree ) :
        return toc

    def tohtml( self ) :
        html = ''
        if self.pos == 'inline' :
            self.randword = random_word()
            html = '<div id="' + self.randword + '"></div>'
        else :
            self.randword = ''
        return html

    def on_posthtml( self ) :
        zwparser = self.macronode.parser.zwparser
        htmltree = et.fromstring( zwparser.html )
        style    = pos_style[self.pos] + 'margin : 10px 10px 10px 10px;'
        toc_div  = htmltree.makeelement(
                        'div', 
                        { 'name' : 'TOC', 'style' : style, }
                   )
        _maketoc( htmltree, toc_div )
        wiki_div = htmltree.makeelement(
                        'div',
                        { 'name' : 'wikipage', }
                   )
        wiki_div.append( toc_div )
        wiki_div.append( htmltree )
        zwparser.html = et.tostring( wiki_div )
