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

wikidoc = """
=== Span

: Description ::
    Create a span element. Try using ~``...~`` markup to generate span
    elements, if advanced styling is required, this macro can come in handy.

Positional arguments,
|= text   | optional, text for the span element

Default CSS styling,
> [<PRE %s >]

CSS styling accepted as optional keyword arguments
""" % css

class Span( ZWMacro ) :

    def __init__( self, *args, **kwargs ) :
        self.text  = len(args) > 0 and args[0] or ''
        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        span      = et.Element( 'span', { 'style' : self.style } )
        span.text = self.text
        html      = ( self.text and et.tostring( span ) ) or ''
        return html
