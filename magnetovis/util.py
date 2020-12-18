import os
import sys

# TODO: Remove
def tstrTimeDelta(time, minute_delta):
    from datetime import timedelta
    
    t_datetime = time2datetime(time) + timedelta(minutes=minute_delta)
    return tstr(t_datetime)


# TODO: Duplicated in Gary's
def tpad(time, length=7):

    # TODO: Check that time is valid
    time = list(time)

    assert(len(time) > 2)
    
    if len(time) > length:
        time = time[0:length]
    else:
        pad = length - len(time)
        time = time + pad*[0]

    return tuple(time)


# TODO: Duplicated in Gary's
def tstr(time, length=7):
    """Create date/time string of the convention to tag files with given array of integers
    
    tstr((2000, 1, 1, 2)) # 2000:01:01T02:00:00
    tstr((2000, 1, 1, 2, 3)) # 2000:01:01T02:03:00
    tstr((2000, 1, 1, 2, 3, 4)) # 2000:01:01T02:03:04
    tstr((2000, 1, 1, 2, 3, 4, 567)) # 2000:01:01T02:03:04.567
    """
    import datetime
    
    if isinstance(time, datetime.date ):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    else:
        # ISO 8601
        assert(len(time) > 2)
    
        if length == 7:
            return '%04d-%02d-%02dT%02d:%02d:%02d.%03d' % tpad(time, length=length)
        elif length == 6:
            return '%04d-%02d-%02dT%02d:%02d:%02d' % tpad(time, length=length)        
        elif length == 5:
            return '%04d-%02d-%02dT%02d:%02d' % tpad(time, length=length)        
        elif length == 4:
            return '%04d-%02d-%02dT%02d' % tpad(time, length=length)        
        elif length == 3:
            return '%04d-%02d-%02d' % tpad(time, length=length)        

# TODO: Duplicated in Gary's
def time2datetime(t):
    import datetime as dt
    
    for i in range(len(t)):
        if int(t[i]) != t[i]:
            raise ValueError("int(t[{0:d}] != t[{0:d}] = {1:f}".format(i, t[i]))\
            
    if len(t) < 3:
        raise ValueError('Time list/tuple must have 3 or more elements')
    if len(t) == 3:
        return dt.datetime(int(t[0]), int(t[1]), int(t[2]))    
    if len(t) == 4:
        return dt.datetime(int(t[0]), int(t[1]), int(t[2]), int(t[3]))    
    if len(t) == 5:
        return dt.datetime(int(t[0]), int(t[1]), int(t[2]), int(t[3]), int(t[4]))    
    if len(t) == 6:
        return dt.datetime(int(t[0]), int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]))    
    if len(t) == 7:
        return dt.datetime(int(t[0]), int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]), int(t[6]))    


# TODO: Use version in hapiclient.py
def urlretrieve(url, fname):
    """Python 2/3 urlretrieve compatability function.

    If Python 3, returns
    urllib.request.urlretrieve(url, fname)

    If Python 2, returns
    urllib.urlretrieve(url, fname)
    """

    import sys

    if sys.version_info[0] > 2:
        import urllib.request, urllib.error
        try:
            res = urllib.request.urlretrieve(url, fname)
            return res
        except urllib.error.URLError as e:
            print(e)
        except ValueError as e:
            print("'" + url + "' is not a valid URL")
    else:
        import urllib, urllib2 #, ssl
        try:
            #context = ssl._create_unverified_context()
            urllib2.urlopen(url) 
            res = urllib.urlretrieve(url, fname)#, context=context)
            return res
        #https://stackoverflow.com/questions/16778435/python-check-if-website-exists
        except urllib2.HTTPError, e: 
            return(e.code)
        except urllib2.URLError, e:
            return(e.args)
        except ValueError:
            print("'" + url + "' is not a valid URL")


def compatability_check(debug=False):

    import glob
    import warnings
    import subprocess
    import site

    if sys.platform == "darwin":
        versions = glob.glob("/Applications/ParaView*")
        versions.sort()
        version = versions[-1]
        if len(version) == 0:
            print("ParaView not found in /Applications directory." \
                " To install ParaView, see https://www.paraview.org/download/.")
            # TODO?: Allow for ParaView not located in /Applications/
            sys.exit(1)
        use = ""
        # versions list will have elements of, e.g.,
        # ["/Applications/ParaView-5.7.0.app", "/Applications/ParaView-5.8.0.app"].
        for version in versions:
            if debug:
                print("Found " + version)
            version_str = version \
                            .replace("/Applications/ParaView-", "") \
                            .replace(".app", "")
            version_num = [int(i) for i in version_str.split(".")]
            # version_num will be tuple of (major, minor, patch)
            if list(sys.version_info[0:2]) > [2, 7] and version_num <= [5, 8]:
                if debug:
                    print('Python > 2.7 is not compatible with ParaView ' \
                        + version_str + ' on OS-X.')
            elif list(sys.version_info[0:2]) == [2, 7] and version_num[0:2] == [5, 8]:
                if debug:
                    print('A bug in ParaView 5.8 for OS-X prevents magnetovis from working. ' \
                        + 'See https://gitlab.kitware.com/paraview/paraview/-/issues/20146')
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
            PARAVIEW = subprocess.check_output(['which','paraview'])
        except:
            print("Executable named 'paraview' was not found in path. " \
                " Install ParaView such that 'which paraview' returns location of paraview.")
            sys.exit(1)
        try:
            PVPYTHON = subprocess.check_output(['which','pvpython'])
        except:
            print("Executable named 'pvpython' was not found in path. " \
                " Install ParaView such that 'which pvpython' returns location of pvpython.")
            sys.exit(1)
    else:
        print("Installation implemented only for Linux and OS-X.")
        sys.exit(0)

    util_path = os.path.dirname(os.path.realpath(__file__))
    ver_path = os.path.join(util_path,'..','etc','version.py')
    if debug:
        print("Executing %s %s" % (PVPYTHON, ver_path))
    try:
            pvpython_version_str = subprocess.check_output([PVPYTHON, ver_path])
    except:
        print("Could not execute " + PVPYTHON + " " + ver_path + ". Exiting.")
        sys.exit(1)

    ver = sys.version_info
    python_version_str = str(ver.major) + "." + str(ver.minor) + "." + str(ver.micro)

    pvpython_version_str = pvpython_version_str.decode().strip()
    pvpython_version_lst = [int(i) for i in pvpython_version_str.split(".")]

    if pvpython_version_lst[0:2] == [2, 7] and sys.version_info[0:2] != (2, 7):
        print('Installed ParaView uses Python 2.7 and so magnetovis requires Python 2.7. Exiting.')
        print("pvpython Python version           = " + pvpython_version_str)
        print("Python version executing setup.py = " + python_version_str)
        #sys.exit(1)

    if sys.version_info[0:2] != pvpython_version_lst[0:2]:
        # Hack to prevent warning from including unneeded information.
        def _warning(message, category=UserWarning, filename='', lineno=-1, file=None, line=''):
            print("UserWarning: " + str(message))
        warnings.showwarning = _warning

        warnings.warn("Installed ParaView uses Python " + pvpython_version_str \
                    + " and magnetovis is being installed for Python " \
                    + python_version_str \
                    + ". There may be compatability issues if you use " \
                    + "libraries and code used are not compatable with Python " \
                    + pvpython_version_str + ".")

    return PARAVIEW
