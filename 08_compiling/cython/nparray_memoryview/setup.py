#from distutils.core import setup
from setuptools import setup
import numpy as np

from Cython.Build import cythonize
setup(ext_modules=cythonize("cythonfn.pyx"),
      include_dirs=[np.get_include()])

