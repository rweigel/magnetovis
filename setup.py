# Not tested
import os
import sys
import warnings
import subprocess
from setuptools import setup, find_packages

install_requires = ["numpy",
                    "spacepy",
                    "hapiclient"]

debug = False
if len(sys.argv) > 1 and sys.argv[1] == 'develop':
    debug = True
    #install_requires.append("pytest")

if sys.platform == "darwin":
    import glob
    versions = glob.glob("/Applications/ParaView*")
    versions.sort()
    version = versions[-1]
    if len(version) == 0:
        print("ParaView not found in /Applications directory." \
            " Install ParaView using https://www.paraview.org/download/.")
        # TODO: Allow for ParaView not located in /Applications/
        sys.exit(1)
    use = ""
    # versions list will have elements of, e.g.,
    # ["/Applications/ParaView-5.7.0.app", "/Applications/ParaView-5.8.0.app"].
    for version in versions:
        if debug:
            print("Found " + version)
        version_str = version.replace("/Applications/ParaView-", "").replace(".app", "")
        version_num = [int(i) for i in version_str.split(".")]
        # version_num will be tuple of (major, minor, patch)
        if list(sys.version_info[0:2]) > [2, 7] and version_num <= [5, 8]:
            if debug:
                print('Python > 2.7 is not compatible with ParaView ' \
                    + version_str + ' on OS-X.')
        elif list(sys.version_info[0:2]) == [2, 7] and version_num[0:2] == [5, 8]:
            if debug:
                print('Python 2.7 is not compatible with ParaView ' \
                    + version_str + ' on OS-X. See ' \
                    + 'https://gitlab.kitware.com/paraview/paraview/-/issues/20146')
        else:            
            use = version
            PARAVIEW = use + "/Contents/MacOS/paraview"
            PVPYTHON = use + "/Contents/bin/pvpython"
    if use == "":
        sys.exit(1)
    else:
        if debug:
            print("Using " + use)

elif sys.platform == "linux":
    try:
        paraview_path = subprocess.check_output(['which','python'])
    except:
        print("Executable named 'paraview' was not found in path. " \
            " Install ParaView such that 'which paraview' returns location of paraview.")
        sys.exit(1)
else:
    print("Installation implemented only for Linux and OS-X.")
    sys.exit(0)

#print(os.environ)
import site; 
print(site.getsitepackages())
PYTHONPATH = "/opt/anaconda3/envs/python2.7/lib/python2.7/site-packages"
pvargs = " ".join(sys.argv[1:])
syscom = "PYTHONPATH=" + PYTHONPATH + ":. " + PARAVIEW + " " + pvargs
print(syscom)

import sys
ver = sys.version_info
print(str(ver.major) + "." + str(ver.minor) + "." + str(ver.micro))

try:
    # N.B.: Assumes that if paraview is in path, so is pvpthon.
    # misc/version.py outputs version string of Python used by pvpython.
    pvpython_version_str = subprocess.check_output([PVPYTHON,'version.py'])
    pvpython_version_str = pvpython_version_str.decode().strip()
    pvpython_version_lst = [int(i) for i in pvpython_version_str.split(".")]
    print(pvpython_version_lst)
    print("pvpython = " + str(pvpython_version_lst[0:2]))
    print("python = " + str(sys.version_info[0:2]))
    if pvpython_version_lst[0:2] == (2, 7) and sys.version_info[0:2] != (2, 7):
        print('Installed ParaView uses Python 2.7 and so magnetovis requires Python 2.7.')
        sys.exit(1)
    if sys.version_info[0:2] != pvpython_version_lst[0:2]:
        ver = sys.version_info
        python_version_str = str(ver.major) + "." + str(ver.minor) + "." + str(ver.micro)

        def _warning(message, category=UserWarning, filename='', lineno=-1, file=None, line=''):
            print("UserWarning: " + str(message))
        warnings.showwarning = _warning

        warnings.warn("Installed ParaView uses Python " + pvpython_version_str \
                    + " and magnetovis is being installed for Python " \
                    + python_version_str \
                    + ". There may be compatability issues if you use " \
                    + "libraries and code used are not compatable with Python " \
                    + pvpython_version_str + ".")
except:
    print("Could not execute " + PVPYTHON + ".")
    sys.exit(1)

#eval "PYTHONPATH=/opt/anaconda3/envs/python2.7/lib/python2.7/site-packages:. $PARAVIEW $@"

if False:
    setup(
        name='magnetovis',
        version='0.1.0',
        author='Bob Weigel, Angel Gutarra-Leon, Gary Quaresima',
        author_email='rweigel@gmu.edu',
        packages=find_packages(),
        description='Magnetosphere visualization in ParaView using Python',
        install_requires=install_requires
    )
