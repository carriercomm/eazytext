"""Implementing the Span macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro, css_props

style_props = {}
style_props.update( css_props )

class Span( ZWMacro ) :
    """Implements Span() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.text = len(args) > 0 and args[0] or ''
        self.prop_values = {
            'color'     : 'gray',
            'padding'   : '2px',
        }
        self.prop_values.update( kwargs )

    def tohtml( self ) :
        style     = ';'.join([ style_props[k] + self.prop_values[k]
                               for k in style_props if k in self.prop_values ])
        span      = et.Element( 'span', { 'style' : style } )
        span.text = self.text
        return et.tostring( span )
