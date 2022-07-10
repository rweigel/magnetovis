import os
import sys
from setuptools import setup, find_packages

# TODO: If Mac M1, verify that Python is using arm64 architecture?
#       Anaconda or Miniconda for x86_64 can be installed and will
#       work on Mac M1; most of magnetovis will also work. However,
#       hxform will not work because it will be compiled as x86_64
#       and Paraview on Mac M1 is compiled using arm64.

install_requires = [
    "numpy",
    "hapiclient",
    "geopack",
    "hxform @ git+https://github.com/rweigel/hxform@main#egg=hxform"
]


debug = False
if len(sys.argv) > 1 and sys.argv[1] == 'develop':
    debug = True
    #install_requires.append("pytest")

# https://stackoverflow.com/a/8663557
# Temporarily modify path so that util.py functions can be used.
setup_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(setup_path, 'magnetovis'))
import util
del sys.path[0]

util.compatability_check()

setup(
    name='magnetovis',
    version='0.1.0',
    author='Bob Weigel, Angel Gutarra-Leon, Gary Quaresima',
    author_email='rweigel@gmu.edu',
    url='https://github.com/rweigel/magnetovis',
    license='LICENSE.txt',
    packages=find_packages(),
    description='Magnetosphere visualization in ParaView using Python',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    scripts=["magnetovis/magnetovis"],
    include_package_data=True
)