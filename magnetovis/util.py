import os
import sys


def trim_iso(isostr):

    if isostr.endswith('Z'):
        isostr = isostr[0:-1]
    if isostr.endswith(':00'):
        isostr = isostr[0:-3]
    if isostr.endswith(':00'):
        isostr = isostr[0:-3]
    if isostr.endswith('T00'):
        isostr = isostr[0:-3]

    if False:
        assert trim_iso('2000-01-01T00:00:00') == "2000-01-01", ""
        assert trim_iso('2000-01-01T00:00') == "2000-01-01", ""
        assert trim_iso('2000-01-01T00') == "2000-01-01", ""

        assert trim_iso('2000-01-01T00:00:00Z') == "2000-01-01", ""
        assert trim_iso('2000-01-01T00:00Z') == "2000-01-01", ""
        assert trim_iso('2000-01-01T00Z') == "2000-01-01", ""

        assert trim_iso('2000-01-01T01:00:00') == "2000-01-01T01", ""
        assert trim_iso('2000-01-01T01:00') == "2000-01-01T01", ""
        assert trim_iso('2000-01-01T01') == "2000-01-01T01", ""

        assert trim_iso('2000-01-01T01:00:00Z') == "2000-01-01T01", ""
        assert trim_iso('2000-01-01T01:00Z') == "2000-01-01T01", ""
        assert trim_iso('2000-01-01T01Z') == "2000-01-01T01", ""

    return isostr


def iso2ints(isostr):
    import re
    tmp = re.split("-|:|T|Z", isostr)
    if len(tmp) > 6:
        tmp = tmp[0:5]

    int_list = []
    for str_int in tmp:
        if str_int != "Z" and str_int != '':
            int_list.append(int(str_int))

    return int_list


def tstr(time, length=7):
    """Create ISO8601 date/time string from integers
    
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
        mvs.logger.info('Executing ' + ' '.join(cmd_list))
        import subprocess
        subprocess.run(cmd_list)
        
    file = paraview_version + '.tar.gz'  
    tmpdir = '/tmp/'
    fullpath = tmpdir + file

    if os.path.exists(fullpath):
        extract(fullpath, install_path)
        return
    
    mvs.logger.info('Downloading ' + file + ' to ' + tmpdir)
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

                
def compatability_check():

    import os
    import glob
    import site
    import warnings
    import subprocess

    import magnetovis as mvs

    mvs.logger.info("Called")

    ver = sys.version_info
    SYSTEM_PYTHON_VERSION = list(ver[0:2])
    SYSTEM_PYTHON_VERSION_STRING = str(ver.major) + "." + str(ver.minor) + "." + str(ver.micro)

    def pvpython_version(PVPYTHON):
        util_path = os.path.dirname(os.path.realpath(__file__))
        try:
            cmd = 'import sys;ver = sys.version_info;print(str(ver.major) + "." + str(ver.minor) + "." + str(ver.micro))'
            mvs.logger.info("Executing:\n\n" + PVPYTHON + " -c '" + cmd + "'\n")
            cmd = [PVPYTHON,'-c',cmd]
            stdout = subprocess.check_output(cmd, encoding='utf-8')
        except:
            mvs.logger.error("Could not execute " + PVPYTHON + " " + cmd + ". Exiting.")
            sys.exit(1)
        version_list = stdout.strip().split(".")
        version_listi = [int(i) for i in version_list]
        return [stdout.strip(), version_listi]

    mvs.logger.info('sys.platform = ' + sys.platform)
    if sys.platform.startswith("darwin"):
        versions = glob.glob("/Applications/ParaView*")
        versions.sort()
        version = versions[-1]

        if len(version) == 0:
            mvs.logger.error("ParaView not found in /Applications directory." \
                            " See https://www.paraview.org/download/.")
            mvs.logger.error("Exiting.")
            # TODO?: Allow for ParaView not located in /Applications
            sys.exit(1)

        # versions list will have elements of, e.g.,
        # ["/Applications/ParaView-5.7.0.app", "/Applications/ParaView-5.8.0.app"].
        version_strs = []
        for version in versions:
            mvs.logger.info("Found " + version)
            version_str = version \
                            .replace("/Applications/ParaView-", "") \
                            .replace(".app", "")
            version_strs.append(version_str)

        #version_num = [int(i) for i in version_str.split(".")]
        # version_num is tuple of (major, minor, patch)
        pvpython_ver_info = pvpython_version(version +  "/Contents/bin/pvpython")
        #print(pvpython_ver_info)

        use = None
        if SYSTEM_PYTHON_VERSION[0:2] == pvpython_ver_info[1][0:2]:
            use = versions[-1]
            PARAVIEW = use + "/Contents/MacOS/paraview"
            PVPYTHON = use + "/Contents/bin/pvpython"
            PVBATCH = use + "/Contents/bin/pvbatch"

        if use is None:
            msg = "\n\nSystem Python version (" + SYSTEM_PYTHON_VERSION_STRING \
                    + f") does not match Python version ({pvpython_ver_info[0]}) used by newest ParaView version on this system " \
                    + f" ({version})" \
                    + f". Consider installing the needed Python version in a virtual environment.\n\n" \
                    + f"Using Anaconda, the commands are\n\n  conda create --name {pvpython_ver_info[0]} python={pvpython_ver_info[0]}\n  conda activate {pvpython_ver_info[0]}\n  pip install -e .\n"
            msg = msg + "\nThe Python version used for a given version of Paraview can be found in the filenames at https://www.paraview.org/download/\n"
            mvs.logger.error(msg)
            mvs.logger.error("Exiting.")
            #raise ValueError(msg)
            sys.exit(1)
        else:
            mvs.logger.info("Using " + use)

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
            mvs.logger.info('PARAVIEW os environment variable set as ' + os.environ['PARAVIEWPATH'])
            PARAVIEWPATH = os.path.expanduser(config['DEFAULT']['PARAVIEWPATH'])                
            PARAVIEW = PARAVIEWPATH + '/bin/paraview'
            PVPYTHON = PARAVIEWPATH + '/bin/pvpython'
            PVBATCH = PARAVIEWPATH + '/bin/pvbatch'

        else:
            mvs.logger.info('PARAVIEW os environment not set.')
            
        if PARAVIEWPATH == '' and os.path.exists(config_file):
            mvs.logger.info('File ' + config_file + ' found')
            config.read(config_file)
            try:
                PARAVIEWPATH = os.path.expanduser(config.get('DEFAULT', 'PARAVIEWPATH'))
                mvs.logger.info('Found PARAVIEWPATH = ' + PARAVIEWPATH + ' in [DEFAULT] section of ' + config_file + '.')
                if os.path.exists(PARAVIEWPATH):
                    PARAVIEW = PARAVIEWPATH + '/bin/paraview'
                    PVPYTHON = PARAVIEWPATH + '/bin/pvpython'
                else:
                    mvs.logger.info(PARAVIEWPATH + ' not found.')
                    PARAVIEWPATH = ''
            except:
                mvs.logger.info('Unable to get PARAVIEWPATH variable in ' + config_file + ' file')

        if PARAVIEWPATH == '':
            PVPYTHON = ''
            try:
                mvs.logger.info('Trying output of `which paraview`')
                PARAVIEW = subprocess.check_output(['which','paraview'])
                try:
                    mvs.logger.info('Trying output of `which pvpython`')
                    PVPYTHON = subprocess.check_output(['which','pvpython'])
                except:
                    mvs.logger.error("Executable named 'pvpython' was not found in path, but 'paraview' found at " \
                          + PARAVIEW + ". Check installation; pvpython binary should be in the " \
                          + "same directory as paraview binary.")
                    sys.exit(1)
            except:
                mvs.logger.info("Executable named 'paraview' was not found in path.")
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
                        mvs.logger.info("Found " + config_file \
                                        + ". Updating PARAVIEWPATH " \
                                        + "variable to " + PARAVIEWPATH)
                        config.read(config_file)
                        if 'PARAVIEWPATH' in config['DEFAULT']:
                            config['DEFAULT']['PARAVIEWPATH'] = PARAVIEWPATH
                        else:
                            config['DEFAULT'] = {'PARAVIEWPATH': PARAVIEWPATH}
                        with open(config_file, 'w') as f:
                            config.write(f)
                        mvs.logger.info("Updated PARAVIEWPATH variable to " + PARAVIEWPATH)
                    else:
                        mvs.logger.info("Writing " + config_file)
                        config['DEFAULT'] = {'PARAVIEWPATH': install_path}
                        with open(config_file, 'w') as f:
                            config.write(f)
                        mvs.logger.info("Wrote " + config_file)
                else:
                    sys.exit(1)
                            
    else:
        mvs.logger.error("Installation implemented only for Linux and OS-X.")
        sys.exit(0)

    return PARAVIEW, PVPYTHON, PVBATCH

