"""Implementing the Clear macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro

css = {
    'clear' : 'both'
}

class Clear( ZWMacro ) :
    """Implements Clear() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.css = {}
        self.css.update( css )
        self.css.update( kwargs )

    def tohtml( self ) :
        style     = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        html  = '<div style="' + style + '"></div>'
        return html
