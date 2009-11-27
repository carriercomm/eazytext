"""Implementing the YearsBefore macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import datetime     as dt

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

class YearsBefore( ZWMacro ) :
    """Implements YearsBefore() Macro"""

    def __init__( self, template, fromyear, frommonth=1, fromday=1, **kwargs ) :
        utc = dt.datetime.utcnow()
        self.template  = template
        try :
            self.fromyear  = int(fromyear)
            self.frommonth = int(frommonth)
            self.fromday   = int(fromday)
        except :
            self.fromyear  = utc.year
            self.frommonth = utc.month
            self.fromday   = utc.day
        self.style     = constructstyle( kwargs )

    def tohtml( self ) :
        utc   = dt.datetime.utcnow()
        date  = dt.datetime( self.fromyear, self.frommonth, self.fromday )
        delta = utc - date
        days  = delta.days
        
        if days > 0 :
            years  = days/365
            months = (days%365) / 30

            if years == 0 :
                years = ''
            elif years == 1 :
                years = '1 year'
            else :
                years = '%s years' % years

            if months == 0 :
                months = ''
            elif months == 1 :
                months = '1 month'
            else :
                months = '%s months' % months

            text  = "%s, %s" % ( years, months )

        else :
            text = 'sometime'

        string = self.template % text

        return '<span style="%s">%s</span>' % (self.style, string)
