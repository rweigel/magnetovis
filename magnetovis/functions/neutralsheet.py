def neutralsheet(xypoints, time=None, psi=0.0, Rh=8., d=4., G=10., Lw=10.):

    """
    Creates the position of the Current Sheet from model outlined in Tsyganenko 1995
    [https://doi.org/10.1029/94JA03193]

    Defaults parameters are Rh = 8, d = 4, G = 10, Lw = 10 used by
    https://sscweb.gsfc.nasa.gov/users_guide/ssc_reg_doc.shtml

    Z = z1 + z2

    z1 = 0.5 * np.tan(psi)
             * (np.sqrt((X - Rh * np.cos(psi))**2 + (d * np.cos(psi))**2)
             -  np.sqrt((X + Rh * np.cos(psi))**2 + (d * np.cos(psi))**2))

    z2 = -G*np.sin(psi) * Y**4/(Y**4 + Lw**4)

    Parameters:
    ----------
    xypoints:

    psi (float):
        Angle between Earth's dipole moment and z-axis in GSM [degrees]. If not
        None, time is ignored.
    Rh (float):
        "hinging distance"
    G (float):
        Amplitude of the current sheet warping.
    Lw (float):
        Defines the extension in the dawn-dusk direction.

    Returns:
    -------

    points (ndarray):
        Columns of x, y, z


    """
    import numpy as np

    assert ((time is not None) or (psi is not None)), 'functions.neutralsheet(): psi and time cannot both be None.'

    xypoints = np.array(xypoints)

    if isinstance(time, str):
        import magnetovis
        time = magnetovis.util.iso2ints(time)

    if len(xypoints) == 2:
        x = xypoints[0]
        y = xypoints[1]
    else:
        x = xypoints[:, 0]
        y = xypoints[:, 1]

    if psi is None:
        from hxform import hxform as hx
        dipole = hx.MAGtoGSM(np.array([0., 0., 1.]), time, 'car', 'sph')
        # dipole array with [radius, latitude,longitude]
        psi = 90. - dipole[1]
    psi = np.deg2rad(psi)

    z1 = 0.5 * np.tan(psi) \
             * (np.sqrt((x - Rh*np.cos(psi))**2 + (d*np.cos(psi))**2) \
             - np.sqrt((x + Rh*np.cos(psi))**2 + (d*np.cos(psi))**2))
    z2 = -G*np.sin(psi)*y**4/(y**4 + Lw**4)
    z = z1 + z2

    return np.column_stack([x, y, z])


if False:
    import numpy as np

    x = np.linspace(-10, -20, 2)
    y = np.linspace(-2, 2, 2)
    print(x)
    print(neutralsheet(np.column_stack([x, y])))
