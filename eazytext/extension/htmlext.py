# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager

from   eazytext.interfaces  import IEazyTextExtension, \
                                   IEazyTextExtensionFactory
from   eazytext.lib         import split_style, constructstyle, lhtml

gsm = getGlobalSiteManager()


doc = """
=== Htmlext
: Description :: Raw html text.
"""

tmpl = 'div class="etext-html" style="%s"> %s </div>'

class Htmlext( object ) :
    implements( IEazyTextExtension )
    def __init__( self, props, nowiki, *args ) :
        self.nowiki  = nowiki
        
        d_style, s_style = split_style( props.pop( 'style', {} ))
        self.style  = s_style
        self.css = {}
        self.css.update( d_style )
        self.css.update( props )

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node ) :
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

    def on_posthtml( self, node ) :
        pass

class HtmlextFactory( object ):
    _doc = doc
    implements( IEazyTextExtensionFactory )
    def __call__( self, *args ):
        return Htmlext( *args )

# Register this plugin
gsm.registerUtility( HtmlextFactory(), IEazyTextExtensionFactory, 'Htmlext' )
