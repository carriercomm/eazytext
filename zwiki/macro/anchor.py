"""Implementing the Anchor macro""" 
# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None


import cElementTree as et

from   zwiki.macro  import ZWMacro

class Anchor( ZWMacro ) :
    """Implements Anchor() Macro"""

    def __init__( self, *args, **kwargs ) :
        args        = list( args )
        style       = kwargs.pop( 'style', {} )
        self.anchor = args and args.pop( 0 ) or ''
        self.text   = args and args.pop( 0 ) or '&#167;'
        self.css = {}
        self.css.update( kwargs )
        self.css.update( style )

    def tohtml( self ) :
        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        html  = '<a name="' + self.anchor + '" style="' + style + '">' + \
                self.text + '</a>'
        return html
