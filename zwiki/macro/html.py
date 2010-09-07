# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


#import xml.etree.cElementTree as et
import lxml.html    as lhtml

from   zwiki.macro  import ZWMacro

wikidoc = """
=== Html

: Description ::
    Embed HTML text within wiki doc. Try to use ''~[< ... ~>]'' markup first,
    if advanced styling is required for the embedded HTML text, then this
    macro can come in handy.

Positional arguments,
|= html | HTML text

CSS styling accepted as optional keyword arguments
"""

class Html( ZWMacro ) :

    def __init__( self, html='' ) :
        self.html  = html
        self.style = ''
        self.css   = {}

    def tohtml( self ) :
        return self.html
