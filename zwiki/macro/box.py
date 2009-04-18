# -*- coding: utf-8 -*-

# gotcha : none
# notes  : none
# todo   : none


from   zwiki.macro import ZWMacro


styles = [
    ('color',  'color : '),
    ('bg',     'background : '),
    ('border', 'border : '),
]

stdstyle = 'padding : 0px 2px 0px 2px; '

class Box( ZWMacro ) :
    """Implements Box() Macro"""

    def __init__( self, *args, **kwargs ) :
        self.text   = len(args) > 0 and args[0] or ''
        self.color  = kwargs.get( 'color', '' )
        self.bg     = kwargs.get( 'bg', '' )
        self.border = kwargs.get( 'border', '' )
        self.style  = kwargs.get( 'style', '' )

    def tohtml( self ) :
        attrs = dir(self)
        style = ';'.join([ attr + getattr( self, item )
                           for item, attr in styles if getattr( self, item ) ])
        style = stdstyle + style + '; ' + self.style + ';'
        html  = '<span ' + 'style="'+style+'">' + self.text  + '</span>'
        return html
