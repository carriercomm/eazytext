# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

import cElementTree as et

from   zwiki.zwext  import ZWExtension
from   zwiki        import split_style, constructstyle

css = { }

wikidoc = """
=== Nested

: Description ::
    Simpley nest another ZWiki document / text within the current
    document.
"""

class Nested( ZWExtension ) :
    """Implements Nested() wikix"""

    def __init__( self, props, nowiki ) :

        self.nowiki = nowiki
        self.style  = constructstyle( props, defcss=css )

    def tohtml( self ) :
        from   zwiki.zwparser import ZWParser

        self.nowiki_h = '<div></div>'
        if self.nowiki :
            zwparser        = ZWParser( lex_optimize=False,
                                        yacc_optimize=False,
                                        style=self.style )
            tu              = zwparser.parse( self.nowiki, debuglevel=0 )
            try :
                self.nowiki_h = tu.tohtml()
            except :
                pass
        return self.nowiki_h
