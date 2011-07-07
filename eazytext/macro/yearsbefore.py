# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import datetime     as dt

from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager

from   eazytext.interfaces  import IEazyTextMacro, IEazyTextMacroFactory
from   eazytext.lib         import split_style, constructstyle, lhtml

gsm = getGlobalSiteManager()

class YearsBefore( object ) :
    """
    h3. YearsBefore

    : Description ::
        Generate a string (based on a template) describing time elapsed since
        the given (day,month,year). The described time is in UTC.
        Accepts CSS styles for keyword arguments.
    : Example ::
        [<PRE {{ YearsBefore('past %s', '2008', color="red" ) }} >]

    Positional arguments,
    |= template | template string.
    |= fromyear | from year

    keyword argument,
    |= frommonth | from month
    |= fromday   | from day
    """

    tmpl = '<span class="etm-yearsbefore" style="%s">%s</span>'
    implements( IEazyTextMacro )

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
        self.style = constructstyle( kwargs )

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node ) :
        utc   = dt.datetime.utcnow()
        date  = dt.datetime( self.fromyear, self.frommonth, self.fromday )
        delta = utc - date
        days  = delta.days
        
        if days > 0 :
            years  = days/365
            months = (days%365) / 30

            years  = '' if years == 0 \
                     else ( '1 year' if years == 1 else '%s years' % years )
            months = '' if months == 0 \
                     else ( '1 month' if months == 1 else '%s months' % months )
            text   = "%s, %s" % ( years, months )

        else :
            text = 'sometime'

        string = self.template % text

        return self.tmpl % (self.style, string)

    def on_posthtml( self, node ) :
        pass

class YearsBeforeFactory( object ):
    implements( IEazyTextMacroFactory )
    def __call__( self, argtext ):
        return eval( 'YearsBefore( %s )' % argtext )

# Register this plugin
gsm.registerUtility(YearsBeforeFactory(), IEazyTextMacroFactory, 'YearsBefore')
