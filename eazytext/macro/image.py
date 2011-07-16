# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager

from   eazytext.interfaces  import IEazyTextMacro, IEazyTextMacroFactory
from   eazytext.lib         import split_style, constructstyle, lhtml

gsm = getGlobalSiteManager()

class Image( object ) :
    template = '<img class="etm-image" ' + \
               '%s %s src="%s" alt="%s" style="%s"> </img>'
    implements( IEazyTextMacro )

    def __init__( self, src, alt, **kwargs ) :
        self.src = src
        self.alt = alt
        self.height = kwargs.pop( 'height', None )
        self.width = kwargs.pop( 'width', None )
        self.href = kwargs.pop( 'href', '' )
        self.style = constructstyle( kwargs )

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        pass

    def tohtml( self, node ) :
        hattr = self.height and ( 'height="%s"' % self.height ) or ''
        wattr = self.width and ( 'width="%s"' % self.width ) or ''
        img = self.template % ( hattr, wattr, self.src, self.alt, self.style )
        # If the image is a link, enclose it with a 'anchor' dom-element.
        if self.href :
            href = lhtml.Element( 'a', { 'href' : self.href } )
            href.append( lhtml.fromstring( img ))
            html = lhtml.tostring( href )
        else :
            html = img
        return html

    def on_posthtml( self, node ) :
        pass

class ImageFactory( object ):
    """
    h3. Image

    : Description ::
        Embed Images in the doc. Try to use ''Link markup'' to embed images, if
        advanced styling is required, this macro can come in handy.
        Accepts CSS styles for keyword arguments.
    : Example ::
        [<PRE {{ Image( '/photo.jpg' ) }} >]

    Positional arguments,
    |= src    | source-url for image, goes into @src attribute
    |= alt    | alternate text, goes into @alt attribute

    keyword argument,
    |= height | optional, image height, goes into @height attribute
    |= width  | optional, image width, goes into @width attribute
    |= href   | optional, href, to convert the image into a hyper-link
    """
    implements( IEazyTextMacroFactory )
    def __call__( self, argtext ):
        return eval( 'Image( %s )' % argtext )

# Register this plugin
gsm.registerUtility( ImageFactory(), IEazyTextMacroFactory, 'Image' )
