# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager

from   eazytext.interfaces  import IEazyTextMacro, IEazyTextMacroFactory
from   eazytext.lib         import lhtml

gsm = getGlobalSiteManager()

class Html( object ) :
    """
    h3. Html

    : Description ::
        Embed HTML text within wiki doc. Try to use ''~[< ... ~>]'' markup
        first, if advanced styling is required for the embedded HTML text,
        then this macro can come in handy.
    : Example ::
        [<PRE {{ Html( '<b>hello world</b>' ) }} >]

    Positional arguments,
    |= html | HTML text
    """
    implements( IEazyTextMacro )

    def __init__( self, html='' ) :
        self.html  = html

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node ) :
        return self.html

    def on_posthtml( self, node ) :
        pass

class HtmlFactory( object ):
    implements( IEazyTextMacroFactory )
    def __call__( self, argtext ):
        return eval( 'Html( %s )' % argtext )

# Register this plugin
gsm.registerUtility( HtmlFactory(), IEazyTextMacroFactory, 'Html' )
