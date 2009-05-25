"""Implementing the Images macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style

css = {
    'margin'    : '10px',
    'padding'   : '0px',
    'border'    : '0px',
}

class Images( ZWMacro ) :
    """Implements Images() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.imgsources = args

        self.alt    = kwargs.pop( 'alt', '' )
        self.height = kwargs.pop( 'height', None )
        self.width  = kwargs.pop( 'width', None )
        self.cols   = int( kwargs.pop( 'cols', '3' ))

        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = css
        self.css.update( d_style )
        self.css.update( kwargs )

    def tohtml( self ) :
        style = '; '.join([k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; ' + self.style + '; '
        hattr = self.height and ( ' height="' + self.height + '" ' ) or ''
        wattr = self.width and ( ' width="' + self.width + '" ' ) or ''

        offset     = 0
        imgsources = list(self.imgsources[:])
        gallerydiv = et.Element( 'div', {'style' : 'display : table;'} )
        while imgsources :
            rowdiv = et.Element( 'div', {'style' : 'display : table-row;'} )
            for i in range( self.cols ) :
                if not imgsources :
                    break
                src    = imgsources.pop( 0 )
                coldiv = et.Element('div', {'style' : 'display : table-cell;'})
                img    = '<img ' + hattr + wattr + ' src="' + src + '" alt="' + \
                        self.alt + '" style="' + style +'"></img>'
                coldiv.append( et.fromstring( img ))
                rowdiv.append( coldiv )
            gallerydiv.append( rowdiv )
        html = et.tostring( gallerydiv )
        return html
