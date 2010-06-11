# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

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
    '-moz-border-radius' : '5px',
    'margin'             : '10px 0px 10px 5px'
}

wikidoc = """
=== ProjectAttributes

: Description ::
    Meant to be used in project front page, displays project attributes, like
    admin, mailinglist, license etc ...

Default CSS styling,
> [<PRE %s >]

CSS styling accepted as optional keyword arguments
""" % css

template = """
<div>
    <div style="display: table">
        <div style="display: table-row">
            <div  class="ralign p5 fntbold" style="width: 8em; display: table-cell; border: none">admin-email :</div>
            <div  class="p5" style="display: table-cell; border: none">%s </div>
        </div>
        <div style="display: table-row">
            <div class="ralign p5 fntbold" style="width: 8em; display: table-cell; border: none;">license : </div>
            <div class="p5" style="display: table-cell; border: none"> %s </div>
        </div>
        <div style="display: table-row">
            <div class="ralign p5 fntbold" style="width: 8em; display: table-cell; border: none;">mailing-lists : </div>
            <div class="p5" style="display: table-cell; border: none"> %s </div>
        </div>
        <div style="display: table-row">
            <div class="ralign p5 fntbold" style="width: 8em; display: table-cell; border: none;">irc-channels : </div>
            <div class="p5" style="display: table-cell; border: none"> %s </div>
        </div>
    </div>
</div>
"""

class ProjectAttributes( ZWMacro ) :

    def __init__( self, *args, **kwargs ) :
        self.project = args and args[0]
        self.style   = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        zwp = self.macronode.parser.zwparser
        app = zwp.app
        zwp.dynamictext = True

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
