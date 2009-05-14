"""Implementing the Clear macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style

css = {
    'clear' : 'both'
}

class Clear( ZWMacro ) :
    """Implements Clear() Macro"""

    def __init__( self, *args, **kwargs ) :
        style    = kwargs.pop( 'style', {} )

        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = {}
        self.css.update( css )
        self.css.update( d_style )
        self.css.update( kwargs )

    def tohtml( self ) :
        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; ' + self.style + '; '
        html  = '<div style="' + style + '"></div>'
        return html
