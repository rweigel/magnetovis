import os
import sys
from setuptools import setup, find_packages

install_requires = [
                        "numpy",
                        "spacepy"
                    ]

if sys.version_info[0] < 3:
    if sys.maxunicode > 65535:
        print('UCS4 build')
    else:
        print('UCS2 build')
else:
    build_ext = None

        
debug = False
if len(sys.argv) > 1 and sys.argv[1] == 'develop':
    debug = True
    #install_requires.append("pytest")

# https://stackoverflow.com/a/8663557
# Temporarily modify path so that util functions can be used.
setup_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(setup_path, 'magnetovis', 'magnetovis'))
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
