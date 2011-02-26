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
=== Anchor

: Description ::
    Create an anchor in the document which can be referenced else-wehere.

Positional arguments,

|= anchor | anchor name as fragment, goes under @name attribute
|= text   | optional, text to be display at the anchor
"""

class Anchor( ZWMacro ) :

    template = '<a class="zwm-anchor" name="%s" style="%s"> %s </a>'

    def __init__( self, *args, **kwargs ) :
        args = list( args )
        self.anchor = args and args.pop( 0 ) or ''
        self.text = args and args.pop( 0 ) or '&#167;'
        self.style = constructstyle( kwargs )

    def tohtml( self ) :
        html = self.template % ( self.anchor, self.style, self.text )
        return html
