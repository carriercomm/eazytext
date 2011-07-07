from   zope.interface   import Interface

class IEazyTextMacro( Interface ) :
    """Macro plugin interface specification. All methods will accept a single
    parameter `node` which contains following useful attributes,
      * node.parser           PLY Yacc parser
      * node.parser.etparser  ETParser() object

    where `etparser` has the following useful attributes,
      * etparser.tu      Translation Unit for the parsed text
      * etparser.text    Raw wiki text.
      * etparser.pptext  Preprocessed wiki text.
      * etparser.html    Converted HTML code from Wiki text

    """
    def on_parse( self, node ) :
        """To be called after parsing the macro text and creating the AST
        `node`
        """

    def on_prehtml( self, node ) :
        """To be called before calling tohtml() method"""

    def tohtml( self, node ) :
        """Return the HTML content to replace the macro text"""

    def on_posthtml( self, node ) :
        """Will be called after calling tohtml() method"""

class IEazyTextMacroFactory( Interface ) :
    """Plugin factory callable, to return a specific type of macro plugin"""

    def __call__( self, argtext ) :
        """Return an instance of macro-plugin, `argtext` is comma seperated
        arugment list"""

class IEazyTextExtension( Interface ) :
    """Wiki Extension plugin interface specification. All methods will accept
    a single parameter `node` which contains following use attributes,
    EazyText extension / nowiki classes.
      *  node.parser            PLY Yacc parser
      *  node.parser.etparser   ETParser() object

    where `etparser` has the following useful attributes,
      *  etparser.tu      Translation Unit for the parsed text
      *  etparser.text    Raw wiki text.
      *  etparser.pptext  Preprocessed wiki text.
      *  etparser.html    Converted HTML code from Wiki text
    """
    
    def __init__( self, props, nowiki ) :
        pass

    def on_parse( self, node ) :
        """To be called after parsing the macro text and creating the AST
        `node`
        """

    def on_prehtml( self, node ) :
        """To be called before calling tohtml() method"""

    def tohtml( self, node ) :
        """Return the HTML content to replace the macro text"""

    def on_posthtml( self, node ) :
        """Will be called after calling tohtml() method"""

class IEazyTextExtensionFactory( Interface ) :
    """Plugin factory callable, to return a specific type of extension plugin"""

    def __call__( self, *args ) :
        """Return an instance of extension-plugin"""

