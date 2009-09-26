"""Implementing the YearsBefore macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import datetime     as dt

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style

class YearsBefore( ZWMacro ) :
    """Implements YearsBefore() Macro"""

    def __init__( self, template, fromyear, **kwargs ) :
        self.template = template
        self.fromyear = int(fromyear)
        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = {}
        self.css.update( d_style )
        self.css.update( kwargs )

    def tohtml( self ) :
        style  = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; ' + self.style + '; '
        utc    = dt.datetime.utcnow()
        num    = utc.year - self.fromyear
        years  = utc.year < self.fromyear and 'sometime' \
                 or (num and (str(num+1) + ' years') or '1 year')
        string = self.template % years
        return '<span>%s</span>' % string
