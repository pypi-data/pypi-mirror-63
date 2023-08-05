# -*- coding: utf-8 -*-
"""
    podgen.version
    ~~~~~~~~~~~~~~~

    :copyright: 2013-2015, Lars Kiesow <lkiesow@uos.de> and 2016, Thorben Dahl
        <thorben@sjostrom.no>

    :license: FreeBSD and LGPL, see license.* for more details.

"""
# Support for Python 2.7
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import *

'Version of python-podgen represented as tuple'
version = (1, 1, "0-rc", 1)


'Version of python-podgen represented as string'
version_str = '.'.join([str(x) for x in version])

version_major = version[:1]
version_minor = version[:2]
version_full  = version

version_major_str = '.'.join([str(x) for x in version_major])
version_minor_str = '.'.join([str(x) for x in version_minor])
version_full_str  = '.'.join([str(x) for x in version_full])

'Name of this project'
name = "python-podgen"

'Website of this project'
website = "https://podgen.readthedocs.org"
