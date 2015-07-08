# -*- coding: utf-8 -*-
'''
Created on 30 mai 2014

@author: rdussurget
'''
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name = "Cyclogeostrophy",
    version = "0.0.1",
    author = "L.Marié (IFREMER)",
    scripts = ["scripts/compute_ug.py"],
    description = ("A module to correct geostrophic current of the effects of cyclo-geostrophy force"),
    packages=['cyclogeo','cyclogeo.utils'],
    package_data={'cyclogeo.utils':['nc.yaml']}
    #~ cmdclass = {'build_ext': build_ext},
    #~ ext_modules = [
                   #~ Extension("cyclogeo",
                             #~ sources = ["cyclogeo/__init__.py"]),
                   #~ Extension("cyclogeo.utils",
                             #~ sources = ["cyclogeo/utils/__init__.py"]),
                   #~ Extension("cyclogeo.utils.Dataset",
                             #~ sources = ["cyclogeo/utils/Dataset.py"]),
                   #~ Extension("cyclogeo.utils.AGrid",
                             #~ sources = ["cyclogeo/utils/AGrid.py"]),
                   #~ Extension("cyclogeo.utils.LoadYaml",
                             #~ sources = ["cyclogeo/utils/LoadYaml.py"]),
                   #~ Extension("cyclogeo.utils.yaml_loader",
                             #~ sources = ["cyclogeo/utils/yaml_loader.py"]),
                   #~
                   #~ ]
)
#"cyclogeo/utils/AGrid.py",
#                                           "cyclogeo/utils/Dataset.py",
#                                           "cyclogeo/utils/LoadYaml.py",
#                                           "cyclogeo/utils/yaml_loader.py"]
