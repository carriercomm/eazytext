import re

VERSION = '0.6dev'

def escape_htmlchars( text ) :
    """If the text is not supposed to have html characters, escape them"""
    text = re.compile( r'&', re.MULTILINE | re.UNICODE ).sub( '&amp;', text )
    text = re.compile( r'"', re.MULTILINE | re.UNICODE ).sub( '&quot;', text )
    text = re.compile( r'<', re.MULTILINE | re.UNICODE ).sub( '&lt;', text )
    text = re.compile( r'>', re.MULTILINE | re.UNICODE ).sub( '&gt;', text )
    return text


def split_style( style ) :
    """`style` can be a CSS style dictionary or string. If dictionary, it can
    have one non-CSS key 'style'. This key can contain the CSS property as a
    string or as another dictionary, in which case the dictionary can once again
    be treated as `style`"""
    style   = style or {}
    s_style = ''
    if isinstance( style, dict ) :
        inner_style = style.pop( 'style', {} )
    elif isinstance( style, (str, unicode) ) :
        inner_style = style
        style       = {}
    if isinstance( inner_style, dict ) and inner_style :
        d_style, s_style = split_style( inner_style )
        style.update( d_style )
    elif isinstance( inner_style, ( str, unicode )) :
        s_style = inner_style
    return style, s_style

def constructstyle( kwargs, defcss={} ) :
    """From the different types of parameters construct a style string"""
    d_style, s_style = split_style( kwargs.pop( 'style', {} ))
    css    = {}
    css.update( defcss )
    css.update( d_style )
    css.update( kwargs )

    style = '; '.join([ "%s: %s" % (k,  css[k]) for k in css ])
    style = "%s; %s ; " % ( style, s_style )
    return style
