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

wikidoc = """
=== Span

: Description ::
    Create a span element. Try using ~``...~`` markup to generate span
    elements, if advanced styling is required, this macro can come in handy.

Positional arguments,
|= text   | optional, text for the span element
"""

class Span( ZWMacro ) :

    tmpl = '<span class="zwm-span" style="%s"> %s </span>'

    def __init__( self, *args, **kwargs ) :
        self.text = len(args) > 0 and args[0] or ''
        self.style = constructstyle( kwargs )

    def tohtml( self ) :
        html = self.tmpl % ( self.style, self.text )
        return html
