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

class Anchor( object ):
    implements( IEazyTextMacro )
    template = '<a class="etm-anchor" name="%s" style="%s"> %s </a>'

    def __init__( self, *args, **kwargs ):
        args = list( args )
        self.anchor = args and args.pop( 0 ) or ''
        self.text = args and args.pop( 0 ) or '&#167;'
        self.style = constructstyle( kwargs )

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node ) :
        return self.template % ( self.anchor, self.style, self.text )

    def on_posthtml( self, node ) :
        pass

class AnchorFactory( object ):
    """
    h3. Anchor

    : Description ::
        Create an anchor in the document which can be referenced else-wehere.
        Accepts CSS styles for keyword arguments.
    : Example ::
        [<PRE {{ Anchor( 'anchorname', 'display-text' ) }} >]

    Positional arguments,

    |= anchor | anchor name as fragment, goes under @name attribute
    |= text   | optional, text to be display at the anchor
    """
    implements( IEazyTextMacroFactory )
    def __call__( self, argtext ):
        return eval( 'Anchor( %s )' % argtext )

# Register this plugin
gsm.registerUtility( AnchorFactory(), IEazyTextMacroFactory, 'Anchor' )
