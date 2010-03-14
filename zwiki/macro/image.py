# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

import cElementTree as et

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

css = {
    'margin'    : '0px',
    'padding'   : '0px',
    'border'    : '0px',
}

wikidoc = """
=== Image

: Description ::
    Embed Images in the doc. Try to use ''Link markup'' to embed images, if
    advanced styling is required, this macro can come in handy.

Positional arguments,
|= src    | source-url for image, goes into @src attribute
|= alt    | alternate text, goes into @alt attribute

keyword argument,
|= height | optional, image height, goes into @height attribute
|= width  | optional, image width, goes into @width attribute
|= href   | optional, href, to convert the image into a hyper-link

Default CSS styling,
> [<PRE %s >]

CSS styling accepted as optional keyword arguments
""" % css

class Image( ZWMacro ) :

    def __init__( self, src, alt, **kwargs ) :
        self.src    = src
        self.alt    = alt
        self.height = kwargs.pop( 'height', None )
        self.width  = kwargs.pop( 'width', None )
        self.href   = kwargs.pop( 'href', '' )

        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        hattr = self.height and ( 'height="%s"' % self.height ) or ''
        wattr = self.width and ( 'width="%s"' % self.width ) or ''
        img   = '<img %s %s src="%s" alt="%s" style="%s"> </img>' % \
                    ( hattr, wattr, self.src, self.alt, self.style )
        # If the image is a link, enclose it with a 'anchor' dom-element.
        if self.href :
            href = et.Element( 'a', { 'href' : self.href } )
            href.append( et.fromstring( img ))
            html = et.tostring( href )
        else :
            html = img
        return html
