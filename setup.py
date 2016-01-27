# -*-
#
# @author: jaumebonet
# @email:  jaume.bonet@gmail.com
# @url:    jaumebonet.github.io
#
# @date:   2016-01-19 17:26:20
#
# @last modified by:   jaumebonet
# @last modified time: 2016-01-27 18:19:47
#
# -*-
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
__version__ = '0.0.1'

setup(
    name='RGcrawler',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=__version__,

    description='A Python Library to crawl ResearchGate',
    # long_description=read('README.md'),

    # The project's main homepage.
    url='https://github.com/jaumebonet/RGcrawler',
    download_url = 'https://github.com/jaumebonet/RGcrawler/archive/{0}.tar.gz'.format(__version__),

    # Author details
    author='Jaume Bonet',
    author_email='jaume.bonet@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    platforms='UNIX',
    keywords='development',

    install_requires=['pynion==0.0.4', 'beautifulsoup4>=4.0'],
    dependency_links=['git+https://github.com/jaumebonet/pynion.git@0.0.4#egg=pynion-0.0.4'],

    packages=find_packages(exclude=['docs', 'test']),

    zip_safe = False,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'RGcrawler=RGcrawler:main',
        ],
    },
)
