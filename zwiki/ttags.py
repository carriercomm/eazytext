# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Templates for commonly used patterns of HTML tags"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import sys
import re

from   zwiki  import escape_htmlchars, split_style, obfuscatemail

wikidoc = """
== Templated Tags

HTML tags with common usage pattern are pre-templated and can be used by
attaching the template name with beginning markup
''~[<''. And the text contained within '' ~[< .... >] '' are interpreted by
the template. For example, most of the pre-formatted text in this page are
generated using ''PRE'' template, like,
   > ~[<PRE preformatted text ~>]

   > [<PRE preformatted text >]
"""

def parsetag( text ) :
    html    = text
    keyword = text[:5].upper()
    if keyword[:3] == 'PRE' :
        html = tt_PRE( text[3:] )

    elif keyword[:4] == 'ABBR' :
        html = tt_ABBR( text[4:] )

    elif keyword[:4] == 'ADDR' :
        html = tt_ADDR( text[4:] )

    elif keyword[:3] == 'FNT' :
        html = tt_FNT( text[3:] )

    elif keyword[:5] == 'FIXME' :
        html = tt_FIXME()

    elif keyword[:1] == 'Q' :
        html = tt_Q( text[1:] )

    elif keyword[:3] == ':-)' :
        html = tt_SMILEYSMILE()

    elif keyword[:3] == ':-(' :
        html = tt_SMILEYSAD()

    elif keyword[:2] == 'FN' :
        html = tt_FOOTNOTE( text[2:] )

    return html


def tt_PRE( text ) :
    """
    === PRE
    :Description::
        Generate a preformated element.

    :Syntax ::
        ~[<PRE //text// ~>]

    :Example ::

    > ~[<PRE sample text ~>]
    
    > [<PRE sample text >]
    """
    template = '<pre class="zwttag">%s</pre>'
    return  template % escape_htmlchars( text )


def tt_ABBR( text ) :
    """
    === ABBR
    :Description::
        Generate Abbreviation element

    :Syntax ::
        ~[<ABBR //text//, //title// ~>]

    :Example ::

    > ~[<ABBR WTO, World Trade organisation ~>]
    
    > [<ABBR WTO, World Trade organisation >]
    """
    args = text.split(',')
    cont = args and args.pop(0).strip() or ''
    title = args and args.pop(0).strip() or ''
    template = '<abbr class="zwttag" title="%s"> %s </abbr>'
    html =  template % ( title, cont )
    return html

def tt_FIXME() :
    """
    === FIXME
    :Description::
        Generate a FIXME label

    :Syntax ::
        ~[<FIXME~>]

    :Example ::

    > ~[<FIXME~>]
    
    > [<FIXME>]
    """
    style = "border : 1px solid cadetBlue; " + \
            "color : red; padding: 1px; font-family : monospace;"
    template = '<span class="zwttag fixme br2" style="%s"> %s </span>'
    html = template % ( style, 'FIXME' )
    return html

def tt_Q( text ) :
    """
    === Q
    :Description::
        Generate a quotable quotes

    :Syntax ::
        ~[<Q -quote-text- ~>]

    :Example ::

    > ~[<Q Emptying the heart of desires,
    >  Filling the belly with food,
    >  Weakening the ambitions,
    >  Toughening the bones. ~>]

    > [<Q
      Emptying the heart of desires,
      Filling the belly with food,
      Weakening the ambitions,
      Toughening the bones. >]

    ''html element generated is a div element with class attribute "qbq"''
    """
    style = 'font-style : italic; margin : 5px 0px 5px 0px; \
             padding : 15px 0px 10px 40px; width: 70%; white-space: pre;'
    template = '<div class="zwttag qbq" style="%s"> %s </div>'
    html = template % (style, text )
    return html

def tt_SMILEYSMILE() :
    """
    === SMILEYSMILE
    :Description::
        Generate a happy smiley Glyph

    :Syntax ::
        ~[<:-)~>]

    :Example ::

    > ~[<:-)~>]
    
    > [<:-)>]
    """
    style = "font-size: x-large; " + \
            "color: darkOrchid; padding: 1px; font-family : monospace;"
    template = '<span class="zwttag smile" style="%s"> %s </span>'
    html = template % ( style, '&#9786;' )
    return html

def tt_SMILEYSAD() :
    """
    === SMILEYSAD
    :Description::
        Generate a SMILEYSAD label

    :Syntax ::
        ~[<:-(~>]

    :Example ::

    > ~[<:-(~>]
    
    > [<:-(>]
    """
    style = "font-size: x-large; " + \
            "color: orangeRed; padding: 1px; font-family : monospace;"
    template = '<span class="zwttag sad" style="%s"> %s </span>'
    html = template % ( style, '&#9785;' )
    return html

def tt_ADDR( text ) :
    """
    === ADDRESS
    :Description::
        Generate `address` element

    :Syntax ::
        ~[<ADDR //field1//, //field2//, ... ~>]

    comma will be replaced with <br></br> element

    :Example ::

    > ~[<ADDR 1, Presidency, St. Mark's Road, Bangalore-1 ~>]
    
    > [<ADDR 1, Presidency, St. Mark's Road, Bangalore-1 >]
    """
    text = text.replace( ',', '<br></br>' )
    template = '<address class="zwttag"> %s </address>'
    html = template % text
    return html

def tt_FNT( text ) :
    """
    === FONT
    :Description::
        Generate a span element with specified font styling.

    :Syntax ::
        ~[<FNT <CSS font style> ; <text> ~>]

    :Example ::

    > ~[<FNT italic bold 12px/30px Georgia, serif ;
      This text is specially fonted ~>]
    > [<FNT italic bold 12px/30px Georgia, serif ;
      This text is specially fonted >]
    """
    try :
        style, innerHTML = text.split( ';', 1 )
    except :
        style = ''
        innerHTML = text
    temlate = '<span class="zwttag fnt" style="font: %s"> %s </span>'
    html = template % ( style, innerHTML )
    return html

def tt_FOOTNOTE( text ) :
    """
    === FOOTNOTE
    :Description::
        Generate footnote references.

    :Syntax ::
        ~[<FN text ~>]

    where `text` will be super-scripted and hyper-linked to foot-note content.

    :Example ::

    > ... mentioned by Richard Feynman ~[<FN 1 ~>], initially proposed by
    > Albert Einstein  ~[<FN 2 ~>]

    And foot-note content can be specified using the Wiki-extension language,
    like,

    > [<PRE 
      {{{ Footnote //footnote-title//
      1 German-born Swiss-American theoretical physicist, philosopher and
      author who is widely regarded as one of the most influential and best
      known scientists and intellectuals of all time. He is often regarded as
      the father of modern physics.

      2 American physicist known for his work in the path integral
      formulation of quantum mechanics, the theory of quantum electrodynamics.
      }}}

      Note that inside the ''Footnote'' extension block, each footnote should
      be seperated by an empty line and each footnote's first word will be
      interpreted as its anchor name. >]
    
    ... mentioned by Richard Feynman [<FN 1 >], initially proposed by
      Albert Einstein  [<FN 2 >]
    ...

    {{{ Footnote //footnote-title//
    1 German-born Swiss-American theoretical physicist, philosopher and
    author who is widely regarded as one of the most influential and best
    known scientists and intellectuals of all time. He is often regarded as
    the father of modern physics.

    2 American physicist known for his work in the path integral
    formulation of quantum mechanics, the theory of quantum electrodynamics.
    }}}
    """
    text = text.strip()
    template = '<sup class="zwttag footnot">' + \
               '<a href="#%s" style="text-decoration: none;"> %s ' + \
               '</a></sup>'
    html = template % ( text, text )
    return html
