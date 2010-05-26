# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

import cElementTree        as et

from   zwiki.zwext  import ZWExtension
from   zwiki        import split_style, constructstyle

wikidoc = """
=== Footnote
:Description::
    Generate footnotes that can be referenced.

:Example ::

foot-note content can be specified like,
> [<PRE {{{ Footnote //footnote-title//
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

{{{ Footnote //footnote-title//
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
<h3>%s</h3>
<table style="padding-left: %s; width: %s;">
%s
</table>
</div>
"""

rowtmpl = """
<tr>
    <td style="text-align: right; vertical-align: top;"><a name="%s">%s</a></td>
    <td style="text-align: left;">%s</td>
</tr>
"""

class Footnote( ZWExtension ) :
    """Implements Footnote() wikix"""

    def __init__( self, props, nowiki, *args ) :
        self.nowiki = nowiki
        self.style  = constructstyle( props, defcss=css )
        self.title  = args and args[0] or 'Footnotes :'
        self.args   = args[1:]

    def tohtml( self ) :
        html  = ''
        newrow= True
        lines = self.nowiki.splitlines()
        while lines :
            line = lines.pop(0).strip(' \t')
            if line and newrow :
                splits = line.split( ' ', 1 )
                name   = splits and splits.pop(0) or ''
                text   = splits and splits.pop(0) or ''
                html   += rowtmpl % (name, name, text)
                newrow = False
            elif not line :
                newrow = True
        html = tmpl % (self.title, "3%", "100%", html)
        return html
