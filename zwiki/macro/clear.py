# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

css = {
    'clear' : 'both',
}

wikidoc = """
=== Clear

: Description :: 
    Styling macro to clear the DOM elements on both sides, warding off from
    floating effects

Positional arguments, None

Default CSS styling,
> [<PRE %s >]

CSS styling accepted as optional keyword arguments
""" % css

class Clear( ZWMacro ) :

    def __init__( self, *args, **kwargs ) :
        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        html  = '<div style="%s"></div>' % self.style
        return html
