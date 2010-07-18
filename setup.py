# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

from setuptools import setup, find_packages

long_description = """
ZWiki
=====

Wiki, in general is a simple markup language to generate html pages
that can be rendered in a browser. This is quick and neat way of 
documentation.

ZWiki is a text markup that is primarily developed for Zeta Project
Collaboration suite, visit `discoverzeta <http://www.discoverzeta.com/>`_

The Browser and its HTML are built for documentation. Wiki makes
it accessible. As a newbie, get started with ZWiki in 5 minutes.  As a pro,
never be limited by a wiki engine.
Our philosophy of wiki,

    "Make simple things easy and difficult things possible"

Some interesting features in zwiki are,

* Text content can be emphasized, italicized, underlined, subscripted,
  superscripted.
* Short cut for hyper links, several variants
* Short cut for referring to images source
* Short cut for e-email links
* Heading
* Horizontal line
* Ordered list
* Unordered list
* Block quoted text
* Small table
* Big table
* Definition list
* Style short cuts
* New line break
* Interspersing HTML text
* Templated tags for common html-tag usage patterns
* Pluggable macros
* Pluggable wiki-extensions

Quicklinks
==========

* `README <http://dev.discoverzeta.com/p/zwiki/wiki/README>`_
* `CHANGELOG <http://dev.discoverzeta.com/p/zwiki/wiki/CHANGELOG>`_
* `Track ZWiki development <http://dev.discoverzeta.com/p/zwiki>`_
* If you have any queries, suggestions
  `discuss with us <http://groups.google.com/group/zeta-discuss>`_

Documentation
=============

* `ZWiki reference <http://dev.discoverzeta.com/help/zwiki/ZWiki>`_
* `ZWiki Macors <http://dev.discoverzeta.com/help/zwiki/ZWMacros>`_
* `ZWiki Templated tags <http://dev.discoverzeta.com/help/zwiki/ZWTemplateTags>`_
* `ZWiki Extensions <http://dev.discoverzeta.com/help/zwiki/ZWExtensions>`_

"""

description='Wiki based documentation tool'

classifiers=[
'Development Status :: 4 - Beta',
'Environment :: Console',
'Environment :: Plugins',
'Environment :: Web Environment',
'Framework :: Pylons',
'Intended Audience :: Developers',
'Intended Audience :: Education',
'Intended Audience :: End Users/Desktop',
'Intended Audience :: Information Technology',
'Intended Audience :: Science/Research',
'Intended Audience :: System Administrators',
'License :: OSI Approved :: BSD License',
'Natural Language :: English',
'Operating System :: MacOS :: MacOS X',
'Operating System :: Microsoft :: Windows :: Windows CE',
'Operating System :: Microsoft :: Windows :: Windows NT/2000',
'Operating System :: POSIX',
'Operating System :: Unix',
'Programming Language :: JavaScript',
'Programming Language :: Python :: 2.5',
'Programming Language :: Python :: 2.6',
'Programming Language :: Python :: 2.7',
'Topic :: Documentation',
'Topic :: Internet',
'Topic :: Utilities',
]

setup(
    name='zwiki-zeta',
    version='0.9beta',
    py_modules=[],
    package_dir={},
    packages=find_packages(),
    ext_modules=[],
    scripts=[],
    data_files=[],
    package_data={},                        # setuptools / distutils
    include_package_data=True,              # setuptools
    exclude_package_data={},                # setuptools
    zip_safe=True,                          # setuptools
    entry_points={                          # setuptools
        'console_scripts' : [
            'zw = zwiki.zwcmd:main'
        ],
    },
    install_requires=[                      # setuptools
        'ply>=3.0',
        'pygments',
    ],
    extras_require={},                      # setuptools
    setup_requires={},                      # setuptools
    dependency_links=[],                    # setuptools
    namespace_packages=[],                  # setuptools
    test_suite='',                          # setuptools

    provides=[ 'zwiki', ],
    requires='',
    obsoletes='',

    author='Pratap R Chakravarthy',
    author_email='prataprc@discoverzeta.com',
    maintainer='Pratap R Chakravarthy',
    maintainer_email='prataprc@discoverzeta.com',
    url='http://discoverzeta.com',
    download_url='http://dev.discoverzeta.com/p/zwiki/downloads',
    license='Original BSD license',
    description=description,
    long_description=long_description,
    platforms='',
    classifiers=classifiers,
    keywords=[ 'wiki documentation web parser' ],
)
