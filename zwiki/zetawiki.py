"""Module containing the Nodes for all non-teminals"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#   1. Add unicode support
#   2. Add ismatched() method.
#   3. For links that open in new window, append a character that would say
#      so.

import sys
import re

from   zwiki          import escape_htmlchars, split_style

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
}

def normalize( val ) :
    try :
        val = int(val)
    except :
        return unicode(val)
    return val

def parse_interzeta( app, name ) :
    host = name and app.h.interzeta_map( name ) or ''
    return host

def parse_zetalink( app, zlink, text='', interzeta='' ) :
    """Parse 'zlink' into zeta understandable notation and convert them into
    relative url"""
    vals   = zlink.split( '.' )
    kwargs = {}
    kwargs.update([ linkmap[val[0]]( val[1:] )
                    for val in vals if val and val[0] in linkmap.keys() ])
    url    = app.h.url_forzetalink( **kwargs )
    href   = url and ( interzeta.rstrip('/') + '/' + url.lstrip('/') ) or ''
    text   = text or zlink
    return ( href, text )

def parse_link( parser, href, text='' ) :
    """Parse href into ( interzeta, zetalink )"""
    href = href.strip( ' \t' )
    if href[0] == '@' :
        X     = href[1:].split( '%' )
        host  = parse_interzeta( parser.zwparser.app, X[0] )
        href, text  = host and \
                        parse_zetalink( parser.zwparser.app, X[1], text, host )\
                      or ''
    elif href[0] == '%' :
        href, text = parse_zetalink( parser.zwparser.app, href[1:], text )
    return (href, text)
