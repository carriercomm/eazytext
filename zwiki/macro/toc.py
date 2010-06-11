# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#   1. Add TOC with pos='inline'


import xml.etree.cElementTree as et
from   random       import choice
from   copy         import copy, deepcopy

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style, constructstyle

alphanum    = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
random_word = lambda : ''.join([ choice(alphanum) for i in range(4) ])

css = {
    'background'         : '#f8f7bc',
    'position'           : 'relative',
    'float'              : 'left',
    'margin'             : '10px',
    'padding'            : '3px',
    'width'              : '20em',
    '-moz-border-radius' : '5px'
}

wikidoc = """
=== Toc

: Description ::
    Macro to generate Table of contents.

Default CSS styling,
> [<PRE %s >]

CSS styling accepted as optional keyword arguments
""" % css

htags = {
    'h1' : 'margin-left : 2px; ',
    'h2' : 'margin-left : ',
    'h3' : 'margin-left : ',
    'h4' : 'margin-left : ',
    'h5' : 'margin-left : ',
}

html_close = """
<div style="color : blue; cursor : pointer; font-size : small; 
            position: relative; float: right;">close</div>"""

html_topic = lambda topic : '<div style="font-weight : bold;">%s </div>' % topic

script = """
<style type="text/css">
    .dispnone { display : none; }
</style>
<script type="text/javascript">
    dojo.addOnLoad(
        function() {
            var n_toc = dojo.query( 'div.toc' )[0];
            var headdiv = n_toc.childNodes[0];
            var toc_div = n_toc.childNodes[1];
            dojo.connect( headdiv.childNodes[0], 'onclick',
                function( e ) {
                    if ( e.target.innerHTML == 'close' ) {
                        dojo.toggleClass( toc_div, 'dispnone', true );
                        e.target.innerHTML = 'show';
                    } else if ( e.target.innerHTML == 'show' ) {
                        dojo.toggleClass( toc_div, 'dispnone', false );
                        e.target.innerHTML = 'close';
                    }
                    dojo.stopEvent( e );
                }
            );
        }
    );
</script>
"""

class Toc( ZWMacro ) :

    def __init__( self, *args, **kwargs ) :
        indent         = int( kwargs.pop( 'indent', '1' ))
        index          = int( kwargs.pop( 'index', '-1' ))
        self.maxheadlen = int(kwargs.pop( 'maxheadlen', 30 ))
        self.topic     = kwargs.pop( 'topic', 'Table of Contents' )
        self.numbered  = kwargs.pop( 'numbered', False )
        self.postindex = index == 0 and -1 or index
        self.htags     = deepcopy( htags )
        self.htags.update(
            [ ( h, htags[h] + str(indent * n) + 'em;' )
              for h, n in [ ('h2', 1), ('h3', 2), ('h4', 3), ('h5', 4) ]]
        )
        self.style  = constructstyle( kwargs, defcss=css )

    def tohtml( self ) :
        # Gotcha : cannot return a empty string since process_textcontent()
        # logic assumes that the translation fails. actually this macro is a
        # post html macro.
        return ' '

    def _maketoc( self, node, toc_div, numbered=False, level='' ) :
        count     = 1
        level     = level[:-1]
        for n in node.getchildren() :
            if n.tag in self.htags :
                item      = n.makeelement( 'div', { 'style' : self.htags[n.tag] } )
                children  = n.getchildren()
                text      = children[0].get('name') \
                                    if len(children) == 2 \
                                    else children[1].get( 'name' )
                link      = item.makeelement( 'a', { 'href' : '#' + text } )
                link.text = self.maxheadlen and \
                                (  text[:self.maxheadlen] + \
                                  (text[self.maxheadlen:] and ' ...' or '' ) ) \
                            or text or ' '
                item.append( link )
                toc_div.append( item )
                count     += 1
            self._maketoc( n, toc_div, numbered )
        return

    def on_posthtml( self ) :
        zwparser = self.macronode.parser.zwparser
        contrdiv = et.Element( 'div', { 'class' : 'toc', 'style' : self.style, } )
        headdiv  = et.Element( 'div', { 'style' : 'margin-bottom : 5px;' } )
        toc_div  = et.Element( 'div', {} )
        id       = random_word()
        try :
            htmltree = et.fromstring( zwparser.html )
            topicdiv = et.fromstring( html_topic(self.topic) )
            closediv = et.fromstring( html_close )
        except :
            self.posthtml = 'Unable to generate the TOC, ' +\
                            'Wiki page not properly formed ! <br></br>'
        else :
            headdiv.append( closediv )
            headdiv.append( topicdiv )
            contrdiv.append( headdiv )
            contrdiv.append( toc_div )
            self._maketoc( htmltree, toc_div, self.numbered )
            self.posthtml = et.tostring( contrdiv ) + script
        return
