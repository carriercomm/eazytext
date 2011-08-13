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

gsm = getGlobalSiteManager()

doc = """
=== Nested

: Description ::
    Nest another EazyText document / text within the current
    document. Property key-value pairs accepts CSS styling attributes.
"""

class Nested( Extension ) :
    tmpl = '<div class="etext-nested" style="%s"> %s </div>'
    
    def __init__( self, *args ):
        self.config = {
            'nested' : True,
            'include_skin' : False,
        }

    def __call__( self, argtext ):  # Does not take any argument.
        o = eval( 'Nested()' )
        return o

    def html( self, node, igen, *args, **kwargs ):
        from   eazytext        import Translate
        # Fetch the properties
        proplines = []
        lines = node.text.splitlines() 
        while lines and lines[0].lstrip().startswith('#') :
            proplines.append( lines.pop(0).lstrip('#') )
        text = '\n'.join( lines )
        try    :
            prop  = proplines and eval( ''.join( proplines )) or {}
            style = ';'.join([ '%s : %s' % (k,v) for k,v in prop.items() ])
        except :
            style = ''

        html = ''
        if text :
            try :
                t    = Translate( etxtext=text, etxconfig=self.config )
                html = self.tmpl % ( style, t( context={} ) )
            except :
                if node.parser.etparser.debug : raise
                html = self.tmpl % ('', '')
        return html


# Register this plugin
gsm.registerUtility( Nested(), IEazyTextExtensionFactory, 'Nested' )
Nested._doc = doc
