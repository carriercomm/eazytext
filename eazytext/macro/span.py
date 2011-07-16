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

class Span( object ) :
    tmpl = '<span class="etm-span" style="%s"> %s </span>'

    def __init__( self, *args, **kwargs ) :
        self.text = len(args) > 0 and args[0] or ''
        self.style = constructstyle( kwargs )

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node ) :
        return self.tmpl % ( self.style, self.text )

    def on_posthtml( self, node ) :
        pass

class SpanFactory( object ):
    """
    h3. Span

    : Description ::
        Create a span element. Try using ~``...~`` markup to generate span
        elements, if advanced styling is required, this macro can come in handy.
        Accepts CSS styles for keyword arguments.
    : Example ::
        [<PRE {{ Span( 'hello world' ) }} >]

    Positional arguments,
    |= text   | optional, text for the span element
    """
    implements( IEazyTextMacroFactory )
    def __call__( self, argtext ):
        return eval( 'Span( %s )' % argtext )


# Register this plugin
gsm.registerUtility( SpanFactory(), IEazyTextMacroFactory, 'Span' )
