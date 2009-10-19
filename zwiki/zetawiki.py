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
        'c' : lambda val : ( 'component', normalize(val) ),
        'm' : lambda val : ( 'milestone', normalize(val) ),
        'v' : lambda val : ( 'version', normalize(val) ),
        't' : lambda val : ( 'ticket', normalize(val) ),
        'r' : lambda val : ( 'review', normalize(val) ),
        's' : lambda val : ( 'source', normalize(val) ),
}

def normalize( val ) :
    """Normalize the identification in table referenced by zetalink"""
    try :
        val = int(val)
    except :
        return unicode(val)
    return val

def parse_interzeta( app, name ) :
    """Find the mapped host for 'name'"""
    host = name and app.h.interzeta_map( name ) or ''
    return host

def parse_zetalink( app, zlink ) :
    """Parse 'zlink' into zeta understandable notation and convert them into
    relative url"""
    vals   = [ ( nm[0], nm[1:].lstrip(':') )
               for nm in zlink.split( '@' )[1:] if nm and nm[0] in linkmap.keys() ]
    kwargs = {}
    kwargs.update([ linkmap[obj]( id ) for obj, id in vals  ])
    
    return app.h.url_forzetalink( **kwargs )

def parse_link( zwparser, markup, text='' ) :
    """Parse markup for interzeta and zetalink. If text is NULL, construct text
    from markup.
    Return,
        (href, text, left) to be used in anchor element"""
    markup = markup.strip( ' \t' )
    m      = tokenizer.match( markup )
    href   = ''
    title  = ''
    groups = []
    if m :
        groups = m.groups()
        left   = markup[m.start():m.end()]    # Left over string
    else :
        left   = markup

    if groups and groups[1] :           # translate zetalink
        ( href, title ) = parse_zetalink( zwparser.app, groups[1] )

    if href and groups[0] :             # Found interzeta pattern
        interzeta = parse_interzeta( zwparser.app, groups[0] )
        if interzeta :
            href  = '%s/%s' % ( interzeta, href )
    text = text or markup
    return ( href, title, text, left )
