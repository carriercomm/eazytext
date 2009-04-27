# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

import cElementTree as et

from   zwiki.zwext    import ZWExtension

class Html( ZWExtension ) :
    """Implements Html() wikix"""

    def __init__( self, props, nowiki ) :
        self.nowiki       = nowiki
        self.css = {}
        self.css.update( props )

    def tohtml( self ) :
        from   zwiki.zwparser import ZWParser

        style   = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        box_div = et.Element( 'div', { 'style' : style } )
        box_div.insert( 0, et.fromstring( self.nowiki ))
        html = ( self.nowiki and et.tostring( box_div ) ) or ''
        return html

