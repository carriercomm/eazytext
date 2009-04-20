"""Implement and package macro framework"""

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none


class ZWMacro( object ) :
    """Base Macro class that should be used to derive ZWiki Macro classes
    The following attributes are available for the ZWMacro() object.
        macronode        passed while instantiating, provides the Macro instance
        macronode.parser PLY Yacc parser
        parser.zwparser  ZWParser() object
        zwparser.tu      Translation Unit for the parsed text
        zwparser.text    Raw wiki text.
        zwparser.pptext  Preprocessed wiki text.
        zwparser.html    Converted HTML code from Wiki text
    """
    
    def __init__( self, *args, **kwargs ) :
        pass

    def on_prehtml( self,  ) :
        """Will be called before calling tohtml() method"""
        pass

    def tohtml( self ) :
        """HTML content to replace the macro text"""
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

from zwiki.macro.span  import Span
from zwiki.macro.toc   import Toc
from zwiki.macro.clear import Clear


def build_macro( macronode, macro ) :
    """Parse the macro text, like,
        {{ Macroname( arg1, arg2, kwarg1=value1, kwarg2=value2 ) }}
    To function name, *args and **kwargs
    """
    try :
        o = eval( macro[2:-2] )
    except :
        o = ZWMacro()
    o.macronode = macronode
    macronode.parser.zwparser.regmacro( o )
    return o
