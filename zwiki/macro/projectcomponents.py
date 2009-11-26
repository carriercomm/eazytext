"""Implementing the ProjectComponents macro"""

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

ct_template = """
<div><span style="font-weight: bold">%s</span> owned by <a href="%s">%s</a></div>
"""

class ProjectComponents( ZWMacro ) :
    """Implements ProjectComponents() Macro"""

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

        cntnr = et.Element( 'div', { 'name' : 'projectcomps', 'class' : 'compdescr', 'style' : self.style } )
        e     = et.Element( 'h3', { 'style' : "border-bottom : 1px solid cadetBlue; color: cadetBlue" })
        e.text= 'Components'
        cntnr.append( e )
        components = p and sorted( p.components, key=lambda c : c.created_on ) or []
        for c in components :
            owner  = c.owner.username
            e      = et.fromstring( ct_template % ( c.componentname,
                                                    app.h.url_foruser( owner ),
                                                    owner
                                                  )
                                  )
            cntnr.append( e )
            e      = et.Element( 'blockquote', {} )
            e.append( et.fromstring( getattr( c, 'descriptionhtml', '<div></div>' )))
            cntnr.append( e )
        return et.tostring( cntnr )

