"""Implementing the ProjectDescription macro"""

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

template = """
<div>
    <div name="summary">
        <span style="font-weight: bold; color: gray;">Summary : </span>
        <em> %s </em>
    </div>
    <div name="desc">
        <blockquote> %s </blockquote> 
    </div>
</div>
"""

class ProjectDescription( ZWMacro ) :
    """Implements ProjectDescription() Macro"""

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

        html= ''
        cntnr = et.Element( 'div', { 'name' : 'projectdesc', 'style' : self.style } )
        if p :
            cntnr.append( 
                et.fromstring( template % \
                                ( p.summary, p.project_info.descriptionhtml )
                             )
            )
        return et.tostring( cntnr )
