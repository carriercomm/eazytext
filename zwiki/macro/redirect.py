# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   : None

from   zwiki.macro  import ZWMacro

class Redirect( ZWMacro ) :
    """
    Just sets the ``redirect`` attribute in
    self.macronode.parser.zwparser.redirect to the the argument that is passed
    """

    def __init__( self, redireclink='' ) :
        self.redirect = redireclink

    def tohtml( self ) :
        self.macronode.parser.zwparser.redirect = self.redirect
        return ''
