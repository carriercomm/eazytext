"""Implementing the Html macro""" 
# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro

class Html( ZWMacro ) :
    """Implements Html() Macro"""

    def __init__( self, html='' ) :
        self.html  = html
        self.style = ''
        self.css   = {}

    def tohtml( self ) :
        return self.html

