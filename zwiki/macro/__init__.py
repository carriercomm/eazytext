"""
== ZWiki Macro framework

Macros are direct function calls that can be made from wiki text into the wiki
engine, provided, there is a macro my that name available. Most probably the
macro will return a html content, which will be used to replace the macro
call.

=== Interfacing with a Macro

As mentioned before, macros are direct function calls into wiki engine and so
it looks like a function call. More specifically the macro call will be
directly evaluated as python code and thus follows all the function calling
rules and conventions of python. 

To expound it further, let us take a specific example of ''YearsBefore''
Macro, which computes the time elapsed from a given (month,day,year) and
composes a string like "2 years 2 months before",

Definition of YearsBefore macro,
> [<PRE YearsBefore( template, fromyear, frommonth=1, fromday=1, **kwargs ) >]

''A small primer on python function calls'',
* Arguments to python functions are of two types, positional and keyword. Other
  types of argument passing are not of concern here.
* Position arguments are specified first in a function call, where the first
  passed parameter is recieved as the first argument, second passed parameter
  is recieved as the second argument and so on. All positional parameters
  are mandatory.
* Keyword arguments are received next. Keyword arguments also carry a
  default value, if in case it is not passed.

With this in mind, we will try to decipher ''YearsBefore'' macro

* ''YearsBefore'', is the name of the macro function.
* ''template'', is the first mandatory positional argument providing the
  template of output string.
* ''fromyear'', is the second mandatory positional argument, specifying the
  year.
* ''frommonth'', is optional keyword argument, specifying the month.
* ''fromday'', is option keyword argument, specifying the day.
* ''kwargs'', most of the macro functions have this last arguments to accept a
  variable number of keyword arguments. One use case for this is to
  pass styling attributes, which is explained the section below.

Use case,
> [<PRE started this activity and running this for {{ YearsBefore('past %s', '2008') }} >]

> started this activity and running this for {{ YearsBefore('past %s', '2008') }}

=== Styling paramters

To get the desired CSS styling for the element returned by macro, pass in the styling
attributes as keyword arguments, like,

> [<PRE started this activity and running this for 
  {{ YearsBefore('past %s', '2008', color="red" ) }} >]

> started this activity and running this for 
> {{ YearsBefore('past %s', '2008', color="red" ) }}

Note that, the attribute name is represented as local variable name inside the
macro function. If you are expert CSS author, you will know that there are
CSS-style attribute-names like ''font-size'', ''font-weight'' which are not
valid variables, so, style attribute-names which contain a ''hypen''
cannot be passed as a keyword argument. As an alternative, there is a special
keyword argument (to all macro functions) by name ''style'', which directly
accepts ''semicolon (;)'' seperated style attributes, like,

> [<PRE started this activity and running this for 
   {{ YearsBefore('past %s', '2008', color="red", style="font-weight: bold; font-size: 200%" ) }} >]

> started this activity and running this for 
> {{ YearsBefore('past %s', '2008', color="red", style="font-weight: bold; font-size: 200%" ) }}

Now let us move on to available macros,

"""

# -*- coding: utf-8 -*-

# Gotcha : none
#   1. While testing ZWiki, make sure that the exception is not re-raised
#      for `eval()` call.
# Notes  : none
# Todo   : 
#   1. Test case for yearsbefore macro


class ZWMacro( object ) :
    """Base Macro class that should be used to derive ZWiki Macro classes
    The following attributes are available for the ZWMacro() object.
        macronode        passed while instantiating, provides the Macro instance
        macronode.parser PLY Yacc parser
        parser.zwparser  ZWParser() object
        zwparser.tu      Translation Unit for the parsed text
        zwparser.text    Raw wiki text.
        zwparser.pptext  Preprocessed wiki text.
        zwparser.html    Converted HTML code from Wiki text
    """
    
    def __init__( self, *args, **kwargs ) :
        pass

    def on_prehtml( self,  ) :
        """Will be called before calling tohtml() method"""
        pass

    def tohtml( self ) :
        """HTML content to replace the macro text"""
        return ''

    def on_posthtml( self,  ) :
        """Will be called afater calling tohtml() method"""
        pass


from zwiki                            import split_style, constructstyle
from zwiki.macro.span                 import Span
from zwiki.macro.toc                  import Toc
from zwiki.macro.clear                import Clear
from zwiki.macro.anchor               import Anchor
from zwiki.macro.html                 import Html  
from zwiki.macro.redirect             import Redirect  
from zwiki.macro.image                import Image
from zwiki.macro.images               import Images
from zwiki.macro.yearsbefore          import YearsBefore
from zwiki.macro.projectdescription   import ProjectDescription
from zwiki.macro.projectattributes    import ProjectAttributes
from zwiki.macro.projectteam          import ProjectTeam
from zwiki.macro.projectcomponents    import ProjectComponents
from zwiki.macro.projectversions      import ProjectVersions

macronames = [ 'ZWMacro', 'Span', 'Toc', 'Clear', 'Anchor', 'Html', 'Redirect',
               'Image', 'Images', 'YearsBefore', 'ProjectDescription',
               'ProjectAttributes', 'ProjectTeam', 'ProjectComponents',
               'ProjectVersions' ]


def build_macro( macronode, macro ) :
    """Parse the macro text, like,
        {{ Macroname( arg1, arg2, kwarg1=value1, kwarg2=value2 ) }}
    To function name, *args and **kwargs
    """
    try :
        o = eval( macro[2:-2] )
    except :
        o = ZWMacro()
        # if macronode.parser.zwparser.debug :
        #     raise
    if not isinstance( o, ZWMacro ) :
        o = ZWMacro()
    zwparser = macronode.parser.zwparser

    # Setup templates and override them with computed macronode's 
    # `style`
    d_style, s_style = split_style( 
                        zwparser.macrostyles[o.__class__.__name__+'style'] )
    d_style.update( getattr( o, 'css', {} ) )
    o.style = "%s ; %s ; %s" % ( s_style, 
                                 getattr( o, 'style', '' ),
                                 constructstyle( d_style )
                               )
              

    # Register macro-node
    o.macronode = macronode
    zwparser.regmacro( o )
    return o

def macro_styles( d_style ) :
    """Extract macro-specific styles and return them as a dictionary"""
    mstyles = dict([ ( m+'style', d_style.pop( m+'style', {} ))
                     for m in macronames ])
    return mstyles
