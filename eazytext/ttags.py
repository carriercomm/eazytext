"""
h2. Templated Tags

HTML tags with common usage pattern are pre-templated and can be used by
attaching the template name with HTML markup
''\[<''. And the text contained within '' \[< .... >] '' are interpreted by
the template. For example, most of the pre-formatted text in this page are
generated using ''PRE'' template, like,
   > \[<PRE preformatted text \>]

   > [<PRE preformatted text >]
"""

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2009 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   eazytext.lib         import escape_htmlchars
from   eazytext.interfaces  import IEazyTextTemplateTags

gsm = getGlobalSiteManager()

class TT( object ):
    ttname = '_default'
    def onparse( self, node ):
        pass

    def headpass1( self, node, igen ):
        pass

    def headpass2( self, node, igen ):
        pass

    def generate( self, node, igen, *args, **kwargs ):
        pass

    def tailpass( self, node, igen ):
        pass


class TTAbbr( TT ):
    """Show the abbreviated text, the expanded full text will be shown by
    hovering over the abbreviated text.
    """
    ttname = 'ABBR'
    implements( IEazyTextTemplateTags )
    template = '<abbr class="etttag" title="%s">%s</abbr>'
    def generate( self, node, igen, *args, **kwargs ):
        args  = node.text.split(',')
        cont  = escape_htmlchars( args and args.pop(0).strip() or '' )
        title = escape_htmlchars( args and args.pop(0).strip() or '' )
        html  =  self.template % ( title, cont )
        igen.puttext( html )
    example = '[<ABBR WTO, World Trade organisation >]'


class TTAddr( TT ) :
    """Encapsulate address text inside <address> tag. Note that comma inside
    the text will automatically be replaced with <br/>"""
    ttname = 'ADDR'
    implements( IEazyTextTemplateTags )
    template = '<address class="etttag">%s</address>'
    def generate( self, node, igen, *args, **kwargs ):
        text = escape_htmlchars( node.text ).replace(',', '<br/>')
        igen.puttext( self.template % text )
    example = "[<ADDR 1, Presidency, St. Mark's Road, Bangalore-1 >]"


class TTFixme( TT ):
    """A simple FIXME motif to associate with a any particular text."""
    ttname = 'FIXME'
    implements( IEazyTextTemplateTags )
    template = '<span class="etttag fixme">%s</span> %s'
    def generate( self, node, igen, *args, **kwargs ):
        igen.puttext( self.template % ('FIXME', node.text) )
    example = '[<FIXME The parser is yet to support unicode>]'


class TTPre( TT ):
    """Preformated text. Text inside this template will be spanned (using span
    element) and styled with //pre//.
    """
    ttname = 'PRE'
    implements( IEazyTextTemplateTags )
    template = '<span class="etttag pre">%s</span>'
    def generate( self, node, igen, *args, **kwargs ) :
        igen.puttext( self.template % escape_htmlchars( node.text ))
    example = '[<PRE sample text >]'


class TTQ( TT ) :
    """Inline quotes using html's <q> tag. For blockquotes use the wiki markup
    //(>)// instead.
    html element generated is a div element with class attribute ''//qbq//''
    """
    ttname = 'Q'
    implements( IEazyTextTemplateTags )
    template = '<div class="etttag qbq">%s</div>'
    def generate( self, node, igen, *args, **kwargs ):
        igen.puttext( self.template % escape_htmlchars( node.text ))
TTQ.example = """[<Q
Emptying the heart of desires,
Filling the belly with food,
Weakening the ambitions,
Toughening the bones.
>]
"""


class TTSmileySmile( TT ):
    """A simple smiley, a happy one."""
    ttname = ':-)'
    implements( IEazyTextTemplateTags )
    template = '<span class="etttag smile">%s</span>'
    def generate( self, node, igen, *args, **kwargs ):
        igen.puttext( self.template % '&#9786;' )
    example='[<:-)>] '


class TTSmileySad( TT ):
    """A simple smiley, a sad one."""
    ttname = ':-('
    implements( IEazyTextTemplateTags )
    template = '<span class="etttag sad">%s</span>'
    def generate( self, node, igen, *args, **kwargs ):
        igen.puttext( self.template % '&#9785;' )
    example = '[<:-(>]'


class TTFnt( TT ) :
    """Style encapsulated text with CSS fonts. The font styling will be applied
    only to the text contained inside the template. """
    ttname = 'FNT'
    implements( IEazyTextTemplateTags )
    template = '<span class="etttag fnt" style="font: %s">%s</span>'
    def generate( self, node, igen, *args, **kwargs ):
        try :
            style, innerHTML = node.text.split( ';', 1 )
        except :
            style, innerHTML = '', node.text
        style, innerHTML = escape_htmlchars(style), escape_htmlchars(innerHTML)
        igen.puttext( self.template % (style, innerHTML) )
TTFnt.example = """[<FNT italic bold 12px/30px Georgia, serif ;
This text is specially fonted >]
"""


class TTFootnote( TT ) :
    """A Footnote reference."""
    ttname = 'FOOTNOTE'
    implements( IEazyTextTemplateTags )
    template = '<sup class="etttag footnote">' + \
               '<a href="#%s" style="text-decoration: none;">%s' + \
               '</a></sup>'
    def generate( self, node, igen, *args, **kwargs ):
        text = escape_htmlchars( node.text.strip() )
        igen.puttext( self.template % (text, text) )
TTFootnote.example = """... mentioned by Richard Feynman
[<FN 1 >], initially proposed by Albert Einstein  [<FN 2 >]

And foot-note content can be specified using the Wiki-extension language,
like,

{{{ Footnote //footnote-title//
1 German-born Swiss-American theoretical physicist, philosopher and
author who is widely regarded as one of the most influential and best
known scientists and intellectuals of all time. He is often regarded as
the father of modern physics.

2 American physicist known for his work in the path integral
formulation of quantum mechanics, the theory of quantum electrodynamics.
}}}
"""

for k, cls in globals().items() :
    if k.startswith( 'TT' ):
        gsm.registerUtility( cls(), IEazyTextTemplateTags, cls.ttname.lower() )
