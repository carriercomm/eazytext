"""Implementing the Image macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style

css = {
    'margin'    : '0px',
    'padding'   : '0px',
    'border'    : '0px',
}

class Image( ZWMacro ) :
    """Implements Image() Macro"""

    def __init__( self, src, alt, **kwargs ) :
        self.src    = src
        self.alt    = alt
        self.height = kwargs.pop( 'height', None )
        self.width  = kwargs.pop( 'width', None )
        self.href   = kwargs.pop( 'href', '' )
        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = css
        self.css.update( d_style )
        self.css.update( kwargs )

    def tohtml( self ) :
        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; ' + self.style + '; '
        hattr = self.height and ( ' height="' + hattr + '" ' ) or ''
        wattr = self.width and ( ' width="' + wattr + '" ' ) or ''
        img   = '<img ' + hattr + wattr + ' src="' + self.src + '" alt="' + \
                self.alt + '" style="' + style +'"></img>'
        if self.href :
            href = et.Element( 'a', { 'href' : self.href } )
            href.append( et.fromstring( img ))
            html = et.tostring( href )
        else :
            html = img
        return html
