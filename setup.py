import os
import sys
from setuptools import setup, find_packages
# https://stackoverflow.com/a/60740731/18433855
# Does not work.
#dist.Distribution().fetch_build_eggs(['Cython', 'numpy'])

install_requires = [
    "numpy",
    "hapiclient",
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

util.compatability_check(debug=debug)

setup(
    name='magnetovis',
    version='0.1.0',
    author='Bob Weigel, Angel Gutarra-Leon, Gary Quaresima',
    author_email='rweigel@gmu.edu',
    packages=find_packages(),
    description='Magnetosphere visualization in ParaView using Python',
    install_requires=install_requires,
    scripts=["magnetovis/magnetovis"]
)
