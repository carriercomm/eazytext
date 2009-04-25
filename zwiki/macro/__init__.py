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


from zwiki.macro.span     import Span
from zwiki.macro.toc      import Toc
from zwiki.macro.clear    import Clear
from zwiki.macro.anchor   import Anchor
from zwiki.macro.html     import Html  
from zwiki.macro.redirect import Redirect  

def build_macro( macronode, macro ) :
    """Parse the macro text, like,
        {{ Macroname( arg1, arg2, kwarg1=value1, kwarg2=value2 ) }}
    To function name, *args and **kwargs
    """
    try :
        o = eval( macro[2:-2] )
    except :
        o = ZWMacro()
    if not isinstance( o, ZWMacro ) :
        o = ZWMacro()
    o.macronode = macronode
    macronode.parser.zwparser.regmacro( o )
    return o
