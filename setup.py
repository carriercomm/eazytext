from setuptools import setup, find_packages

long_description = """
Wiki in general is a simple markup language to generate html formatted pages
that can be rendered in a browser. This helps in quick and neat way of
documentation.
ZWiki is a markup language that is primarily developed for Zeta Project
Managment and SCM web application.
"""

description='Wiki Parser and HTML translator'

setup(
    name='zwiki',
    version='0.83dev',
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
    ],
    extras_require={},                      # setuptools
    setup_requires={},                      # setuptools
    dependency_links=[],                    # setuptools
    namespace_packages=[],                  # setuptools
    test_suite='',                          # setuptools
    #test_loader='',                        # setuptools
    #eager_resources='',                    # setuptools

    provides='',
    requires='',
    obsoletes='',

    author='R Pratap Chakravarthy',
    author_email='prataprc@gmail.com',
    maintainer='R Pratap Chakravarthy',
    maintainer_email='prataprc@gmail.com',
    url='',
    download_url='',
    license='',
    description=description,
    long_description=long_description,
    platforms='',
    classifiers=[],
    keywords='',
)
