# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""
== ZWiki Extensions

ZWiki Extension is a plugin like framework to extend wiki engine itself. One
can define markups, text formats etc ... and integrate it with ZWiki as an
extension.

=== Extension Framework

Extented wiki text can be added into the main document by enclosing them within
triple curly braces '' ~{~{{ ... ~}~}} ''. Everything between the curly braces
are passed directly to the extension module, which, in most of the cases will
return a translated HTML text. The general format while using a wiki extension
is,

> [<PRE
{{{<b>extension-name</b> <em>space seperated parameter-strings</em>
# { '<b>property-name</b>' : '<b>value</b>'
#   '<b>property-name</b>' : '<b>value</b>'
#   <b>...</b>
# }

<b>wiki-text ...</b>

}}}
>]

* ''extension-name'', should be one of the valid extensions.
* ''parameter-strings'', string values that will be passed as parameters.
* ''property-name'', property name can be a property accepted by the extension
  module or can be CSS property. Note that, the entire property block should
  be marked by a beginning ''hash (#)''

== Extension List
"""

# -*- coding: utf-8 -*-

# Gotcha : None
#   1. While testing ZWiki, make sure that the exception is not re-raised
#      for `eval()` call.
# Notes  : None
# Todo   : None


class ZWExtension( object ) :
    """Base Extension class that should be used to derive
    ZWiki Extension / nowiki classes.
    The following attributes are available for the ZWExtension() object.
        zwextnode        passed while instantiating, provides the Extention
                         instance
        zwextnode.parser ZWParser() object
        parser.tu        Translation Unit for the parsed text
        parser.text      Raw wiki text.
        parser.pptext    Preprocessed wiki text.
        parser.html      Converted HTML code from Wiki text
    """
    
    def __init__( self, props, nowiki ) :
        pass

    def on_prehtml( self,  ) :
        """Will be called before calling tohtml() method"""
        pass

    def tohtml( self ) :
        """HTML content to replace the nowiki text"""
        return ''

    def on_posthtml( self,  ) :
        """Will be called afater calling tohtml() method"""
        pass


from zwiki                import split_style, constructstyle
from zwiki.zwext.box      import Box
from zwiki.zwext.code     import Code
from zwiki.zwext.footnote import Footnote
from zwiki.zwext.html     import Html
from zwiki.zwext.nested   import Nested

extnames = [ 'ZWExtension', 'Box', 'Code', 'Footnote', 'Html', 'Nested' ]

def build_zwext( zwextnode, nowiki ) :
    """Parse the nowiki text, like,
        {{{ ExtensionName
        # property dictionary
        # ..
        # ..
        ....
        }}}
    To function name, *args and **kwargs
    """
    props = []
    nowikilines = nowiki.split('\n')
    for i in range(len(nowikilines)) :
        if len(nowikilines[i]) and nowikilines[i][0] == '#' :
            props.append( nowikilines[i][1:] )
            continue
        break;
    nowiki = '\n'.join( nowikilines[i:] )

    try :
        props   = props and eval( ''.join( props ) ) or {}
    except :
        props   = {}

    try :
        xwiki   = zwextnode.xwikiname
        o       = globals()[zwextnode.xwikiname](
                        *( [ props, nowiki ] + zwextnode.xparams )
                  )
    except :
        o = ZWExtension( {}, nowiki )
        # if zwextnode.parser.zwparser.debug :
        #     raise

    if not isinstance( o, ZWExtension ) :
        o = ZWExtension( {}, nowiki )
    zwparser = zwextnode.parser.zwparser
    # Setup templates and override them with computed extension's
    # `style`
    d_style, s_style = split_style( 
                        zwparser.extstyles[o.__class__.__name__+'style'] )
    d_style.update( getattr( o, 'css', {} ) )
    o.style = "%s ; %s ; %s" % ( s_style, 
                                 getattr( o, 'style', '' ),
                                 constructstyle( d_style )
                               )

    # Register extension
    o.zwextnode = zwextnode
    zwextnode.parser.zwparser.regzwext( o )
    return o

def extension_styles( d_style ) :
    """Extract the extension styles and return them as a dictionary"""
    mstyles = dict([ ( e+'style', d_style.pop( e+'style', {} ))
                     for e in extnames ])
    return mstyles
