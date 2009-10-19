"""Implementing the ProjectDescription macro"""

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

        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = {}
        self.css.update( css )
        self.css.update( d_style )
        self.css.update( kwargs )

    def tohtml( self ) :
        app = self.macronode.parser.zwparser.app
        p   = self.project and app.projcomp.get_project( unicode(self.project ))
        html= ''

        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; %s ;' % self.style
        cntnr = et.Element( 'div', { 'name' : 'projectdesc', 'style' : style } )
        if p :
            cntnr.append( 
                et.fromstring( template % \
                                ( p.summary, p.project_info.descriptionhtml )
                             )
            )
        return et.tostring( cntnr )

