"""Implementing the ProjectAttributes macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#   CSS styling is currently using zeta.

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
                    <td class="ralign p5 fntbold">admin-email : </td><td class="p5"> %s </td>
                </tr>
                <tr>
                    <td class="ralign p5 fntbold">license : </td><td class="p5"> %s </td>
                </tr>
                <tr>
                    <td class="ralign p5 fntbold">mailing-lists : </td><td class="p5"> %s </td>
                </tr>
                <tr>
                    <td class="ralign p5 fntbold">irc-channels : </td><td class="p5"> %s </td>
                </tr>
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

class ProjectAttributes( ZWMacro ) :
    """Implements ProjectAttributes() Macro"""

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
        
        cntnr = et.Element( 'div', { 'name' : 'projectattrs', 'style' : style } )
        if p :
            cntnr.append(
                et.fromstring(
                    template % \
                        ( p.admin_email, p.license.licensename,
                          ', '.join([ m.mailing_list for m in p.mailinglists ]),
                          ', '.join([ m.ircchannel for m in p.ircchannels ]),
                        )
                )
            )
        return et.tostring( cntnr )

