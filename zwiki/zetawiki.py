"""Module containing the Nodes for all non-teminals"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : 
#   interzeta, must be a alphanumeric word which doesn't start with '_' or '-'
#   but can contain, '_' or '-'
# Todo   :
#   1. Add unicode support
#   2. Add ismatched() method.
#   3. For links that open in new window, append a character that would say
#      so.

import sys
import re

from   zwiki          import escape_htmlchars, split_style

tokenizer = re.compile( r'(@@[a-zA-Z0-9\-_]*)?((@[^ @\t\r\n]*)+)' )

linkmap = {
        'u' : lambda val : ( 'user', normalize(val) ),
        'a' : lambda val : ( 'attachment', normalize(val) ),
        'g' : lambda val : ( 'tag', normalize(val) ),
        'l' : lambda val : ( 'license', normalize(val) ),
        'p' : lambda val : ( 'project', normalize(val) ),
        'm' : lambda val : ( 'milestone', normalize(val) ),
        't' : lambda val : ( 'ticket', normalize(val) ),
        'r' : lambda val : ( 'review', normalize(val) ),
        's' : lambda val : ( 'source', normalize(val) ),
        'v' : lambda val : ( 'revision', normalize(val) ),
        'w' : lambda val : ( 'wiki', normalize(val) ),
}

def normalize( val ) :
    """Normalize the identification in table referenced by zetalink"""
    try :
        val = int(val)
    except :
        val = unicode(val)
    return val

def parse_interzeta( app, name ) :
    """Find the mapped host for 'name'"""
    host = name and app.h.interzeta_map( name ) or ''
    return host

def parse_zetalink( app, zlink ) :
    """Parse 'zlink' into zeta understandable notation and convert them into
    relative url"""
    types  = linkmap.keys() 
    kwargs = dict([ linkmap[ nm[0] ]( nm[1:].lstrip(':') )
                    for nm in zlink.split( '@' )[1:] if nm and (nm[0] in types)
                 ])
    return app.h.url_forzetalink( app.c, **kwargs )

def parse_link( zwparser, markup, text='' ) :
    """Parse markup for interzeta and zetalink. If text is NULL, construct text
    from markup.
    Return,
        (href, text, left) to be used in anchor element"""
    markup = markup
    m      = tokenizer.match( markup )
    href   = ''
    title  = ''
    groups = []
    if m :
        groups = m.groups()
        left   = markup[m.start():m.end()]    # Left over string
    else :
        left   = markup
    if groups and groups[1] :                 # translate zetalink
        (href, ztext, title, style) = parse_zetalink( zwparser.app, groups[1] )

    if href and groups[0] :                   # Found interzeta pattern
        interzeta = parse_interzeta( zwparser.app, groups[0] )
        href      = interzeta and '%s%s' % ( interzeta, href ) or href
    text = text or ztext or markup
    return ( href, title, text, style )
