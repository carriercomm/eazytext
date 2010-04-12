"""Module providing templates for commonly used patterns of HTML tags"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import sys
import re

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
    keyword = text[:5]
    if keyword[:3] == 'PRE' :
        html = tt_PRE( text[3:] )

    elif keyword[:4] == 'ABBR' :
        html = tt_ABBR( text[4:] )

    elif keyword[:4] == 'ADDR' :
        html = tt_ADDR( text[4:] )

    elif keyword[:5] == 'FIXME' :
        html = tt_FIXME()

    elif keyword[:3] == ':-)' :
        html = tt_SMILEYSMILE()

    elif keyword[:3] == ':-(' :
        html = tt_SMILEYSAD()

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
    return '<pre>%s</pre>' % text


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
    args  = text.split(',')
    cont  = args and args.pop(0).strip() or ''
    title = args and args.pop(0).strip() or ''
    html  = '<abbr title="%s">%s</abbr>' % ( title, cont )
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
    style = "-moz-border-radius : 3px; border : 1px solid cadetBlue; " + \
            "color : red; padding: 1px; font-family : monospace;"
    html  = '<span style="%s">%s</span>' % (style, 'FIXME')
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
    html  = '<span style="%s">%s</span>' % (style, '&#9786;')
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
    html  = '<span style="%s">%s</span>' % (style, '&#9785;')
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
    html  = '<address>%s</address>' % text
    return html
