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
=== Nested

: Description ::
    Nest another EazyText document / text within the current
    document. Property key-value pairs accepts CSS styling attributes.
"""


class Nested( object ) :

    tmpl = '<div class="etext-nested"> %s </div>'
    implements( IEazyTextExtension )
    
    def __init__( self, props, nowiki, *args ) :
        self.nowiki = nowiki
        self.style = constructstyle( props )

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node) :
        from   eazytext.parser import ETParser

        if self.nowiki :
            etparser = ETParser(
                            nested=True,
                            style=self.style,
                            skin=None,
                            lex_optimize=False,
                            yacc_optimize=False,
                       )
            tu = etparser.parse( self.nowiki, debuglevel=0 )
            try :
                html = self.tmpl % ( tu.tohtml() )
            except :
                if self.extnode.parser.etparser.debug : raise
                html = self.tmpl % ''
        return html

    def on_posthtml( self, node ) :
        pass

class NestedFactory( object ):
    implements( IEazyTextExtensionFactory )
    def __call__( self, *args ):
        return Nested( *args )

# Register this plugin
gsm.registerUtility( NestedFactory(), IEazyTextExtensionFactory, 'Nested' )
NestedFactory._doc = doc
