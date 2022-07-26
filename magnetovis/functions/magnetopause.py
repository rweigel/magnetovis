def magnetopause(model, model_params=None, return_x_max=False):


def Fairfield71(return_x_max=False):

    # Fairfield, 1971; https://doi.org/10.1029/JA076i028p06700
    # 0 = y^2 + A*x*y + B*x^2 + C*y + D*x + E

    # Table 2, column 4 of Fairfield, 1971
    A =   -0.0942
    B =   -0.3818
    C =   -0.498
    D =   17.992
    E = -240.12

    # Caution: Duplicate code exists in bowshock.py/Fairfield71().

    import vtk
    quadric = vtk.vtkQuadric()
    quadric.SetCoefficients(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9)

    sample = vtk.vtkSampleFunction()
    sample.SetSampleDimensions(100, 100, 0)
    sample.SetImplicitFunction(quadric)
    sample.SetModelBounds(-45, 20, -60, 60, 0, 0)
    sample.Update()

    # https://vtk.org/doc/nightly/html/classvtkContourFilter.html
    contourFilter = vtk.vtkContourFilter()
    # 1 contour level with contours levels starting at 0 and ending at 0
    contourFilter.GenerateValues(1,0,0) 
    contourFilter.SetInputConnection(sample.GetOutputPort())
    contourFilter.Update()

    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa
    pdow = dsa.WrapDataObject(contourFilter.GetOutputDataObject(0))

    xyz = pdow.GetPoints()

    return xyz

    def Roelof_Sibeck93(Bz, Psw, return_x_max=False):

        """
        Roelof and Sibeck, 1993; https://doi.org/10.1029/93JA02362

        r**2 * s1 * X**2 + s2 * X + s3 = 0

        where

        r**2 = Y**2 + Z**2

        s1 =  exp(a00 + a10 * x + a01 * y + a20 * x**2 + a11 * x * y + a02 * y**2)
        s2 =  exp(b00 + b10 * x + b01 * y + b20 * x**2 + b11 * x * y + b02 * y**2)
        s3 = -exp(c00 + c10 * x + c01 * y + c20 * x**2 + c11 * x * y + c02 * y**2)

        x = np.log(Psw/P0)/sigma_lnp
        y = (Bz - Bz0)/sigma_Bz

        a00, a01, a20, a11, ... are constants.


        Parameters:
        ----------
        Bz : float
            Interplanetary magnetic field in nT.

        Psw  : float
            Solar wind dynamic pressure in nPa.

        return_x_max : bool, optional
            When True the function does not create a magnetopause surface. Instead
            it only returns the maximum value of X in GSE coordinates so that the
            bow shock can use it to calculate the appropriate sub solar distance.


        Returns:
        -------
            X, Y, and Z coordinates of the magnetopause in GSE.
        """

        P0 = 2.088 # nPa
        sigma_lnp = 0.6312 # dimensionless
        Bz0 = -0.1635 # nT
        sigma_Bz = 3.489

        a00 = -1.764
        a10 = -0.299
        a01 = -0.151
        a20 = -0.246
        a11 = 0.050
        a02 = 0.476

        b00 = 2.934
        b10 = -0.076
        b01 = -0.129
        b20 = -0.012
        b11 = 0.079
        b02 = 0.0026

        c00 = 5.397
        c10 = -0.183
        c01 = -0.041
        c20 = -0.044
        c11 = 0.040
        c02 = 0.020

        x = np.log(float(Psw)/P0)/sigma_lnp
        y = (Bz - Bz0)/sigma_Bz

        lnA = a00 + a10 * x + a01 * y + a20 * x**2 + a11 * x * y + a02 * y**2
        lnB = b00 + b10 * x + b01 * y + b20 * x**2 + b11 * x * y + b02 * y**2
        ln_negC = c00 + c10 * x + c01 * y + c20 * x**2 + c11 * x * y + c02 * y**2

        s1 = np.exp(lnA)
        s2 = np.exp(lnB)
        s3 = - np.exp(ln_negC)

        sqrt_descriminate = np.sqrt(s2**2 - 4 * (-s1) * (-s3))
        x_max = (s2 - sqrt_descriminate)/ (-2 * s1)
        x_min = (s2 + sqrt_descriminate)/ (-2 * s1)
        if x_min < -40:
            x_min = -40

        if return_x_max:
            return x_max

        X = [[x_max]]
        all_x_values = np.flipud(np.linspace(x_min, x_max, 50))

        for x in all_x_values:
            X = np.pad(X, ((1, 1), (1, 1)), 'constant', constant_values=((x, x), (x, x)))
        X = X.flatten()

        r = -s1 * X **2 - s2 * X - s3
        r[r<0] = 0
        r = np.sqrt(r)

        m = np.linspace(1,-1,2*len(all_x_values)+1,endpoint=True)
        u = np.matlib.repmat(m,1,len(m)).flatten()
        v = np.repeat(m,len(m))
        phi = np.arctan2(v,u)

        Y = r * np.cos(phi)
        Z = r * np.sin(phi)
        points = np.column_stack([X, Y, Z])

        return points


    def Sibeck_Lopez_Roelof1991(Bz=None, Psw=None, return_x_max=False):

        """
        The magnetopause model from Sibeck, Lopez, and Roelof 1991 paper.
        DOI: https://doi.org/10.1029/93JA02362

        r**2 * s1 * X**2 + s2 * X + s3 = 0

        where
        r**2 = Y**2 + Z**2
        s1 = 0.14
        s2 = 18.2
        s3 = -217.2
        p0 = 2.04  #
        rho =  (p0/Psw)**(1/6) #

        Parameters:
        ----------
        Bz_or_Psw : float
            The parameter has the option of being the interplanetary magnetic field
            Bz in nT or the dynamic solar wind pressure Psw in nPa. The choice is
            made by the second parameter "option".

        option : string, optional
            This has two possible values "Bz" or "Psw" which specifies how Bz_or_Psw
            should be interpreted as. The default is "Bz".

        return_x_max : bool, optional
            When True the function does not create a magnetopause surface. Instead
            it only returns the maximum value of X in GSE coordinates so that the
            bow shock can use it to calculate the appropriate sub solar distance.

        Returns:
        -------
        3 numpy array's

            Creates 3 numpy array's of the X, Y, and Z coordinates of the
            magnetopause according to the Siebeck, Lopez and Roelof 1991 model
            based on the solar wind dynamic pressure or interplanetary magnetic
            field in GSE coordinates.

        """
        if Psw != None:
            s1, s2, s3 = 0.14, 18.2, -217.2
            p_0 = 2.04
            rho = (p_0 / Psw) ** (1./6)
        elif Bz != None:
            rho = 1
            if Bz <= -4:
                s1, s2, s3 = 0.12, 19.9, -200.6
                if Bz < -6:
                    print('WARNING Bz={}nT which is out of range of valid values'+
                          'for Sibeck Lopez Roelof 91 magnetopause model. \n'+
                          'valid values are [-6,6] \n'+
                          'Using values for Bz in [-6,-4] bin.'.format(Bz))
            elif Bz <= -2:
                s1, s2, s3 = 0.22, 18.2, -213.4
            elif Bz <= 0:
                s1, s2, s3 = 0.11, 17.9, -212.8
            elif Bz <= 2:
                s1, s2, s3 = 0.2, 17.1, -211.5
            elif Bz <= 4:
                s1, s2, s3 = 0.09, 15.7, -198.3
            else:
                s1, s2, s3 = 0.13, 13.1, -179.2
                if Bz > 6:
                    print('WARNING Bz={}nT which is out of range of valid values'+
                          'for Sibeck Lopez Roelof 91 magnetopause model. \n'+
                          'valid values are [-6,6] \n'+
                          'Using values for Bz in [4,6] bin.'.format(Bz))

        sqrt_descriminate = np.sqrt((s2*rho)**2 - 4 * (s1) * (s3) * rho**2)
        x_max = (-s2*rho + sqrt_descriminate)/ (2 * s1)
        x_min = (-s2*rho - sqrt_descriminate)/ (2 * s1)
        if x_min < -40:
            x_min = -40

        if return_x_max:
            return x_max

        X = [[x_max]]
        all_x_values = np.flipud(np.linspace(x_min,x_max,50))

        for x in all_x_values:
            X = np.pad(X,((1,1),(1,1)),'constant',constant_values=((x,x),(x,x)))
        X = X.flatten()

        r = -s1 * X **2 - s2 * rho * X - s3 * rho ** 2
        r[r<0] = 0
        r = np.sqrt(r)

        m = np.linspace(1,-1,2*len(all_x_values)+1,endpoint=True)
        u = np.matlib.repmat(m,1,len(m)).flatten()
        v = np.repeat(m,len(m))
        phi = np.arctan2(v,u)

        Y = r * np.cos(phi)
        Z = r * np.sin(phi)

        points = np.column_stack([X, Y, Z])
        return points


    def Shue97(Bz, Psw, return_x_max=False):
        """
        Magntopause positions from Shue et al. 1997.
        [https://doi.org/10.1029/98JA01103]

        The magnetopause distance from Earth's center from Shue et al. 1997
        is

        r = r_0*(2/(1+cos(theta)))**alpha

        where

        r:      distance to the magnetopause surface in GSM coordinates
        r_0:    depends on the interplanetary magnetic field Bz and the solar wind
                dynamic pressure Psw units in RE
        theta:  the angle between positive x-axis in GSM coordinates and the
                r vector
        alpha:  depends on the interplanetary magnetic field Bz and the solar wind
                dynamic pressure Psw units in RE

        Parameters:
        -----------
        Bz: float
                Interplanetary magnetic field in nT
        Psw: float
                Solar wind dynamic pressure in nPa

        Returns:
        -------
        XYZ: 
        """

        import numpy as np
        import numpy.matlib

        if Bz >= 0:
            # Eqn 12 of Shue et al. 1997
            r_0 = 11.4 + 0.013*Bz * (Psw**(-1/6.6))       
        else:
            # Eqn 13 of Shue et al. 1997
            r_0 = 11.4 + 0.14*Bz * (Psw**(-1/6.6))        
    
        # Eqn 14 of Shue et al. 1997
        alpha = (0.58 - 0.010 * Bz) * (1 + 0.010 * Psw)  

        if return_x_max:
            return r_0 * (2./(1+np.cos(0)))**alpha

        stopping_constant = 40/(2**alpha * r_0)
        theta_finder_array = np.arange(np.pi/2, np.pi, 0.01)
        for theta in theta_finder_array:
            stopping_value = np.cos(theta)/((1 + np.cos(theta))**alpha)
            if abs(stopping_value) < stopping_constant:
                last_theta = theta
            else:
                break

        last_theta = np.rad2deg(last_theta)
        theta_array = [[0]]
        all_theta_values = np.flipud(np.linspace(last_theta, 0, 50))
        for theta in all_theta_values:
            theta_array = np.pad(theta_array,((1, 1), (1, 1)), 'constant',
                                 constant_values=((theta, theta), (theta, theta)))
        theta_array = theta_array.flatten()
        m = np.linspace(1, -1, 2*len(all_theta_values) + 1,endpoint=True)
        u = np.matlib.repmat(m, 1, len(m)).flatten()
        v = np.repeat(m, len(m))
        phi_array = np.arctan2(v, u)
        theta_array = np.radians(theta_array)

        r_array = r_0*( (2/(1+np.cos(theta_array)))**alpha)

        X = r_array * np.cos(theta_array)
        Y = r_array * np.sin(theta_array) * np.sin(phi_array)
        Z = r_array * np.sin(theta_array) * np.cos(phi_array)
        points = np.column_stack([X, Y, Z])

        return points
