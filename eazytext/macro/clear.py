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
from   eazytext.lib         import split_style, constructstyle, lhtml

gsm = getGlobalSiteManager()

class Clear( object ) :
    implements( IEazyTextMacro )
    template = '<div class="etm-clear" style="%s"></div>'

    def __init__( self, *args, **kwargs ) :
        self.style = constructstyle( kwargs )

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node ) :
        return self.template % self.style

    def on_posthtml( self, node ) :
        pass

class ClearFactory( object ):
    """
    h3. Clear

    : Description :: 
        Styling macro to clear the DOM elements on both sides, warding off from
        floating effects. Accepts CSS styles for keyword arguments.
    : Example ::
        [<PRE {{ Clear() }} >]

    Positional arguments, //None//
    """
    implements( IEazyTextMacroFactory )
    def __call__( self, argtext ):
        return eval( 'Clear( %s )' % argtext )

# Register this plugin
gsm.registerUtility( ClearFactory(), IEazyTextMacroFactory, 'Clear' )
