"""Implementing the Image macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

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

        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        hattr = self.height and ( 'height="%s"' % self.height ) or ''
        wattr = self.width and ( 'width="%s"' % self.width ) or ''
        img   = '<img %s %s src="%s" alt="%s" style="%s"></img>' % \
                    ( hattr, wattr, self.src, self.alt, self.style )
        # If the image is a link, enclose it with a 'anchor' dom-element.
        if self.href :
            href = et.Element( 'a', { 'href' : self.href } )
            href.append( et.fromstring( img ))
            html = et.tostring( href )
        else :
            html = img
        return html
