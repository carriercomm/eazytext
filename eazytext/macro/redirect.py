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

class Redirect( object ) :
    """
    Just sets the ``redirect`` attribute in
    self.macronode.parser.etparser.redirect to the the argument that is passed
    """
    implements( IEazyTextMacro )
    def __init__( self, redireclink='' ) :
        self.redirect = redireclink

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node ) :
        self.macronode.parser.etparser.redirect = self.redirect
        return ''

    def on_posthtml( self, node ) :
        pass

class RedirectFactory( object ):
    implements( IEazyTextMacroFactory )
    def __call__( self, argtext ):
        return eval( 'Redirect( %s )' % argtext )

# Register this plugin
gsm.registerUtility( RedirectFactory(), IEazyTextMacroFactory, 'Redirect' )
