"""Implementing the ProjectTeam macro"""

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

template = """
<div>
    <div class="curvy4"> </div>
    <div class="curvy2">
        <div class="bgblue1" style="height : 1px ; margin: 0px 2px 0px 2px;"> </div>
    </div>
    <div class="curvy1">
        <div class="bgblue1" style="height : 1px ; margin: 0px 1px 0px 1px;"> </div>
    </div>
    <div>
        <div class="bgblue1 p5" style="margin: 0px 1px 0px 1px;">
            <table>
                <tr>
                    <td class="ralign p5 w30 fntbold" style="border: none;"> Admin : </td>
                    <td class="p5" style="border: none;"> %s </td>
                </tr>
                %s
            </table>
        </div>
    </div>
    <div class="curvy1">
        <div class="bgblue1" style="height : 1px ; margin: 0px 1px 0px 1px;"> </div>
    </div>
    <div class="curvy2">
        <div class="bgblue1" style="height : 1px ; margin: 0px 2px 0px 2px;" > </div>
    </div>
    <div class="curvy4"> </div>
</div>
"""
team_template = """
<tr>
    <td class="ralign p5 w30 fntbold" style="border: none;">%s : </td>
    <td class="p5" style="border: none"> %s </td>
</tr>
"""

class ProjectTeam( ZWMacro ) :
    """Implements ProjectTeam() Macro"""

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
        p   = self.project and app.projcomp.get_project( unicode(self.project ))

        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; %s ;' % self.style
        
        cntnr = et.Element( 'div', { 'name' : 'projectteam', 'style' : style } )

        if p :
            admin  = p.admin.username
            admin  = '<a href="%s">%s</a>' % \
                            ( app.h.url_foruser( admin ), admin  )
            items  = app.projcomp.projectteams( p ).items()
            teams  = ''
            for team, value in sorted( items, key=lambda x : x[0] ) :
                if team == app.projcomp.team_nomember :
                    continue
                users = [ '<a href="%s">%s</a>' % ( u, u ) for id, u in value[0] ]
                teams += team_template % \
                            ( team, users and ', '.join( users ) or '-' )
            cntnr.append( et.fromstring( template % ( admin, teams )))
        return et.tostring( cntnr )
