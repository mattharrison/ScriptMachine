# Copyright (c) 2009 Matt Harrison
from distutils.core import setup
#from setuptools import setup

from scriptmachinelib import meta

setup(name='ScriptMachine',
      version=meta.__version__,
      author=meta.__author__,
      description='FILL IN',
      scripts=['bin/scriptmachine'],
      package_dir={'scriptmachinelib':'scriptmachinelib'},
      packages=['scriptmachinelib'],
)
