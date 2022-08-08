import os
import sys

def trim_nums(vals, n, style='number'):
  """ Round floats with precision larger than n

  For n = 2,

  r = trim_nums(val, n)
  
  val      r
  1     -> 1
  1.0   -> 1.0
  1.00  -> 1.00
  1.005 -> 1.01

  r = trim_nums(val, n, style='string')
  
  val      r
  1     -> '1'
  1.0   -> '1.0'
  1.00  -> '1.00'
  1.005 -> '1.01…' (Unicode ellipsis)

  val can be a list, e.g.,
  
  trim_nums([1, 1.005], 2) = [1, 1.01]
  trim_nums([1, 1.005], 2, style='string') = '[1, 1.01…]'

  """

  if isinstance(vals, list):
    for i, v in enumerate(vals):
      if v != round(v, n):
        vals[i] = round(v, n)
        if style == 'string':
          vals[i] = "{0:.4f}…".format(vals[i])
      else:
        if style == 'string':
          vals[i] = "{}".format(vals[i])
  else:
    if vals != round(vals, n):
      vals = round(vals, n)
      if style == 'string':
        vals = "{0:.4f}…".format(vals)

  if style == 'number':
    return vals
  else:
    if isinstance(vals, list):
      return "[" + "{}".format(", ".join(vals)) + "]"
    else:
      return "{}".format(vals)

def trim_nums_test():

  assert trim_nums(1, 4) == 1
  assert trim_nums(1.00001, 4) == 1.0000
  assert trim_nums(1.00005, 4) == 1.0001
  assert trim_nums([1], 4)[0] == 1
  assert trim_nums(1, 4, style='string') == "1"
  assert trim_nums(1.00001, 4, style='string') == "1.0000…"
  assert trim_nums([1.00001], 4, style='string') == "[1.0000…]"
  assert trim_nums([1.00001, 1.0], 4, style='string') == "[1.0000…, 1.0]"


def trim_iso(isostr):

  if isostr.endswith('Z'):
      isostr = isostr[0:-1]
  if isostr.endswith(':00'):
      isostr = isostr[0:-3]
  if isostr.endswith(':00'):
      isostr = isostr[0:-3]
  if isostr.endswith('T00'):
      isostr = isostr[0:-3]

  return isostr

def trim_iso_test():

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

                
def compatability_check(use=''):

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
        cmd = 'import sys;ver = sys.version_info;print(str(ver.major) + "." + str(ver.minor) + "." + str(ver.micro))'
        try:
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
        version_paths = glob.glob("/Applications/ParaView*")
        version_paths.sort()

        if len(version_paths) == 0:
            mvs.logger.error("ParaView not found in /Applications directory." \
                            " See https://www.paraview.org/download/.")
            mvs.logger.error("Exiting.")
            sys.exit(1)

        # version_paths list will have elements of, e.g.,
        # ["/Applications/ParaView-5.7.0.app", "/Applications/ParaView-5.8.0.app"].
        version_strs = []
        found = False
        version_paths_releases = []
        version_paths_masters = []
        version_ints_releases = []
        version_ints_masters = []
        for version_path in version_paths:
            mvs.logger.info("Found " + version_path)
            version_str = version_path \
                            .replace("/Applications/ParaView-", "") \
                            .replace(".app", "")
            version_strs.append(version_str)

            if use == version_str:
                found = True
                version = version_path
                break

            if 'master' in version_str:
                version_paths_masters.append(version_path)
                version_ints_masters.append([int(y) for y in version_str.replace("master-","").replace("-",'.').split(".")[0:-1]])
            else:
                version_paths_releases.append(version_path)
                version_ints_releases.append([int(y) for y in version_str.replace("-",'.').split(".")])
 
        if use == 'latest-release' or found == False:
            if len(version_paths_releases) > 0:
                # Semantic sort.
                l = sorted((e,i) for i,e in enumerate(version_ints_releases))
                version = version_paths_releases[l[-1][1]]
                found = True
        if use == 'latest-master' or found == False:
            if len(version_paths_masters) > 0:
                l = sorted((e,i) for i,e in enumerate(version_ints_masters))
                version = version_paths_masters[l[-1][1]]
                found = True

        if not found:
            if use != '':
                mvs.logger.error(f"ParaView version {use} is not installed. Installed versions include {version_strs}")
                mvs.logger.error("Exiting.")
                sys.exit(1)

        pvpython_ver_info = pvpython_version(version +  "/Contents/bin/pvpython")

        if SYSTEM_PYTHON_VERSION[0:2] == pvpython_ver_info[1][0:2]:
            PARAVIEW = version + "/Contents/MacOS/paraview"
            PVPYTHON = version + "/Contents/bin/pvpython"
            PVBATCH = version + "/Contents/bin/pvbatch"
            mvs.logger.info("Using " + use)
        else:
            descr = 'latest ParaView version on this system'
            if use != '':
                descr = 'requested ParaView version'

            msg = "\n\nSystem Python version (" + SYSTEM_PYTHON_VERSION_STRING \
                    + f") does not match Python version ({pvpython_ver_info[0]}) used by the {descr}" \
                    + f" ({version})" \
                    + f". Consider installing the needed Python version in a virtual environment.\n\n" \
                    + f"Using Anaconda, the commands are\n\n  conda create --name {pvpython_ver_info[0]} python={pvpython_ver_info[0]}\n  conda activate {pvpython_ver_info[0]}\n  pip install -e .\n"
            msg = msg + "\nThe Python version used for a given version of Paraview can be found in the filenames at https://www.paraview.org/download/\n"
            mvs.logger.error(msg)
            mvs.logger.error("Exiting.")
            sys.exit(1)

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


def fileparts(file):
    import os
    (dirname, fname) = os.path.split(file)
    (fname, fext) = os.path.splitext(fname)

    if file.startswith("http"):
        fname_split = file.split("/")
        fname, fext = os.path.splitext(fname_split[-1])
        dirname = "/".join(fname_split[0:-1])
    else:
        file_parts = fname

    return dirname, fname, fext


def dlfile(file, tmpdir=None):

    import os
    from urllib.request import urlretrieve

    import magnetovis as mvs

    if tmpdir is None:
        import tempfile
        import platform
        system = platform.system()
        if system in ["Darwin", "Linux"]:
            tmpdir = "/tmp"
        else:
            tmpdir = tempfile.gettempdir()

    (dirname, fname, fext) = fileparts(file)
    filename = fname + fext
    subdir = dirname.replace("http://","").replace("https://","")
    subdir = os.path.join(tmpdir, subdir)
    if not os.path.exists(subdir):
        mvs.logger.info("Creating " + subdir)
        os.makedirs(subdir)
    tmppath = os.path.join(subdir, filename)

    if os.path.exists(tmppath):
        mvs.logger.info("Found " + tmppath)
    else:
        partfile = tmppath + ".part"
        mvs.logger.info("Downloading " + file + " to " + partfile)
        try:
            urlretrieve(dirname + "/" + filename, partfile)
        except Error as e:
            mvs.logger.info("Download error")
            # Won't remove .part file if application crashes.
            # Would need to register an atexit.
            if os.path.exists(partfile):
                mvs.logger.info("Removing " + partfile)
                os.remove(partfile)
            raise 

        mvs.logger.info("Renaming " + partfile + "\nto\n" + tmppath)
        os.rename(partfile, tmppath)

    return tmppath
