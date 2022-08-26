def t89c(points, ut=100, iopt=1, ps=None):

    import platform
    platform_str = platform.platform()
    if platform_str.endswith('arm64-arm-64bit'):
        try:
            from geopack import geopack
        except:
            msg = 'pip install --pre -i https://pypi.anaconda.org/scipy-wheels-nightly/simple scipy'
            msg = '\n\nThis function uses a library that depends on scipy. On Mac M1, you need to install scipy using: \n\n   ' + msg + '\n'
            raise ImportError(msg)

    import numpy as np

    import magnetovis as mvs
    from geopack import geopack
    from geopack import t89

    if False:
        print(ut)
        print(iopt)
        print(ps)
        #import datetime
        #ut = (datetime.datetime(2001,1,1,2,3,4)-datetime.datetime(1970,1,1)).total_seconds()
        ut = 983420048.0
        ut = 983627464.0
        ps = geopack.recalc(ut)
        print(ps)
        print(f"---{ps}")

    ps = geopack.recalc(ut)
    B = np.zeros(points.shape)
    for i in range(points.shape[0]):
        r = np.linalg.norm(points[i,:])
        if r < 1:
            B[i,0] = np.nan
            B[i,1] = np.nan
            B[i,2] = np.nan
        else:
            #print(geopack.igrf_gsm(*[-5.1,0.3,2.8]))

            b0xgsm,b0ygsm,b0zgsm = geopack.igrf_gsm(points[i,0], points[i,1], points[i,2])
            if False:
                B[i,0] = b0xgsm
                B[i,1] = b0ygsm
                B[i,2] = b0zgsm

            dbxgsm,dbygsm,dbzgsm = t89.t89(iopt, ps, points[i,0], points[i,1], points[i,2])
            B[i,0] = b0xgsm + dbxgsm
            B[i,1] = b0ygsm + dbygsm
            B[i,2] = b0zgsm + dbzgsm

    return B
