#! /usr/bin/env python

"""Release and package tool for ZWiki,
execute this command from ZWiki repository root. Also make sure that
cleanzwiki.sh is done before executing this script."""

import os
from   os.path          import join, abspath, isdir
from   optparse         import OptionParser


usage    = "usage: %prog <cmd>"
tmpdir   = '/tmp/zwiki-release'
activate ='/tmp/zwiki-release/bin/activate'

def check() :
    """Do release check"""
    isdir( tmpdir ) and os.system( 'rm -rf %s' % tmpdir )

    eggfile = join( 'dist', os.listdir( './dist/' )[0] )

    cmd = "virtualenv --no-site-packages %s" % tmpdir
    print "    %s" % cmd
    os.system( cmd )

    cmd = 'bash -c "source %s; easy_install %s"' % (activate, eggfile)
    print "    %s" % cmd
    os.system( cmd )

    cmd = 'bash -c "source %s; easy_install nose"' % activate
    print "    %s" % cmd
    os.system( cmd )

    cwd = abspath( os.curdir )
    os.chdir( 'zwiki/test' )
    cmd = 'bash -c "source %s; ./runtest.sh"' % activate
    print "    %s" % cmd
    os.system( cmd )

def egg() :
    print "Packaging ZWiki into egg file ..."""
    cmd = 'python ./setup.py bdist_egg --exclude-source-files'
    print "    %s" % cmd
    os.system( cmd )

def cmdoptions() :
    op            = OptionParser( usage=usage )
    options, args = op.parse_args()
    return op, options, args

if __name__ == '__main__' :
    op, options, args = cmdoptions()
    options.cmd       = args and args.pop(0) or 'check'

    if options.cmd == 'check' :
        egg()
        check()
    elif options.cmd == 'egg' :
        egg()
    else :
        op.print_help()
