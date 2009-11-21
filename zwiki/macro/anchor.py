"""Implementing the Anchor macro""" 
# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

class Anchor( ZWMacro ) :
    """Implements Anchor() Macro"""

    def __init__( self, *args, **kwargs ) :
        args        = list( args )
        self.anchor = args and args.pop( 0 ) or ''
        self.text   = args and args.pop( 0 ) or '&#167;'

        self.style  = constructstyle( kwargs )

    def tohtml( self ) :
        html = '<a name="%s" style="%s">%s</a>' % \
                        ( self.anchor, self.style, self.text )
        return html
