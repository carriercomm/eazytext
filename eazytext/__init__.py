# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

__version__ = '0.92dev'

import codecs
from   os.path                  import dirname
from   copy                     import deepcopy
from   datetime                 import datetime as dt

from   zope.component           import getGlobalSiteManager
import pkg_resources            as pkg

# Import macro-plugins so that they can register themselves.
import eazytext.macro
# Import extension-plugins so that they can register themselves.
import eazytext.extension

from   eazytext.interfaces      import IEazyTextMacroFactory, \
                                       IEazyTextExtensionFactory
from   eazytext.parser          import ETParser

DEFAULT_ENCODING = 'utf-8'

defaultconfig = {
    # Development mode settings
    'devmod': True,
    # List of directories to look for the .etx file
    'directories' : '.',
    # path to store the compiled .py file (intermediate file)
    'module_directory' : None,
    # CSV of escape filter names to be applied for expression substitution
    'escape_filters' : 'uni',
    # Default input endcoding for .etx file.
    'input_encoding': DEFAULT_ENCODING,
    # CSV list of plugin packages that needs to be imported, before compilation.
    'plugin_packages'   : '',
    # Default skin file to include translated html file, use this option along
    # with `include_skin`.
    'skinfile' : 'default.css',
    'include_skin' : False,
    # If set to true, the email-id generated using [[ mailto:... ]] markup will
    # be obfuscated.
    'obfuscatemail' : False,
    # Denotes that the parser is invoked by a parent parser, may be because of
    # a plugin
    'nested' : False,
    # Do not allow any <script> tag in the finally generated HTML text.
    'stripscript' : True,
    # If set to false generate the html text enclosed within <article> tag, else
    # wrap them withing <html><body> tag
    'ashtml' : False,
}

macroplugins = {}         # { plugin-name   : instance }
extplugins   = {}         # { plugin-name   : instance }
init_status = 'pending'
def initplugins( etxconfig, force=False ):
    """Collect and organize macro plugins and extension plugins implementing
    the interfaces,
        IEazyTextMacroFactory, IEazyTextExtensionFactory
    """
    global macroplugins, extplugins
    if init_status == 'progress' :
        return etxconfig

    if (force == True) or etxconfig.get( 'macroplugins', None ) == None :
        # Load and classify plugins
        init_status = 'progress'
        gsm = getGlobalSiteManager()

        # Load plugin packages
        packages = etxconfig['plugin_packages']
        packages = filter(None, [ x.strip(' \t') for x in packages.split(',') ])
        [ __import__(pkg) for pkg in filter(None, packages) ]

        # Gather plugins template tag handlers, filter-blocks
        for x in gsm.registeredUtilities() :
            if x.provided == IEazyTextMacroFactory :    # Filter blocks
                macroplugins[x.name] = x.component
            if x.provided == ITayraEscapeFilter :   # Escape Filters
                extplugins[x.name] = x.component
            etxconfig['macroplugins'] = macroplugins
            etxconfig['extplugins'] = extplugins

    init_status = 'done'
    return etxconfig


#---- APIs for executing Tayra Template Language

class Translate( object ):
    def __init__( self, etxloc=None, etxtext=None, etxconfig_ ):
        """`etxconfig` parameter will find its way into every object defined
        by wiki processor.
            TODO : somehow find a way to pass the arguments to `body` function
        """
        etxconfig = deepcopy( defaultconfig )
        etxconfig.update( etxconfig_ )
        # Initialize plugins
        self.etxconfig = initplugins( etxconfig, force=etxconfig['devmod'] )
        self.etxloc, self.etxtext = etxloc, self.etxtext
        self.etparser = ETParser( etxconfig=etxconfig )

    def __call__( self, entry='body', context={} ):
        from  eazytext.compiler  import Compiler, TemplateLookup
        self.compiler = Compiler(
            self.etxloc, etxconfig=self.etxconfig, etparser=self.etparser
        )
        context['_etxcontext'] = context
        module = self.compiler.execetx( context=context )
        entry = getattr( module, entryfn )
        html = entry() if callable( entry ) else ''
        return html

def etx_cmdline( etxloc, **kwargs ):
    from eazytext.compiler import Compiler, TemplateLookup

    etxconfig = deepcopy( defaultconfig )
    # directories, module_directory, devmod
    ttlconfig.update( kwargs )
    ttlconfig.setdefault( 'module_directory', dirname( ttlloc ))

    # Parse command line arguments and configuration
    args = eval( ttlconfig.pop( 'args', '[]' ))
    context = eval( ttlconfig.pop( 'context', '{}' ))
    debuglevel = ttlconfig.pop( 'debuglevel', 0 )
    show = ttlconfig.pop( 'show', False )
    dump = ttlconfig.pop( 'dump', False )
    encoding = ttlconfig['input_encoding']

    # Initialize plugins
    ttlconfig = initplugins( ttlconfig, force=ttlconfig.get('devmod', True) )

    # Setup parser
    ttlparser = TTLParser( debug=debuglevel, ttlconfig=ttlconfig )
    compiler = Compiler( ttlloc, ttlconfig=ttlconfig, ttlparser=ttlparser )
    pyfile = compiler.ttlfile+'.py'
    htmlfile = compiler.ttlfile.rsplit('.', 1)[0] + '.html'

    if debuglevel :
        print "AST tree ..."
        tu = compiler.toast()
    elif show :
        print "AST tree ..."
        tu = compiler.toast()
        tu.show()
    elif dump :
        tu = compiler.toast()
        rctext =  tu.dump()
        if rctext != codecs.open( compiler.ttlfile, encoding=encoding ).read() :
            print "Mismatch ..."
        else : print "Success ..."
    else :
        print "Generating py / html file ... "
        pytext = compiler.topy()
        # Intermediate file should always be encoded in 'utf-8'
        codecs.open(pyfile, mode='w', encoding=DEFAULT_ENCODING).write(pytext)

        #code = compiler.ttl2code( pyfile=pyfile, pytext=pytext )
        #context['_ttlcontext'] = context
        #module = compiler.execttl( code, context=context )
        ## Fetch parent-most module
        #body = getattr( module.self, 'body' )
        #html = body( *args ) if callable( body ) else ''

        ttlconfig.setdefault( 'memcache', 'true' )
        r = Renderer( ttlloc, ttlconfig )
        html = r( context=context )
        codecs.open( htmlfile, mode='w', encoding=encoding).write( html )

        # This is for measuring performance
        st = dt.now()
        [ r( context=context ) for i in range(10) ]
        print (dt.now() - st) / 10

