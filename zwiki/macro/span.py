"""Implementing the Span macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style

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
        self.text = len(args) > 0 and args[0] or ''

        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = {}
        self.css.update( css )
        self.css.update( d_style )
        self.css.update( kwargs )

    def tohtml( self ) :
        style     = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style     += '; ' + self.style + '; '
        span      = et.Element( 'span', { 'style' : style } )
        span.text = self.text
        html      = ( self.text and et.tostring( span ) ) or ''
        return html
