# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

from   zope.component       import getGlobalSiteManager

from   eazytext.extension   import Extension
from   eazytext.interfaces  import IEazyTextExtensionFactory
from   eazytext.lib         import lhtml

gsm = getGlobalSiteManager()

doc = """
=== Htmlext
: Description :: Raw html text.
"""

tmpl = 'div class="etext-html" style="%s"> %s </div>'

class Htmlext( Extension ) :
    _doc = doc
    def __init__( self, props, nowiki, *args ) :
        self.nowiki  = nowiki
        
        d_style, s_style = split_style( props.pop( 'style', {} ))
        self.style  = s_style
        self.css = {}
        self.css.update( d_style )
        self.css.update( props )

    def __call__( self, argtext ):
        return eval( 'Htmlext( %s )' % argtext )

    def html( self, node, igen, *args, **kwargs ) :
        fn = lambda (k, v) : '%s : %s' % (k,v)
        style = '; '.join(map( fn, self.css.items() ))
        if self.style :
            style += '; ' + self.style + '; '

        try :
            boxnode = lhtml.fromstring( self.nowiki )
        except :
            if self.extnode.parser.etparser.debug : raise
            html = tmpl % (style, '')
        else :
            html = tmpl % (style, lhtml.tostring(boxnode) )
        return html

# Register this plugin
gsm.registerUtility( Htmlext(), IEazyTextExtensionFactory, 'Htmlext' )
