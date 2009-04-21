# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#   1. Add TOC with pos='inline'


import cElementTree as et

from   zwiki.macro  import ZWMacro, css_props

alphanum    = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
random_word = lambda : ''.join([ choice(alphanum) for i in range(4) ])

style_props = {}
style_props.update( css_props )

htags = {
    'h1' : 'margin-left : 2px; ',
    'h2' : 'margin-left : ',
    'h3' : 'margin-left : ',
    'h4' : 'margin-left : ',
    'h5' : 'margin-left : ',
}

def _maketoc( node, toc_div ) :
    for n in node.getchildren() :
        if n.tag in htags :
            item      = n.makeelement( 'div', { 'style' : htags[n.tag] } )
            text      = n.getchildren()[0].get( 'name' ) 
            link      = item.makeelement( 'a', { 'href' : '#' + text } )
            link.text = text
            item.append( link )
            toc_div.append( item )
        _maketoc( n, toc_div )
    return

class Toc( ZWMacro ) :
    """Implements Toc() Macro"""

    def __init__( self, *args, **kwargs ) :
        ind = int(kwargs.pop( 'indent', '1' ))
        htags.update(
            [ ( h, htags[h] + str(ind * n) + 'em;' )
              for h, n in [ ('h2', 1), ('h3', 2), ('h4', 3), ('h5', 4) ]]
        )
        self.prop_values = {
                'bg'           : '#f8f7bc',
                'pos'          : 'relative',
                'float'        : 'left',
                'margin'       : '10px',
                'padding'      : '3px',
        }
        self.prop_values.update( kwargs )

    def tohtml( self ) :
        return ''

    def on_posthtml( self ) :
        toc_style = ';'.join([ style_props[k] + self.prop_values[k]
                                 for k in style_props if k in self.prop_values])
        zwparser  = self.macronode.parser.zwparser
        try :
            htmltree  = et.fromstring( zwparser.html )
            toc_div   = htmltree.makeelement(
                             'div', 
                             { 'name' : 'TOC', 'style' : toc_style, }
                        )
            _maketoc( htmltree, toc_div )
            wiki_div = htmltree.makeelement( 'div', { 'name' : 'wikipage', })
            wiki_div.append( toc_div )
            wiki_div.append( htmltree )
            html = et.tostring( wiki_div )
        except :
            html = 'Unable to generate the TOC, Wiki page not properly formed !'
            html += zwparser.html
        zwparser.html = html
