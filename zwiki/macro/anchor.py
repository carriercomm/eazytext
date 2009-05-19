"""Implementing the Anchor macro""" 
# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style

class Anchor( ZWMacro ) :
    """Implements Anchor() Macro"""

    def __init__( self, *args, **kwargs ) :
        args        = list( args )
        self.anchor = args and args.pop( 0 ) or ''
        self.text   = args and args.pop( 0 ) or '&#167;'

        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = {}
        self.css.update( d_style )
        self.css.update( kwargs )

    def tohtml( self ) :
        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; ' + self.style + '; '
        html  = '<a name="' + self.anchor + '" style="' + style + '">' + \
                self.text + '</a>'
        return html
