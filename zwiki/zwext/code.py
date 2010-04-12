# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

import cElementTree        as et
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
    Enclose code-snippet within a box and syntax-highlight text, where
    highlighting is available for [[ /help/pygments | several-dozen formats ]].
    To invoke the correct highligher, use the // Alias // field.

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

"""

script_templ = """
<style type="text/css">
    %s
    .highlighttable td.linenos { padding : 3px }
    .highlighttable td.code { padding : 3px }
    .highlight { background-color : #FAFAFA; }
</style>
"""

code_templ = """
<div style="background : #FAFAFA; border : 1px dashed gray; -moz-border-radius: 4px;">
%s
</div>
"""

class Code( ZWExtension ) :
    """Implements Code() wikix"""

    def __init__( self, props, nowiki, *args ) :
        self.nowiki  = nowiki
        self.style   = constructstyle( props, defcss=css )
        self.lexname = args and args[0].lower() or 'text'
        self.args    = args[1:]

    def tohtml( self ) :
        lexer = get_lexer_by_name( self.lexname )
        scrpt = HtmlFormatter().get_style_defs('.highlight')
        code  = highlight( self.nowiki, lexer, HtmlFormatter( linenos=True ) )
        html  = '<div style="%s">%s%s</div>' % \
                    ( self.style, (script_templ % scrpt), (code_templ % code) )
        return html

