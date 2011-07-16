"""
h3. EazyText Extensions

EazyText Extension is a plugin framework to extend wiki engine itself. One
can define new markups, text formats etc ... and integrate it with EazyText as
an extension.

h3. Extension Framework

Extented wiki text can be added into the main document by enclosing them within
triple curly braces '' ~{~{{ ... ~}~}} ''. Everything between the curly braces
are passed directly to the extension module, which, in most of the cases will
return a translated HTML text. The general format while using a wiki extension
is,

> ~{~{~{''extension-name'' //space seperated parameter-strings//
> # {
> # ''property-name'' : //value//
> # ''property-name'' : //value//
> # ...
> # }
> 
> ''wiki-text ...''
> ~}~}~}

* ''extension-name'', should be one of the valid extensions.
* ''parameter-strings'', string values that will be passed as parameters.
* ''property-name'', property name can be a property accepted by the extension
  module or can be CSS property. Note that, the entire property block should
  be marked by a beginning ''hash (#)''
* ''wiki-text'', the actual text that get passed on to the extension class.
"""

# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.


# Gotcha : None
#   1. While testing EazyText, make sure that the exception is not re-raised
#      for `eval()` call.
# Notes  : None
# Todo   : None

import os, sys
from   os.path                      import splitext, dirname
from   zope.component               import queryUtility

import eazytext.extension.box
import eazytext.extension.code
import eazytext.extension.footnote
import eazytext.extension.htmlext
import eazytext.extension.nested

def build_ext( extnode, nowiki ) :
    """Parse the nowiki text, like,
        {{{ ExtensionName
        # property dictionary
        # ..
        # ..
        ....
        }}}
    To function name, *args and **kwargs
    """
    from   eazytext.interfaces   import IEazyTextExtensionFactory
    props = []
    nowikilines = nowiki.split( '\n' )
    for i in range( len(nowikilines) ) :
        if len(nowikilines[i]) and nowikilines[i][0] == '#' :
            props.append( nowikilines[i][1:] )
            continue
        break;
    nowiki = '\n'.join( nowikilines[i:] )

    try :
        props = props and eval( ''.join( props ) ) or {}
    except :
        if extnode.parser.etparser.debug : raise
        props = {}

    try :
        factory = queryUtility( IEazyTextExtensionFactory, extnode.xwikiname )
        args = [ props, nowiki ] + extnode.xparams
        ext = factory( *args )
    except :
        if extnode.parser.etparser.debug : raise
        ext = None

    etparser = extnode.parser.etparser
    if ext :
        ext.extnode = extnode               # Backreference to parser AST node
        extnode.parser.etparser.regext(ext) # Register macro with the parser
        ext.on_parse(ext.extnode)           # Callback on_parse()
    return ext
