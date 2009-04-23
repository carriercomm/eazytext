# -*- coding: utf-8 -*-

# gotcha : none
# notes  : none
# todo   : none

import cElementTree as et

from   zwiki.zwext    import ZWExtension

box_css = {
    'color'         : 'gray',
    'border-top'    : 'thin solid #CEF2E0',
    'border-right'  : 'thin solid #CEF2E0',
    'border-bottom' : 'thin solid #CEF2E0',
    'border-left'   : 'thin solid #CEF2E0',
    'position'      : 'relative',
    'float'         : 'left',
}
title_css = {
    'color'          : '',
    'background'     : '#CEF2E0',
    'margin-bottom'  : '5px',
    'font-weight'    : 'bold',
    'padding-top'    : '3px',
    'padding-right'  : '3px',
    'padding-bottom' : '3px',
    'padding-left'   : '3px'
}
cont_css = {
    'padding-top'    : '3px',
    'padding-right'  : '3px',
    'padding-bottom' : '3px',
    'padding-left'   : '3px',
}

class Box( ZWExtension ) :
    """Implements Box() wikix"""

    def __init__( self, props, nowiki ) :
        self.nowiki       = nowiki
        self.title        = props.pop( 'title', '' )
        self.titlestyle   = props.pop( 'titlestyle', '' )
        self.contentstyle = props.pop( 'contentstyle', '' )

        self.box_css = {}
        self.box_css.update( box_css )
        self.box_css.update( props )
        self.title_css = {}
        self.title_css.update( title_css )
        self.title_css.update( self.titlestyle )
        self.cont_css = {}
        self.cont_css.update( cont_css )
        self.cont_css.update( self.contentstyle )

    def tohtml( self ) :
        from   zwiki.zwparser import ZWParser

        box_style     = '; '.join([ k + ' : ' + self.box_css[k]
                                    for k in self.box_css ])
        box_div       = et.Element( 'div', { 'style' : box_style } )

        title_style   = '; '.join([ k + ' : ' + self.title_css[k]
                                    for k in self.title_css ])
        content_style = '; '.join([ k + ' : ' + self.cont_css[k]
                                    for k in self.cont_css ])
        if self.title :
            title_div        = et.Element( 'div', { 'style' : title_style } )
            title_div.text   = self.title
            box_div.insert( 0, title_div )
        if self.nowiki :
            zwparser        = ZWParser(lex_optimize=False, yacc_optimize=False)
            tu              = zwparser.parse( self.nowiki, debuglevel=0 )
            self.nowiki_h   = tu.tohtml()
            content_div     = et.Element( 'div', { 'style' : content_style } )
            content_div.insert( 0, et.fromstring( self.nowiki_h ))
            box_div.insert( 1, content_div )
        html = ( (self.title or self.nowiki) and et.tostring( box_div ) ) or ''
        return html
