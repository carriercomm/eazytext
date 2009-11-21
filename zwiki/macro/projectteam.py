"""Implementing the ProjectTeam macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

css = {
    'padding'            : '5px',
    'background'         : '#e5ecf9',
    '-moz-border-radius' : '5px'
}

template = """
<div>
    <div style="display: table">
        <div style="display: table-row">
            <div class="ralign p5 fntbold" style="border: none;"> Admin : </div>
            <div class="p5" style="border: none;"> %s </div>
        </div>
        %s
    </div>
</div>
"""
team_template = """
<div style="display: table-row">
    <div class="ralign p5 fntbold" style="border: none;">%s : </div>
    <div class="p5" style="border: none"> %s </div>
</div>
"""

class ProjectTeam( ZWMacro ) :
    """Implements ProjectTeam() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.project = args and args[0]
        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        app = self.macronode.parser.zwparser.app
        try :   # To handle test cases.
            p   = getattr( app.c, 'project', None )
        except :
            p   = None
        if self.project :
            p = app.projcomp.get_project( unicode(self.project ))

        cntnr = et.Element( 'div', { 'name' : 'projectteam', 'style' : self.style } )

        if p :
            admin  = p.admin.username
            admin  = '<a href="%s">%s</a>' % \
                            ( app.h.url_foruser( admin ), admin  )
            items  = app.projcomp.projectteams( p ).items()
            teams  = ''
            for team, value in sorted( items, key=lambda x : x[0] ) :
                if team == app.projcomp.team_nomember :
                    continue
                users = [ '<a href="%s">%s</a>' % ( app.h.url_foruser(u), u ) 
                          for id, u in value[0] ]
                teams += team_template % \
                            ( team, users and ', '.join( users ) or '-' )
            cntnr.append( et.fromstring( template % ( admin, teams )))
        return et.tostring( cntnr )
