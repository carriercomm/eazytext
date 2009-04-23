"""Implementing the Span macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro

css = {
    'color'          : 'gray',
    'padding-top'    : '2px',
    'padding-right'  : '2px',
    'padding-bottom' : '2px',
    'padding-left'   : '2px',
}

class Span( ZWMacro ) :
    """Implements Span() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.text       = len(args) > 0 and args[0] or ''
        self.css = {}
        self.css.update( css )
        self.css.update( kwargs )

    def tohtml( self ) :
        style     = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        span      = et.Element( 'span', { 'style' : style } )
        span.text = self.text
        html      = ( self.text and et.tostring( span ) ) or ''
        return html
