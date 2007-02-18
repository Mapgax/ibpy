#!/usr/bin/env python
"""IbPy - Interactive Brokers Python API

IbPy is a third-party implementation of the API used for accessing the
Interactive Brokers on-line trading system.  IbPy implements functionality
that the Python programmer can use to connect to IB, request stock ticker
data, submit orders for stocks and options, and more.
"""

import sys
from distutils.core import setup


classifiers = """
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Office/Business :: Financial
Topic :: Office/Business :: Financial :: Investment
Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
"""


doclines = __doc__.split('\n')


setup(
    name = "IbPy",
    version = "0",
    description = doclines[0],
    author = "Troy Melhase",
    author_email = "troy@gci.net",
    url = "http://code.google.com/p/ibpy/",
    license = "BSD License",
    packages = ["ib", "ib/aux", "ib/ext", "ib/opt", ],
    classifiers = filter(None, classifiers.split("\n")),
    long_description = "\n".join(doclines[2:]),
    platforms = ["any"],
    download_url = "http://code.google.com/p/ibpy/downloads/list",
)