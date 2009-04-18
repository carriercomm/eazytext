# -*- coding: utf-8 -*-

# gotcha : none
# notes  : none
# todo   : none


from   zwiki.zwext import ZWExtension


styles = [
    ('color',  'color : '),
    ('bg',     'background : '),
    ('border', 'border : '),
]

stdstyle = 'padding : 5px 5px 5px 5px; border : thin solid gray;' + \
           'margin  : 2px 2px 2px 2px;' + \
           'background : ButtonHighlight;'

class Box( ZWExtension ) :
    """Implements Box() wikix"""

    def __init__( self, props, nowiki ) :
        self.nowiki = nowiki
        self.color  = props.get( 'color', '' )
        self.bg     = props.get( 'bg', '' )
        self.border = props.get( 'border', '' )
        self.style  = props.get( 'style', '' )

    def tohtml( self ) :
        attrs = dir(self)
        style = ';'.join([ attr + getattr( self, item )
                           for item, attr in styles if getattr( self, item, '' ) ])
        style = stdstyle + style + '; ' + self.style + ';'
        html  = '<div ' + 'style="'+style+'">' + self.nowiki  + '</div>'
        return html
