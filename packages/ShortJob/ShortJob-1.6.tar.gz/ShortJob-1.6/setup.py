#!/usr/bin/env python
# ====================================================
#   Copyright (C)2019 All rights reserved.
#
#   Author        : Xin-Xin MA
#   Email         : xxmawhu@163.com
#   File Name     : setup.py
#   Created Time  : 2019-09-24 10:51
#   Last Modified : 2019-09-29 12:09
#   Describe      :
#
# ====================================================

from setuptools import setup
from setuptools import find_packages
import sys
import os
m_version = "1.6"
disrip=open("README.md").read()
if sys.argv[1] == "publish":
    os.system("python setup.py sdist")
    os.system("python setup.py bdist_wheel")
    os.system("twine upload dist/*{}* --skip-existing".format(m_version))
else:
    setup(name='ShortJob',
      version=m_version,
      author='Xin-Xin Ma',
      packages=find_packages(),
      description="Multitask Multilanguage",
      project_urls={
          'Source': 'https://github.com/xxmawhu/ShortJob',
      },
      )
