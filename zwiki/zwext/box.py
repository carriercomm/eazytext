# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

import cElementTree as et

from   zwiki.zwext    import ZWExtension
from   zwiki          import split_style

box_css = {
    'color'         : 'gray',
    'border-top'    : 'thin solid #CEF2E0',
    'border-right'  : 'thin solid #CEF2E0',
    'border-bottom' : 'thin solid #CEF2E0',
    'border-left'   : 'thin solid #CEF2E0',
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

wikidoc = """
=== Box

: Description ::
    Generate a box with title and content. Text within the curly braces will be
    interpreted as the content and can contain ZWiki text as well.

keyword argument,
|= title        | optional, title string
|= titlestyle   | optional, title style string in CSS style format
|= contentstyle | optional, content style string in CSS style format

Default CSS styling for title,
> [<PRE %s >]

Default CSS styling for content,
> [<PRE %s >]

Default CSS styling for the entire extension,
> [<PRE %s >]
""" % ( title_css, cont_css, box_css )

class Box( ZWExtension ) :
    """Implements Box() wikix"""

    def __init__( self, props, nowiki, *args ) :
        self.nowiki  = nowiki
        self.title   = props.pop( 'title', '' )
        boxstyle     = props.pop( 'style', {} )
        titlestyle   = props.pop( 'titlestyle', {} )
        contentstyle = props.pop( 'contentstyle', '' )

        d_style, s_style = split_style( boxstyle )
        self.style     = s_style
        self.css   = {}
        self.css.update( box_css )
        self.css.update( props )
        self.css.update( d_style )

        d_style, s_style = split_style( titlestyle )
        self.titlestyle  = s_style
        self.title_css   = {}
        self.title_css.update( title_css )
        self.title_css.update( d_style )

        d_style, s_style  = split_style( contentstyle )
        self.contentstyle = s_style
        self.cont_css     = {}
        self.cont_css.update( cont_css )
        self.cont_css.update( d_style )

    def tohtml( self ) :
        from   zwiki.zwparser import ZWParser

        style = '; '.join([k + ' : ' + self.css[k] for k in self.css])
        if self.style :
            style += '; ' + self.style + '; '
        box_div       = et.Element( 'div', { 'style' : style } )

        titlestyle = '; '.join([ k + ' : ' + self.title_css[k] for k in self.title_css ])
        if self.titlestyle  :
            titlestyle += '; ' + self.titlestyle + '; '
        if self.title :
            title_div        = et.Element( 'div', { 'style' : titlestyle } )
            title_div.text   = self.title or ' ' # Dont keep text empty
            box_div.insert( 0, title_div )

        if self.nowiki :
            self.contentstyle \
                and self.cont_css.setdefault( 'style', self.contentstyle )
            zwparser        = ZWParser( lex_optimize=False,
                                        yacc_optimize=False,
                                        style=self.cont_css )
            tu              = zwparser.parse( self.nowiki, debuglevel=0 )
            self.nowiki_h   = tu.tohtml()
            try :
                cnode = et.fromstring( self.nowiki_h )
                cnode.text = ' '                # Don't keep text empty
            except :
                box_div.insert( 1, et.fromstring( '<div> </div>' ))
            else :
                box_div.insert( 1, cnode )
        html = ( (self.title or self.nowiki) and et.tostring( box_div ) ) or ''
        return html
