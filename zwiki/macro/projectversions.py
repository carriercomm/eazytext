"""Implementing the ProjectVersions macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

css = {
    'padding'   : '0px',
    'border'    : '0px',
}

wikidoc = """
=== ProjectVersions

: Description ::
    Meant to be used in project front page, displays list of project versions

Default CSS styling,
> [<PRE %s >]

CSS styling accepted as optional keyword arguments
""" % css

class ProjectVersions( ZWMacro ) :

    def __init__( self, *args, **kwargs ) :
        self.project = args and args[0]
        self.style   = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        app = self.macronode.parser.zwparser.app
        try :   # To handle test cases.
            p   = getattr( app.c, 'project', None )
        except :
            p   = None
        if self.project :
            p = app.projcomp.get_project( unicode(self.project ))

        cntnr = et.Element( 'div', { 'name' : 'projectvers', 'class': 'verdescr',
                                     'style' : self.style } )
        e     = et.Element( 'h3', { 'style' : "border-bottom : 1px solid cadetBlue; color: cadetBlue" })
        e.text= 'Versions'
        cntnr.append( e )
        versions = p and sorted( p.versions, key=lambda v : v.created_on ) or []
        for v in versions :
            e      = et.Element( 'div', { 'style' : 'font-weight: bold' } ) 
            e.text = v.version_name
            cntnr.append( e )
            e      = et.Element( 'blockquote', {} )
            try :
                e.append( et.fromstring( getattr( v, 'descriptionhtml', '<div></div>' )))
            except :
                pass
            cntnr.append( e )
        return et.tostring( cntnr )
