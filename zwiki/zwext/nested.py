# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

from   zwiki.zwext  import ZWExtension
from   zwiki        import split_style, constructstyle, lhtml

doc = """
=== Nested

: Description ::
    Simpley nest another ZWiki document / text within the current
    document. Property key-value pairs accepts CSS styling attributes.
"""


class Nested( ZWExtension ) :

    tmpl = '<div class="zwext-nested"> %s </div>'
    
    def __init__( self, props, nowiki, *args ) :
        self.nowiki = nowiki
        self.style = constructstyle( props )

    def tohtml( self ) :
        from   zwiki.zwparser import ZWParser

        if self.nowiki :
            zwparser = ZWParser(
                            nested=True,
                            style=self.style,
                            skin=None,
                            lex_optimize=False,
                            yacc_optimize=False,
                       )
            tu = zwparser.parse( self.nowiki, debuglevel=0 )
            try :
                html = self.tmpl % ( tu.tohtml() )
            except :
                html = self.tmpl % ''
        return html

Nested._doc = doc
