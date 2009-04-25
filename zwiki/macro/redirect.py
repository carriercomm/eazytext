"""Implementing the Redirect macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


from   zwiki.macro  import ZWMacro

class Redirect( ZWMacro ) :
    """Implements Redirect() Macro"""

    def __init__( self, redireclink='' ) :
        self.redirect = redireclink

    def tohtml( self ) :
        self.macronode.parser.zwparser.redirect = self.redirect
        return ''

