# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

#import xml.etree.cElementTree as et
import lxml.html           as lhtml
from   pygments            import highlight
from   pygments.formatters import HtmlFormatter
from   pygments.lexers     import guess_lexer, get_lexer_for_filename, \
                                  get_lexer_by_name

from   zwiki.zwext  import ZWExtension
from   zwiki        import split_style, constructstyle

css = { 
    'margin-left'  : '5%',
    'margin-right' : '5%',
}

wikidoc = """
=== Code

: Description ::
    Syntax highlighting for code-snippet. Highlighting is available for
    [[ /help/pygments | several-dozen formats ]], refer to the //Alias// field
    to invoke the correct highligher.

'' Example ''

> [<PRE  {{{ Code C
    struct process {
      struct process *next;
      const char *name;
      PT_THREAD((* thread)(struct pt *, process_event_t, process_data_t));
      struct pt pt;
      unsigned char state;
    };
  }}} >]

{{{ Code C
struct process {
  struct process *next;
  const char *name;
  PT_THREAD((* thread)(struct pt *, process_event_t, process_data_t));
  struct pt pt;
  unsigned char state;
};
}}}

To highlight a different syntax, supply the syntax name as a parameter like,
> [<PRE {{{ Code <syntax-name> >]

To disable line numbers while highlighting add parameter 'noln'. The default
is to list the line numbers.
> [<PRE {{{ Code <syntax-name> nonl >]

"""

script_templ = """
<style type="text/css">
    %s
    .highlighttable td.linenos {
        padding : 3px;
        color : brown;
        background-color : activeborder;
    }
    .highlighttable td.code { padding : 3px }
    .highlight { background-color : #FAFAFA; }
</style>
"""

code_templ = """
<div class="br4" style="background : #FAFAFA; border : 1px dashed gray;">
%s
</div>
"""

class Code( ZWExtension ) :
    """Implements Code() wikix"""

    def __init__( self, props, nowiki, *args ) :
        self.nowiki  = nowiki
        self.style   = constructstyle( props, defcss=css )
        self.lexname = args and args[0].lower() or 'text'
        self.linenos = 'noln' not in args

    def tohtml( self ) :
        try :
            lexer = get_lexer_by_name( self.lexname )
            scrpt = HtmlFormatter().get_style_defs('.highlight')
            code  = highlight( self.nowiki, lexer,
                               HtmlFormatter( linenos=self.linenos ) )
            html  = '<div style="%s">%s%s</div>' % \
                        ( self.style, (script_templ % scrpt), (code_templ % code) )
        except:
            html  = self.nowiki
        return html

