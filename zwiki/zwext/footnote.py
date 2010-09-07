# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

#import xml.etree.cElementTree as et
import lxml.html    as lhtml

from   zwiki.zwext  import ZWExtension
from   zwiki        import split_style, constructstyle

wikidoc = """
=== Footnote
:Description::
    Generate footnotes that can be referenced. Note that each foot not block
    should be aligned at the left side after the foot-note anchor name,
    even if it is a multiline foot-note. And the foot-note anchor name should
    be aligned with the begining of the line.

:Example ::

foot-note content can be specified like,
> [<PRE {{{ Footnote footnote-title
  1 German-born Swiss-American theoretical physicist, philosopher and
  author who is widely regarded as one of the most influential and best
  known scientists and intellectuals of all time. He is often regarded as
  the father of modern physics.

  2 American physicist known for his work in the path integral
  formulation of quantum mechanics, the theory of quantum electrodynamics.
  }}} >]

Note that inside the ''Footnote'' extension block, each footnote should be
seperated by an empty line and each footnote's first word will be interpreted
as its anchor name, which can be referenced else where like,

> ... mentioned by Richard Feynman ~[<FN 1 ~>], initially proposed by Albert Einstein  ~[<FN 2 ~>]

... mentioned by Richard Feynman [<FN 1 >], initially proposed by
  Albert Einstein  [<FN 2 >]
...

{{{ Footnote footnote-title
1 German-born Swiss-American theoretical physicist, philosopher and
  author who is widely regarded as one of the most influential and best
  known scientists and intellectuals of all time. He is often regarded as
  the father of modern physics.

2 American physicist known for his work in the path integral
  formulation of quantum mechanics, the theory of quantum electrodynamics.
}}}
"""

css = {
}

tmpl = """
<div style="">
<b> %s </b>
<table style="margin-left: %s">
%s
</table>
</div>
"""

rowtmpl = """
<tr>
    <td style="padding: 5px; color: blue; vertical-align: top;"><a name="%s">%s</a></td>
    <td style="padding: 5px; text-align: left;">%s</td>
</tr>
"""

class Footnote( ZWExtension ) :
    """Implements Footnote() wikix"""

    def _compose(self, lines) :
        html = ''
        if lines :
            splits = lines[0].split(' ', 1)
            name   = splits and splits.pop(0) or ''
            text   = ' '.join( [splits and splits.pop(0) or '' ] + lines[1:] )
            html   = rowtmpl % (name, name, text)
        return html

    def __init__( self, props, nowiki, *args ) :
        self.nowiki = nowiki
        self.style  = constructstyle( props, defcss=css )
        self.title  = args and args[0] or 'Footnotes :'
        self.args   = args[1:]

    def tohtml( self ) :
        html  = []
        curr  = []
        lines = self.nowiki.splitlines()
        while lines :
            line = lines.pop(0)
            stripped = line.strip(' \t')
            if curr and line and line[0] in [ ' ', '\t' ] :
                curr.append(stripped)
            elif line and line[0] not in [ ' ', '\t' ] :
                curr and html.append( self._compose(curr) )
                curr = [line]
            elif not stripped :
                continue
        curr and html.append(self._compose(curr))
        html = tmpl % (self.title, self.style, ''.join(html))
        return html
