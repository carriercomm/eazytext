# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#   1. Add TOC with pos='inline'


import cElementTree as et

from   zwiki.macro  import ZWMacro

alphanum    = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
random_word = lambda : ''.join([ choice(alphanum) for i in range(4) ])

css = {
    'background'     : '#f8f7bc',
    'position'       : 'relative',
    'float'          : 'left',
    'margin-top'     : '10px',
    'margin-left'    : '10px',
    'margin-bottom'  : '10px',
    'margin-right'   : '10px',
    'padding-top'    : '3px',
    'padding-left'   : '3px',
    'padding-bottom' : '3px',
    'padding-right'  : '3px',
}

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
        ind            = int( kwargs.pop( 'indent', '1' ))
        index          = int( kwargs.pop( 'index', '-1' ))
        self.postindex = index == 0 and -1 or index
        htags.update(
            [ ( h, htags[h] + str(ind * n) + 'em;' )
              for h, n in [ ('h2', 1), ('h3', 2), ('h4', 3), ('h5', 4) ]]
        )
        self.css = {}
        self.css.update( css )
        self.css.update( kwargs )

    def tohtml( self ) :
        return ''

    def on_posthtml( self ) :
        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        zwparser  = self.macronode.parser.zwparser
        try :
            htmltree  = et.fromstring( zwparser.html )
            toc_div   = et.Element( 'div', { 'name' : 'TOC', 'style' : style, })
            _maketoc( htmltree, toc_div )
            self.posthtml = et.tostring( toc_div )
        except :
            self.posthtml = 'Unable to generate the TOC, ' +\
                            'Wiki page not properly formed ! <br></br>'
        return
