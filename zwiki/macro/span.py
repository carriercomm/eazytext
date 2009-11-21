"""Implementing the Span macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

css = {
    'color'   : 'gray',
    'padding' : '2px',
}

class Span( ZWMacro ) :
    """Span() macro"""

    def __init__( self, *args, **kwargs ) :
        """
        args    : span text
        kwargs  : CSS styling as key, value pairs.
                  special key, 'style' is accepted
        """
        self.text  = len(args) > 0 and args[0] or ''
        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        span      = et.Element( 'span', { 'style' : self.style } )
        span.text = self.text
        html      = ( self.text and et.tostring( span ) ) or ''
        return html
