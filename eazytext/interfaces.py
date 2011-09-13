# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2009 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

"""
h3. An introduction to multi-pass compilation implemented on the AST

Once the //abstract-syntax-tree// is constructed, the tree will be walked
multiple times, by calling the methods headpass1(), headpass2(), generate()
and tailpass() on each node and all of its child nodes. Interface
specifications //IEazyTextTemplateTags//, //IEazyTextExtension// and
//IEazyTextMacro// will provide the entry points for the implementing plugin.

"""

from   zope.interface   import Interface

class IEazyText( Interface ):
    """Base class for all `eazytext` interface specifications."""


class IEazyTextMacro( IEazyText ) :
    """h4. IEazyTextMacro interface specification
    Interface specification for wiki Macro plugin. All methods will accept
    a parameter `node` which contains following attributes,
      *  ''node.parser''            PLY Yacc parser
      *  ''node.parser.etparser''   ETParser() object

    where `etparser` has the following useful attributes,
      *  ''etparser.ctx''         Context for AST construction.
      *  ''etparser.etxconfig''   Configuration parameters
      *  ''etparser.tu''          Translation Unit for the parsed text
      *  ''etparser.text''        Raw wiki text.
      *  ''etparser.pptext''      Preprocessed wiki text.
      *  ''etparser.html''        Converted HTML code from Wiki text

    if any of the specified method recieves `igen` as a parameter, it can be
    used to generate stack machine instruction.
    __call__ method will be used to create a new instance based on macro
    arguments
    """
    
    def __call__( argtext ) :
        """Return an instance of the macro-plugin, using the macro arguments,
        `argtext`.
        """

    def onparse( node ):
        """Will be invoked after parsing the text and while instantiating the
        AST node corresponding to the macro. If the interface returns a
        string, it will be assumed as html and prefixed to the wikipage.
        """

    def headpass1( node, igen ):
        """Invoked during headpass1 phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the macro.
        """

    def headpass2( node, igen ):
        """Invoked during headpass2 phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the macro.
        """

    def generate( node, igen, *args, **kwargs ):
        """Invoked during generate phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the macro.
        """

    def tailpass( node, igen ):
        """Invoked during tailpass phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the macro.
        """



class IEazyTextExtension( IEazyText ) :
    """h4. IEazyTextExtension
    Interface specification for wiki Extension plugin. All methods will accept
    a parameter `node` which contains following use attributes,
    EazyText extension / nowiki classes.
      *  ''node.parser''            PLY Yacc parser
      *  ''node.text''              Raw extension text between {{{ ... }}}
      *  ''node.parser.etparser'' ETParser() object

    where `etparser` has the following useful attributes,
      *  ''etparser.etxconfig'' Configuration parameters
      *  ''etparser.tu''        Translation Unit for the parsed text
      *  ''etparser.text''      Raw wiki text.
      *  ''etparser.pptext''    Preprocessed wiki text.
      *  ''etparser.html''      Converted HTML code from Wiki text

    if any of the specified method recieves `igen` as a parameter, it can be
    used generate the stack machine instruction.
    __call__ method will be used to create a new instance based on extension
    arguments
    """
    
    def __call__( *args ) :
        """Return an instance of the extension-plugin, using the extension
        arguments list, `args`.
        """

    def onparse( node ):
        """Will be invoked after parsing the text and while instantiating the
        AST node corresponding to extension. If the interface returns a
        string, it will be assumed as html and prefixed to the wikipage.
        """

    def headpass1( node, igen ):
        """Invoked during headpass1 phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the wiki-extension.
        """

    def headpass2( node, igen ):
        """Invoked during headpass2 phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the wiki-extension.
        """

    def generate( node, igen, *args, **kwargs ):
        """Invoked during generate phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the wiki-extension.
        """

    def tailpass( node, igen ):
        """Invoked during tailpass phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the wiki-extension.
        """


class IEazyTextTemplateTags( IEazyText ) :
    """h4. Interface specification for templated tag plugins
    Implementing plugin-class will have to support the multi pass AST processing.
        headpass1(), headpass2(), generate() and tailpass() methods
    """

    def onparse( node ):
        """Will be invoked after parsing the text and while instantiating the
        AST node corresponding to template-tag. If the interface returns a
        string, it will be assumed as html and prefixed to the wikipage.
        """

    def headpass1( node, igen ):
        """Invoked during headpass1 phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the templated-tag.
        """

    def headpass2( node, igen ):
        """Invoked during headpass2 phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the templated-tag.
        """

    def generate( node, igen, *args, **kwargs ):
        """Invoked during generate phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the templated-tag.
        """

    def tailpass( node, igen ):
        """Invoked during tailpass phase, `igen` object can be used to
        generate the stack machine instruction. `node` is NonTerminal AST node
        representing the templated-tag.
        """
