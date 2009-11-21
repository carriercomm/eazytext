"""Implementing the Clear macro"""

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

class Clear( ZWMacro ) :
    """Implements Clear() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        html  = '<div style="%s"></div>' % self.style
        return html
