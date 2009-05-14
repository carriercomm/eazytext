# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

import cElementTree as et

from   zwiki.zwext    import ZWExtension
from   zwiki          import split_style

class Html( ZWExtension ) :
    """Implements Html() wikix"""

    def __init__( self, props, nowiki ) :
        self.nowiki  = nowiki
        
        d_style, s_style = split_style( props.pop( 'style', {} ))
        self.style  = s_style
        self.css    = {}
        self.css.update( d_style )
        self.css.update( props )

    def tohtml( self ) :
        from   zwiki.zwparser import ZWParser

        style   = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style   += '; ' + self.style + '; '
        box_div = et.Element( 'div', { 'style' : style } )
        box_div.insert( 0, et.fromstring( self.nowiki ))
        html = ( self.nowiki and et.tostring( box_div ) ) or ''
        return html

