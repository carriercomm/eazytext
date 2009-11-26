"""Implement and package zwiki extension framework"""

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


from zwiki              import split_style
from zwiki.zwext.box    import Box
from zwiki.zwext.html   import Html
from zwiki.zwext.nested import Nested

extnames = [ 'ZWExtension', 'Box', 'Html', 'Nested' ]

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
        props = props and eval( ''.join( props ) ) or {}
        o = globals()[zwextnode.xwikiname]( props, nowiki )
    except :
        o = ZWExtension( {}, nowiki )
        # if zwextnode.parser.zwparser.debug :
        #     raise
    if not isinstance( o, ZWExtension ) :
        o = ZWExtension( {}, nowiki )
    zwparser = zwextnode.parser.zwparser
    # Setup templates and override them with computed extension's
    # `style` and `css`
    d_style, s_style = split_style( 
                        zwparser.extstyles[o.__class__.__name__+'style'] )
    d_style.update( getattr( o, 'css', {} ) )
    o.css = d_style
    o.style = s_style + getattr( o, 'style', '' )
    # Register extension
    o.zwextnode = zwextnode
    zwextnode.parser.zwparser.regzwext( o )
    return o

def extension_styles( d_style ) :
    """Extract the extension styles and return them as a dictionary"""
    mstyles = dict([ ( e+'style', d_style.pop( e+'style', {} ))
                     for e in extnames ])
    return mstyles
