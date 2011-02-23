# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Implementing the Images macro"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle, lhtml

css = {
    'margin'    : '10px',
    'padding'   : '0px',
    'border'    : '0px',
}

wikidoc = """
=== Images

: Description ::
    Embed Image galleries in the doc. 

Positional arguments,
|= *args  | variable number of image sources (@src), one for each for image

keyword argument,
|= alt    | alternate text (@alt), that goes into each image
|= height | optional, image height, applicable to all image's @height attribute
|= width  | optional, image width, applicable to all image's @width attribute
|= cols   | optional, number of image columns in the gallery, default is 3.

Default CSS styling,
> [<PRE %s >]

CSS styling accepted as optional keyword arguments
""" % css

class Images( ZWMacro ) :

    def __init__( self, *args, **kwargs ) :
        self.imgsources = args

        self.alt    = kwargs.pop( 'alt', '' )
        self.height = kwargs.pop( 'height', None )
        self.width  = kwargs.pop( 'width', None )
        self.cols   = int( kwargs.pop( 'cols', '3' ))
        
        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        hattr = self.height and ( 'height="%s"' % self.height ) or ''
        wattr = self.width and ( 'width="%s"' % self.width ) or ''

        imgsources = list(self.imgsources[:])
        gallerydiv = lhtml.Element( 'div', {'style' : 'display : table;'} )
        while imgsources :
            rowdiv = lhtml.Element( 'div', {'style' : 'display : table-row;'} )
            for i in range( self.cols ) :
                if not imgsources :
                    break
                src    = imgsources.pop( 0 )
                coldiv = lhtml.Element('div', {'style' : 'display : table-cell;'})
                img    = '<img %s %s src="%s" alt="%s" style="%s"> </img>' % \
                                ( hattr, wattr, src, self.alt, self.style )
                coldiv.append( lhtml.fromstring( img ))
                rowdiv.append( coldiv )
            gallerydiv.append( rowdiv )
        html = lhtml.tostring( gallerydiv )
        return html
