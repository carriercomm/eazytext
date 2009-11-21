"""Implementing the ProjectAttributes macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#   CSS styling is currently using zeta.

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
            <div  class="ralign p5 fntbold" style="display: table-cell; border: none">admin-email :</div>
            <div  class="p5" style="display: table-cell; border: none">%s</div>
        </div>
        <div style="display: table-row">
            <div class="ralign p5 fntbold" style="display: table-cell; border: none;">license : </div>
            <div class="p5" style="display: table-cell; border: none"> %s </div>
        </div>
        <div style="display: table-row">
            <div class="ralign p5 fntbold" style="display: table-cell; border: none;">mailing-lists : </div>
            <div class="p5" style="display: table-cell; border: none"> %s </div>
        </div>
        <div style="display: table-row">
            <div class="ralign p5 fntbold" style="display: table-cell; border: none;">irc-channels : </div>
            <div class="p5" style="display: table-cell; border: none"> %s </div>
        </div>
    </div>
</div>
"""

class ProjectAttributes( ZWMacro ) :
    """Implements ProjectAttributes() Macro"""

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

        cntnr = et.Element( 'div', { 'name' : 'projectattrs', 'style' : self.style } )
        if p :
            cntnr.append(
                et.fromstring(
                    template % \
                        ( p.admin_email, p.license and p.license.licensename,
                          ', '.join([ m.mailing_list for m in p.mailinglists ]),
                          ', '.join([ m.ircchannel for m in p.ircchannels ]),
                        )
                )
            )
        return et.tostring( cntnr )
