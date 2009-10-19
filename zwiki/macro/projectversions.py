"""Implementing the ProjectVersions macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style

css = {
    'padding'   : '0px',
    'border'    : '0px',
}

class ProjectVersions( ZWMacro ) :
    """Implements ProjectVersions() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.project = args and args[0]

        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = {}
        self.css.update( css )
        self.css.update( d_style )
        self.css.update( kwargs )

    def tohtml( self ) :
        app = self.macronode.parser.zwparser.app
        try :   # To handle test cases.
            p   = getattr( app.c, 'project', None )
        except :
            p   = None
        if self.project :
            p = app.projcomp.get_project( unicode(self.project ))

        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; %s ;' % self.style
        
        cntnr = et.Element( 'div', { 'name' : 'projectvers', 'style' : style } )
        e     = et.Element( 'h3', { 'style' : "border-bottom : 1px solid cadetBlue; color: cadetBlue" })
        e.text= 'Versions'
        cntnr.append( e )
        versions = p and sorted( p.versions, key=lambda v : v.created_on ) or []
        for v in versions :
            e      = et.Element( 'div', { 'style' : 'font-weight: bold' } ) 
            e.text = v.version_name
            cntnr.append( e )
            e      = et.Element( 'blockquote', {} )
            e.text = v.description
            cntnr.append( e )
        return et.tostring( cntnr )

