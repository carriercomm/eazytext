# -*- coding: utf-8 -*-

# gotcha : none
# notes  : none
# todo   : none

import xml.etree.ElementTree as et

from   zwiki.zwext           import ZWExtension, styles

title_styles = {
    'titlecolor'   : 'color : ',
    'titlebg'      : 'background : ',
    'titlemb'      : 'margin-bottom : ',
    'titlefontw'   : 'font-weight : ',
    'titlepadding' : 'padding : ',
}

class Box( ZWExtension ) :
    """Implements Box() wikix"""

    def __init__( self, props, nowiki ) :
        self.nowiki      = nowiki
        self.color       = props.get( 'color', 'gray' )
        self.bg          = props.get( 'bg', '' )
        self.bordercolor = props.get( 'bordercolor', '#CEF2E0' )
        self.border      = props.get( 'border', '' )
        self.margin      = props.get( 'margin', '' )
        self.padding     = props.get( 'padding', '' )
        self.width       = props.get( 'width', '' )
        self.pos         = props.get( 'pos', 'relative' )
        self.float       = props.get( 'float', 'left' )
        self.style       = props.get( 'style', '' )

        self.titlecolor  = props.get( 'titlecolor', '' )
        self.titlebg     = props.get( 'titlebg', '#CEF2E0' )
        self.titlemb     = props.get( 'titlemb', '5px' )
        self.titlefontw  = props.get( 'titlefontw', 'bold' )
        self.titlepadding= props.get( 'titlepadding', '3px' )
        self.title       = props.get( 'title', '' )

    def tohtml( self ) :
        box_style   = ';'.join([ styles[prop] + getattr( self, prop )
                                 for prop in styles if getattr( self, prop ) ])
        box_style   = box_style + '; ' + self.style
        box_div     = et.Element( 'div', { 'style' : box_style } )
        if self.title :
            title_style = ';'.join([ title_styles[prop] + getattr( self, prop )
                                     for prop in title_styles
                                     if getattr( self, prop ) ])
            title_div        = et.Element( 'div', { 'style' : title_style } )
            title_div.text   = self.title
            box_div.insert( 0, title_div )
        if self.nowiki :
            content_div      = et.Element( 'div', { 'style' : 'padding : 3px;' } )
            content_div.text = self.nowiki
            box_div.insert( 1, content_div )
        return et.tostring( box_div )
