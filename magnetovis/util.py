import os
import sys

print('\n\n util path: ~/magnetovis/pkg/magnetovis/util.py \n\n')

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# from config import conf

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
