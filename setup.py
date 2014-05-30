'''
Created on 30 mai 2014

@author: rdussurget
'''
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("cyclogeo", ["cyclogeo/__init__.py"])]
)