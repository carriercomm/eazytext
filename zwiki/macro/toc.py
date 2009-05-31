# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  : None
# Todo   :
#   1. Add TOC with pos='inline'


import cElementTree as et
from   random       import choice

from   zwiki.macro  import ZWMacro
from   zwiki        import split_style

alphanum    = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
random_word = lambda : ''.join([ choice(alphanum) for i in range(4) ])

css = {
    'background'     : '#f8f7bc',
    'position'       : 'relative',
    'float'          : 'left',
    'margin-top'     : '10px',
    'margin-left'    : '10px',
    'margin-bottom'  : '10px',
    'margin-right'   : '10px',
    'padding-top'    : '3px',
    'padding-left'   : '3px',
    'padding-bottom' : '3px',
    'padding-right'  : '3px',
}

htags = {
    'h1' : 'margin-left : 2px; ',
    'h2' : 'margin-left : ',
    'h3' : 'margin-left : ',
    'h4' : 'margin-left : ',
    'h5' : 'margin-left : ',
}

html_close = """
<span style="margin-left: 20px; color : blue; cursor : pointer; font-size : small; 
             text-align :  right;">close</span>"""

html_topic = lambda topic : '<span style="font-weight : bold;">' + topic + \
                            '</span>'

script = """
<style type="text/css">
    .dispnone { display : none; }
</style>
<script type="text/javascript">
    dojo.addOnLoad(
        function() {
            var toc_nodes = dojo.getObject( 'toc_nodes', null );
            if( ! toc_nodes ) {
                toc_nodes = dojo.query( 'div.toc' );
                dojo.forEach(
                    toc_nodes,
                    function( node ) {
                        var headdiv = node.childNodes[0];
                        var toc_div = node.childNodes[1];
                        dojo.connect(
                            headdiv.childNodes[1], 'onclick',
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
                dojo.setObject( 'toc_nodes', toc_nodes );
            }
        }
    );
</script>
"""

class Toc( ZWMacro ) :
    """Implements Toc() Macro"""

    def __init__( self, *args, **kwargs ) :
        indent         = int( kwargs.pop( 'indent', '1' ))
        index          = int( kwargs.pop( 'index', '-1' ))
        maxheadlen     = kwargs.pop( 'maxheadlen', '' )
        self.topic     = kwargs.pop( 'topic', 'Table of Contents' )
        self.maxheadlen= maxheadlen and int(maxheadlen) or None
        self.numbered  = kwargs.pop( 'numbered', False )
        self.postindex = index == 0 and -1 or index
        htags.update(
            [ ( h, htags[h] + str(indent * n) + 'em;' )
              for h, n in [ ('h2', 1), ('h3', 2), ('h4', 3), ('h5', 4) ]]
        )

        d_style, s_style = split_style( kwargs.pop( 'style', {} ))
        self.style  = s_style
        self.css    = {}
        self.css.update( css )
        self.css.update( d_style )
        self.css.update( kwargs )

    def _maketoc( self, node, toc_div, numbered=False, level='' ) :
        count     = 1
        level     = level[:-1]
        for n in node.getchildren() :
            if n.tag in htags :
                item      = n.makeelement( 'div', { 'style' : htags[n.tag] } )
                text      = n.getchildren()[0].get( 'name' ) # The anchor child
                link      = item.makeelement( 'a', { 'href' : '#' + text } )
                link.text = self.maxheadlen and \
                                (  text[:self.maxheadlen] + \
                                  (text[self.maxheadlen:] and ' ...' or '' ) ) \
                            or text
                item.append( link )
                toc_div.append( item )
                count     += 1
            self._maketoc( n, toc_div, numbered )
        return

    def tohtml( self ) :
        return ''

    def on_posthtml( self ) :
        style = '; '.join([ k + ' : ' + self.css[k] for k in self.css ])
        if self.style :
            style += '; ' + self.style + '; '
        zwparser = self.macronode.parser.zwparser
        try :
            htmltree = et.fromstring( zwparser.html )
            id       = random_word()
            contrdiv = et.Element( 'div', { 'class' : 'toc', 'style' : style, } )
            headdiv  = et.Element( 'div', { 'style' : 'margin-bottom : 5px;' } )
            topicdiv = et.fromstring( html_topic(self.topic) )
            closediv = et.fromstring( html_close )
            headdiv.append( topicdiv )
            headdiv.append( closediv )
            contrdiv.append( headdiv )
            toc_div  = et.Element( 'div', {} )
            self._maketoc( htmltree, toc_div, self.numbered )
            contrdiv.append( toc_div )
            self.posthtml = et.tostring( contrdiv ) + script
        except :
            self.posthtml = 'Unable to generate the TOC, ' +\
                            'Wiki page not properly formed ! <br></br>'
        return
