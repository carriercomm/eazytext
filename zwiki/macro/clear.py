"""Implementing the Clear macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro, css_props

style_props = {}
style_props.update( css_props )

class Clear( ZWMacro ) :
    """Implements Clear() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.prop_values = {
                'clear' : 'both'
        }
        self.prop_values.update( kwargs )

    def tohtml( self ) :
        style = ';'.join([ style_props[k] + self.prop_values[k]
                           for k in style_props if k in self.prop_values ])
        html  = '<div style="' + style + '"></div>'
        return html
