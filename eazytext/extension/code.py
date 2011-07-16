# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

# Gotcha : none
# Notes  : none
# Todo   : none
#   1. Unit test case for this extension.

from   pygments            import highlight
from   pygments.formatters import HtmlFormatter
from   pygments.lexers     import guess_lexer, get_lexer_for_filename, \
                                  get_lexer_by_name

from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager

from   eazytext.interfaces  import IEazyTextExtension, \
                                   IEazyTextExtensionFactory
from   eazytext.lib         import split_style, constructstyle, lhtml

gsm = getGlobalSiteManager()


doc = """
h3. Code

: Description ::
    Syntax highlighting for code-snippet. Highlighting is available for
    [[ http://pygments.org/docs/lexers/ | several-dozen formats ]].
    Property key-value pairs accepts CSS styling attributes.

'' Example ''

> [<PRE {{{ Code C
>   struct process {
>     struct process *next;
>     const char *name;
>     PT_THREAD((* thread)(struct pt *, process_event_t, process_data_t));
>     struct pt pt;
>     unsigned char state;
>   };
> }}} >]

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


class Code( object ) :

    implements( IEazyTextExtension )
    tmpl = '<div class="etext-code" style="%s"> %s </div>'
    script_tmpl = '<style type="text/css"> %s </style>'
    code_tmpl = '<div class="codecont"> %s </div>'
    hashtext = None

    def __init__( self, props, nowiki, *args ) :
        self.nowiki = nowiki
        self.style = constructstyle( props )
        self.lexname = args and args[0].lower() or 'text'
        self.linenos = 'noln' not in args

    def on_parse( self, node ) :
        pass

    def on_prehtml( self, node ) :
        etparser = self.extnode.parser.etparser
        if self.hashtext == etparser.hashtext :
            return None
        else :
            self.hashtext == etparser.hashtext
            script = HtmlFormatter().get_style_defs('.highlight')
            html = self.script_tmpl % script
            return (-100, html)

    def tohtml( self , node) :
        try :
            lexer = get_lexer_by_name( self.lexname )
            code  = highlight( self.nowiki, lexer,
                               HtmlFormatter( linenos=self.linenos ) )
            html  = self.tmpl % ( self.style, (self.code_tmpl % code) )
        except:
            if self.extnode.parser.etparser.debug : raise
            html  = self.nowiki
        return html

    def on_posthtml( self, node ) :
        pass

class CodeFactory( object ):
    implements( IEazyTextExtensionFactory )
    def __call__( self, *args ):
        return Code( *args )

# Register this plugin
gsm.registerUtility( CodeFactory(), IEazyTextExtensionFactory, 'Code' )
CodeFactory._doc = doc
