import os
import sys


def tstr(time, length=7):
    """Create ISO8601 date/time string
    
    tstr((2000, 1, 1, 2)) # 2000-01-01T02:00:00
    tstr((2000, 1, 1, 2, 3)) # 2000-01-01T02:03:00
    tstr((2000, 1, 1, 2, 3, 4)) # 2000-01-01T02:03:04
    tstr((2000, 1, 1, 2, 3, 4, 567)) # 2000-01-01T02:03:04.000567
    """
    import datetime
    assert(len(time) > 2)

    time = datetime.datetime(*time)
    time_str = time.isoformat()

    if length == 7:
        l = len("2000-01-01T02:03:04.000567")
    elif length == 6:
        l = len("2000-01-01T02:03:04")
    elif length == 5:
        l = len("2000-01-01T02:03")
    elif length == 4:
        l = len("2000-01-01T02")
    elif length == 3:
        l = len("2000-01-01")
    
    return time_str[0:l]


def time2datetime(t):
    import datetime as dt

    t = list(t)
    for i in range(len(t)):
        if int(t[i]) != t[i]:
            raise ValueError("int(t[{0:d}] != t[{0:d}] = {1:f}".format(i, t[i]))\
        
        t[i] = int(t[i])

    if len(t) < 3:
        raise ValueError('Time list/tuple must have 3 or more elements')
    else:
        return dt.datetime(*t)


def prompt(question, default=''):
    # Based on suggestions in https://gist.github.com/garrettdreyfus/8153571

    import sys
    if sys.version_info[0] > 2:
        reply = str(input(question + ': ')).lower().strip()
    else:
        reply = str(raw_input(question + ': ')).lower().strip()

    if len(reply) == 0:
        return default
    return reply[:1] 


def install_paraview(paraview_version, install_path='/tmp/'):


    def extract(fullpath, install_path):
        cmd_list = ['tar', 'zxf', '--checkpoint', 10000, '--checkpoint-action="echo=Extracted file %u/124000"',fullpath, '--directory', install_path]
        print('Executing ' + ' '.join(cmd_list))
        import subprocess
        subprocess.run(cmd_list)
        
    file = paraview_version + '.tar.gz'  
    tmpdir = '/tmp/'
    fullpath = tmpdir + file

    if os.path.exists(fullpath):
        extract(fullpath, install_path)
        return
    
    print('Downloading ' + file + ' to ' + tmpdir)
    url = 'https://www.paraview.org/paraview-downloads/download.php?' + \
          'submit=Download&version=v5.8&type=binary&os=Linux&downloadFile=' + file 

    # https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
    from clint.textui import progress
    import requests

    r = requests.get(url, stream=True)
    with open(fullpath, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

                
def compatability_check(debug=False):

    import os
    import glob
    import site
    import warnings
    import subprocess
        
    debug = True

    ver = sys.version_info
    SYSTEM_PYTHON_VERSION = list(ver[0:2])
    SYSTEM_PYTHON_VERSION_STRING = str(ver.major) + "." + str(ver.minor) + "." + str(ver.micro)

    PARAVIEW_PYTHON_VERSIONS = {
                                "5.9.0": [3,8,8],
                                "5.9.1": [3,8,8]
                                }

    if debug:
        print('sys.platform = ' + sys.platform)
    if sys.platform.startswith("darwin"):
        versions = glob.glob("/Applications/ParaView*")
        versions.sort()
        version = versions[-1]
        if len(version) == 0:
            print("ParaView not found in /Applications directory." \
                " To install ParaView, see https://www.paraview.org/download/.")
            print("Exiting.")
            # TODO?: Allow for ParaView not located in /Applications/
            sys.exit(1)
        use = ""
        # versions list will have elements of, e.g.,
        # ["/Applications/ParaView-5.7.0.app", "/Applications/ParaView-5.8.0.app"].
        version_strs = []
        for version in versions:
            if debug:
                print("Found " + version)
            version_str = version \
                            .replace("/Applications/ParaView-", "") \
                            .replace(".app", "")
            version_strs.append(version_str)
            version_num = [int(i) for i in version_str.split(".")]
            # version_num is tuple of (major, minor, patch)
            if version_str in PARAVIEW_PYTHON_VERSIONS \
                and SYSTEM_PYTHON_VERSION[0:2] == PARAVIEW_PYTHON_VERSIONS[version_str][0:2]:
                use = version
                PARAVIEW = use + "/Contents/MacOS/paraview"
                PVPYTHON = use + "/Contents/bin/pvpython"
                PVBATCH = use + "/Contents/bin/pvbatch"

        if use == "":
            msg = "System Python version (" + SYSTEM_PYTHON_VERSION_STRING + ") does not match Python used by available ParaView version(s) " + ", ".join(version_strs) + ". Consider installing the needed Python version in a virtual environment. Using Anaconda the commands are\n\n  conda create --name 3.8 python=3.8\n  conda activate 3.8\n  pip install magnetovis\n"
            msg = msg + "\nAllowed Paraview/Python versions:\n"
            for pv_ver in PARAVIEW_PYTHON_VERSIONS:                
                msg = msg + " ParaView " + pv_ver + " and Python " + ".".join(str(x) for x in PARAVIEW_PYTHON_VERSIONS[pv_ver][0:2]) + "\n"
            print(msg)
            print("Exiting.")
            #raise ValueError(msg)
            sys.exit(1)
        else:
            if debug:
                print("Using " + use)

    elif sys.platform.startswith("linux"):

        if sys.version_info[0] < 3:
            import ConfigParser
            config = ConfigParser.ConfigParser()
        else:
            import configparser
            config = configparser.ConfigParser()


        config_file = os.path.expanduser('~') + '/.magnetovis.conf'
        PARAVIEWPATH = ''
        if 'PARAVIEWPATH' in os.environ:
            if debug:
                print('PARAVIEW os environment variable set as ' + os.environ['PARAVIEWPATH'])
            PARAVIEWPATH = os.path.expanduser(config['DEFAULT']['PARAVIEWPATH'])                
            PARAVIEW = PARAVIEWPATH + '/bin/paraview'
            PVPYTHON = PARAVIEWPATH + '/bin/pvpython'
            PVBATCH = PARAVIEWPATH + '/bin/pvbatch'

        else:
            if debug:
                print('PARAVIEW os environment not set.')
            
        if PARAVIEWPATH == '' and os.path.exists(config_file):
            if debug:
                print('File ' + config_file + ' found')
            config.read(config_file)
            try:
                PARAVIEWPATH = os.path.expanduser(config.get('DEFAULT', 'PARAVIEWPATH'))
                if debug:
                    print('Found PARAVIEWPATH = ' + PARAVIEWPATH + ' in [DEFAULT] section of ' + config_file + '.')
                if os.path.exists(PARAVIEWPATH):
                    PARAVIEW = PARAVIEWPATH + '/bin/paraview'
                    PVPYTHON = PARAVIEWPATH + '/bin/pvpython'
                else:
                    print(PARAVIEWPATH + ' not found.')
                    PARAVIEWPATH = ''
            except:
                if debug:
                    print('unable to get PARAVIEWPATH variable in ' + config_file + ' file')

        if PARAVIEWPATH == '':
            PVPYTHON = ''
            try:
                if debug:
                    print('Trying output of `which paraview`')
                PARAVIEW = subprocess.check_output(['which','paraview'])
                try:
                    if debug:
                        print('Trying output of `which pvpython`')
                    PVPYTHON = subprocess.check_output(['which','pvpython'])
                except:
                    print("Executable named 'pvpython' was not found in path, but 'paraview' found at " \
                          + PARAVIEW + ". Check installation; pvpython binary should be in the " \
                          + "same directory as paraview binary.")
                    sys.exit(1)
            except:
                print("Executable named 'paraview' was not found in path.")
                if prompt('Attempt to install? [y]/n', default='y') == 'y':
                    install_path = prompt('Enter installation path [~]', default='~')
                    install_path = os.path.expanduser(install_path)
                    paraview_version = 'ParaView-5.8.0-MPI-Linux-Python3.7-64bit'
                    install_paraview(paraview_version, install_path=install_path)
                    PARAVIEWPATH = install_path + '/' + paraview_version
                    PARAVIEW = PARAVIEWPATH + '/bin/paraview'
                    PVPYTHON = PARAVIEWPATH + '/bin/pvpython'
                    config = configparser.ConfigParser()
                    if os.path.exists(config_file):
                        if debug:
                            print("Found " + config_file + ". Updating PARAVIEWPATH " + \
                                  "variable to " + PARAVIEWPATH)
                        config.read(config_file)
                        if 'PARAVIEWPATH' in config['DEFAULT']:
                            config['DEFAULT']['PARAVIEWPATH'] = PARAVIEWPATH
                        else:
                            config['DEFAULT'] = {'PARAVIEWPATH': PARAVIEWPATH}
                        with open(config_file, 'w') as f:
                            config.write(f)
                        if debug:
                            print("Updated PARAVIEWPATH variable to " + PARAVIEWPATH)
                    else:
                        if debug:
                            print("Writing " + config_file)
                        config['DEFAULT'] = {'PARAVIEWPATH': install_path}
                        with open(config_file, 'w') as f:
                            config.write(f)
                        if debug:
                            print("Wrote " + config_file)
                else:
                    sys.exit(1)
                            
    else:
        print("Installation implemented only for Linux and OS-X.")
        sys.exit(0)

    if False:
        util_path = os.path.dirname(os.path.realpath(__file__))
        ver_path = os.path.join(util_path,'..','etc','version.py')
        if debug:
            print("Executing %s %s" % (PVPYTHON, ver_path))
        try:
                pvpython_version_str = subprocess.check_output([PVPYTHON, ver_path])
        except:
            print("Could not execute " + PVPYTHON + " " + ver_path + ". Exiting.")
            sys.exit(1)

    return PARAVIEW, PVPYTHON, PVBATCH
