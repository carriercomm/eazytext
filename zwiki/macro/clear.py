# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle, lhtml

wikidoc = """
=== Clear

: Description :: 
    Styling macro to clear the DOM elements on both sides, warding off from
    floating effects

Positional arguments, None
"""

class Clear( ZWMacro ) :

    template = '<div class="zwm-clear" style="%s"></div>'

    def __init__( self, *args, **kwargs ) :
        self.style = constructstyle( kwargs )

    def tohtml( self ) :
        html = self.template % self.style
        return html
