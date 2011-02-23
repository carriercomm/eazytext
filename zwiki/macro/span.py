# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Implementing the Span macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle, lhtml

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
        span      = lhtml.Element( 'span', { 'style' : self.style } )
        span.text = self.text or ' '    # Don't keep the text empty
        html      = ( self.text and lhtml.tostring( span ) ) or ''
        return html
