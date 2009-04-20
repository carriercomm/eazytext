# -*- coding: utf-8 -*-

# gotcha : none
# notes  : none
# todo   : none

import cElementTree as et

from   zwiki.zwext  import ZWExtension, css_props

style_props = {}
style_props.update( css_props )

titlestyle_props = {
        'titlecolor'   : 'color : ',
        'titlebg'      : 'background : ',
        'titlemb'      : 'margin-bottom : ',
        'titlefontw'   : 'font-weight : ',
        'titlepadding' : 'padding : ',
}

class Box( ZWExtension ) :
    """Implements Box() wikix"""

    def __init__( self, props, nowiki ) :
        self.nowiki     = nowiki
        self.title      = props.pop( 'title', '' )
        self.titlestyle = props.pop( 'titlestyle', '' )

        self.prop_values = {
                'color'        : 'gray',
                'bordercolor'  : '#CEF2E0',
                'pos'          : 'relative',
                'float'        : 'left',
        }
        self.prop_values.update( props )

        self.titleprop_values = {
                'titlecolor'   : '',
                'titlebg'      : '#CEF2E0',
                'titlemb'      : '5px',
                'titlefontw'   : 'bold',
                'titlepadding' : '3px',
        }
        self.titleprop_values.update( self.titlestyle )

    def tohtml( self ) :
        box_style   = ';'.join([ style_props[k] + self.prop_values[k]
                                 for k in style_props if k in self.prop_values])
        box_div     = et.Element( 'div', { 'style' : box_style } )

        title_style = ';'.join([ titlestyle_props[k] + self.titleprop_values[k]
                                 for k in titlestyle_props ])
        if self.title :
            title_div        = et.Element( 'div', { 'style' : title_style } )
            title_div.text   = self.title
            box_div.insert( 0, title_div )
        if self.nowiki :
            content_div      = et.Element( 'div', { 'style' : 'padding : 3px;' } )
            content_div.text = self.nowiki
            box_div.insert( 1, content_div )
        return et.tostring( box_div )
