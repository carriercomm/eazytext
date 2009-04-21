"""Implement and package zwiki extension framework"""

# -*- coding: utf-8 -*-

# Gotcha : None
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

css_props = {
    'color'        : 'color : ',
    'bg'           : 'background : ',
    'bordercolor'  : 'border : thin solid ' ,
    'border'       : 'border : ',
    'borderTop'    : 'border-top : ',
    'borderRight'  : 'border-right : ',
    'borderBottom' : 'border-bottom : ',
    'borderLeft'   : 'border-left : ',
    'padding'      : 'padding : ',
    'margin'       : 'margin : ',
    'width'        : 'width : ',
    'pos'          : 'position : ',
    'float'        : 'float : ',
    'clear'        : 'clear :',
    'style'        : '',
}

from zwiki.zwext.box import Box


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
        props  = eval( ''.join( props ) )
        o = globals()[zwextnode.xwikiname]( props, nowiki )
    except :
        o = ZWExtension( {}, nowiki )
    if not isinstance( o, ZWExtension ) :
        o = ZWExtension( {}, nowiki )
    o.zwextnode = zwextnode
    zwextnode.parser.zwparser.regzwext( o )
    return o
