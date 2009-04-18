"""Implementing the Box macro"""

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none


import xml.etree.ElementTree as et

from   zwiki.macro           import ZWMacro, styles

class Box( ZWMacro ) :
    """Implements Box() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.text        = len(args) > 0 and args[0] or ''
        self.color       = kwargs.get( 'color', 'gray' )
        self.bordercolor = kwargs.get( 'bordercolor', '' )
        self.bg          = kwargs.get( 'bg', '' )
        self.border      = kwargs.get( 'border', '' )
        self.margin      = kwargs.get( 'margin', '' )
        self.padding     = kwargs.get( 'padding', '2px' )
        self.style       = kwargs.get( 'style', '' )

    def tohtml( self ) :
        style     = ';'.join([ styles[prop] + getattr( self, prop )
                               for prop in styles if getattr( self, prop ) ])
        style     = style + '; ' + self.style + ';'
        span      = et.Element( 'span', { 'style' : style } )
        span.text = self.text
        return et.tostring( span )
