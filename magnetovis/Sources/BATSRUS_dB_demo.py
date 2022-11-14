import paraview.simple as pvs
import magnetovis as mvs

# Demo 1
rBody = 1.5     # Inner simulation boundary
rCurrents = 1.8 # FACs are mapped to ionosphere starting at rCurrents
# Anything below rCurrents is not included in dB calc by BATSRUS.

innerRadius = rCurrents-0.001
outerRadius = 300

single = True  # Run first vtkfile
test   = False # Use artificial j instead of j in file
time   = '2001-09-02T04:10:00' # Should be 2019; TODO: Get from filename.

import glob
#vtkfiles = glob.glob('/Volumes/My Passport for Mac/git-data/sblake/DIPTSUR2/GM/IO2/3d*.vtk')

# https://github.com/spacecataz/swmf_runfiles/blob/main/divB_test/ideal_btest/PARAM.in_init#L106
#rBody = 2.5
#rCurrents = 3.0
#vtkfiles = glob.glob('/Volumes/My Passport for Mac/git-data/dwelling/divB_simple1/GM/3d__*.vtk')

# https://ccmc.gsfc.nasa.gov/results/viewrun.php?domain=GM&runnumber=Brian_Curtis_042213_7
#vtkfiles = glob.glob('/Volumes/WDMyPassport5GB-1/git-data/Curtis/data/Brian_Curtis_042213_2/GM_CDF/3d__*.vtk')
#vtkfiles = ["/tmp/3d__var_1_e20120723-120000-000.out.cdf.vtk"]
vtkfiles = ["/Volumes/My Passport for Mac/git-data/dwelling/divB_simple1/GM/3d__mhd_4_e20100320-000000-000.vtk"]

if test:
    j = 'js' # Use a artificial j for Biot-Savart calculations
else:
    j = 'j'

if False:
    time = '2001-09-02T04:10:00' # Should be 2019
    pos = (1., 18.907, 72.815)   # Geographic r, lat, long of Colaba
    from hxform import hxform as hx
    pos_gsm = hx.transform(pos, time, 'GEO', 'GSM', ctype_in="sph", ctype_out="car", lib='cxform')
    print(pos_gsm)
    n_geo = hx.transform([0, 0, 1], time, 'GEO', 'GSM', ctype_in="car", ctype_out="car", lib='cxform')
    print(n_geo)
    # (0.711553841455819, -0.6707300139270566, 0.20931406815328438)

def nez(time, pos, csys):
  """Unit vectors in geographic north, east, and zenith dirs"""

  import numpy as np
  from hxform import hxform as hx

  # z axis in geographic
  Z = hx.transform(np.array([0, 0, 1]), time, 'GEO', csys, lib='cxform')

  pos = np.array(pos)

  # zenith direction ("up")
  z_geo = pos/np.linalg.norm(pos)

  e_geo = np.cross(z_geo, Z)
  e_geo = e_geo/np.linalg.norm(e_geo)

  n_geo = np.cross(e_geo, z_geo)
  n_geo = n_geo/np.linalg.norm(n_geo)

  return n_geo, e_geo, z_geo


# Point to compute ΔB
if False:
    from hxform import hxform as hx
    pos = (1., 18.907, 72.815)   # Geographic r, lat, long of Colaba
    #(X,Y,Z) = hx.transform(pos, time, 'GEO', 'GSM', ctype_in="sph", ctype_out="car", lib='cxform')
    #(X, Y, Z) = (0.711553841455819, -0.6707300139270566, 0.20931406815328438)    
else:
    (X, Y, Z) = (1, 0, 0)
    #(X, Y, Z) = (0.01, 0, 0)


RGBPointsPositive = [
                        0, 0.85, 0.85, 0.85,
                        1, 0.71, 0.02, 0.15
                   ]
RGBPointsNegative = [
                        0, 0.85, 0.85, 0.85,
                        1, 0.15, 0.02, 0.71
                    ]

def SetColorBar(color_by, title, source, UseLogScale=True, Position=None, WindowLocation="Lower Right Corner", RGBPoints=None):

    ckwargs =  {
        'scalarBar': {
                        'Title': title,
                        'ComponentTitle': '',
                        'HorizontalTitle': 1,
                        'TitleJustification': 'Left',
                        'ScalarBarLength': 0.35
                    },
        'colorTransferFunction': {
                                    "UseLogScale": UseLogScale,
                                    "separate": True
                                }
    }

    if RGBPoints is not None:
        ckwargs['colorTransferFunction']['RGBPoints'] = RGBPoints

    if Position is not None:
        ckwargs['scalarBar']['Position'] = Position
        ckwargs['scalarBar']['WindowLocation'] = 'Any Location'
    else:
        ckwargs['scalarBar']['WindowLocation'] = WindowLocation

    mvs.SetColoring(color_by, source=source, **ckwargs)


def RenderScene(vtkfile, DateTime=""):

    # Geographic north, east and zenith unit vectors 
    n_geo, e_geo, z_geo = nez(DateTime, (X,Y,Z), "GSM")

    #print(n_geo)
    n_geo = [0, 0, 1]
    s = pvs.Sphere(registrationName="ΔB point", Radius=0.2, Center=(X,Y,Z))
    pvs.Show(s)


    mvs.Earth(time=DateTime, coord_sys="GSM")

    batsrus = mvs.BATSRUS(file=vtkfile, setPresentationProperties=False)
    # Add radial distance of cell center for use by threshold filter
    registrationName = "Append CellCenter_R"
    calculator1 = pvs.Calculator(registrationName=registrationName, Input=batsrus)
    calculator1.AttributeType = 'Cell Data'
    calculator1.Function = "(CellCenter_X^2 + CellCenter_Y^2 + CellCenter_Z^2)^0.5"
    calculator1.ResultArrayName = "CellCenter_R"

    # Create a simulated j that is 1 µA/m^2 in ϕ hat direction.
    registrationName = 'Append js'
    calculator2 = pvs.Calculator(registrationName=registrationName, Input=calculator1)
    calculator2.AttributeType = 'Cell Data'
    calculator2.Function = f"-iHat*CellCenter_Y/CellCenter_R + jHat*CellCenter_X/CellCenter_R + kHat*(j_Z*0.0)" 
    calculator2.ResultArrayName = 'js'

    # Add j_phi
    registrationName = 'Append j_phi'
    calculator3 = pvs.Calculator(registrationName=registrationName, Input=calculator2)
    calculator3.AttributeType = 'Cell Data'
    calculator3.Function = f"-{j}_X*CellCenter_Y/CellCenter_R + {j}_Y*CellCenter_X/CellCenter_R" 
    calculator3.ResultArrayName = 'j_phi'

    threshold1 = pvs.Threshold(registrationName=f"Cells w/ CellCenter_R > rCurrents = {rCurrents}", Input=calculator3)
    threshold1.Scalars = ['CELLS', 'CellCenter_R']
    threshold1.LowerThreshold = innerRadius
    threshold1.UpperThreshold = outerRadius

    if True:

        # Biot-Savart formula (Jackson 5.14)
        # dB = dV*(µ_o/4π)(J x (r-r'))/|r-r'|^3
        # r is cell center
        # r' is vector from origin to dV

        # [B] = [µ_o][j][V^3]/[r^2]
        #  j has units of µA/m^2.
        #  r has units of R_E = 6371 km (TODO: check that this is value used in simulation)
        #  Volume has units of R_E^3

        # [B] = [µ_o][j][r]

        # Given that µ_o = 4π*1e-7 [N/A^2], B in [T] is
        # B = (µ_o/4π in N/A^2)*(j in µA/m^2 * (1e-6 A/µA))*(r in R_E * 6.371e6 m/1 R_E)
        #   = 6.731e-7 (j in µA/m^2)*(r in R_E)
        # => conversion of j and r to SI so B in [T] is the same as multiplying by 6.731e-7
        # To convert this to [nT], divide by 1e-9 giving a scale factor of 673.1.

        Denominator  = f"((({X}-CellCenter_X)^2+({Y}-CellCenter_Y)^2+({Z}-CellCenter_Z)^2)^(3/2))"
        BiotSavart_X = f"iHat*CellVolume*( {j}_Y*({Z}-CellCenter_Z) - {j}_Z*({Y}-CellCenter_Y) )"
        BiotSavart_Y = f"jHat*CellVolume*( {j}_Z*({X}-CellCenter_X) - {j}_X*({Z}-CellCenter_Z) )"
        BiotSavart_Z = f"kHat*CellVolume*( {j}_X*({Y}-CellCenter_Y) - {j}_Y*({X}-CellCenter_X) )"

        registrationName = 'dB'
        dB = pvs.Calculator(registrationName=registrationName, Input=threshold1)
        dB.AttributeType = 'Cell Data'
        dB.Function = "673.1*(" + BiotSavart_X + " + " + BiotSavart_Y + " + " + BiotSavart_Z + ")/" + Denominator 
        dB.ResultArrayName = registrationName
        #SetColorBar(('CELLS', registrationName), r'Δ$\mathbf{B}$ [nT]', dB)

        import paraview
        import numpy as np
        from vtk.util import numpy_support

        #source = pvs.GetActiveSource()
        #print(source)
        sourceData = paraview.servermanager.Fetch(dB)
        dB_vtk = sourceData.GetCellData().GetArray('dB')
        dB_numpy = numpy_support.vtk_to_numpy(dB_vtk)
        dB_N_Total = np.dot(np.sum(dB_numpy, axis=0), n_geo)
        print(dB_N_Total)
        dB_N_Totali = int(dB_N_Total)
        mvs.SetTitle(DateTime + f'   $\Delta B_N = {dB_N_Totali:d}$ [nT]', display={'WindowLocation': 'Any Location', 'Position': [0.01, 0.93]})
        dB_N_Total = np.abs(dB_N_Total)

        # Smallest volume is 1/4096.
        # TODO: Get from file.
        # Normalize by total field and cell volume size. One must
        # interpret large volumes with a constant color as being
        # composed of subvolumes with the same dB contribution.)
        minCellVolume = 1/4096
        Normalization = f"{dB_N_Total}*{minCellVolume}/CellVolume"

        if True:

            # Signed dB in northward direction. Calculator appends dB_Ns to dB
            registrationName = 'dB_N'
            dB_N = pvs.Calculator(registrationName=registrationName, Input=dB)
            dB_N.AttributeType = 'Cell Data'
            dB_N.Function = f"dot(dB, iHat*{n_geo[0]}+jHat*{n_geo[1]}+kHat*{n_geo[2]})/{Normalization}"
            dB_N.ResultArrayName = registrationName

            # Remove zeros that occur when dB_N = 0. This modifies dB_N!
            dB_Nt = pvs.Threshold(registrationName="dB_Nt", Input=dB_N)
            dB_Nt.Scalars = ['CELLS', registrationName]
            dB_Nt.LowerThreshold = 1e-16
            dB_Nt.UpperThreshold = 1e8
            #SetColorBar(('CELLS', 'dB_Ns'), 'Δ$B_N$', dB_N)

            sliceXY = pvs.Slice(registrationName="dB_N y=0 slice", Input=dB_Nt)
            sliceXY.SliceType = 'Plane'
            sliceXY.SliceType.Normal = [0.0, 1.0, 0.0]
            sliceXY.Triangulatetheslice = 0
            pvs.Hide3DWidgets(proxy=sliceXY.SliceType)
            # dB_Nt is not a data array. So we must color by dB_N, which was had the threshold applied.
            SetColorBar(('CELLS', 'dB_N'), '$\delta B_N/\|\Delta B_N\|$', sliceXY, WindowLocation='Upper Right Corner', RGBPoints=RGBPointsPositive)

            renderView1 = pvs.GetActiveView()
            sliceXYDisplay = pvs.GetDisplayProperties(sliceXY, view=renderView1)
            sliceXYDisplayTF = pvs.GetColorTransferFunction('dB_N', sliceXYDisplay, separate=True)
            sliceXYDisplayTF.RescaleTransferFunction(1e-11, 1e-04)
            sliceXYDisplayTF = pvs.GetOpacityTransferFunction('dB_N', sliceXYDisplay, separate=True)
            sliceXYDisplayTF.RescaleTransferFunction(1e-11, 1e-04)

            range = sliceXY.CellData.GetArray('dB_N').GetRange()
            with open('BATSRUS_dB_demo/dB_N.txt', 'a') as f:
                f.write("{}, {}".format(*range))

        if True:

            # Signed dB in northward direction. Calculator appends dB_Ns to dB
            registrationName = 'dB_S'
            dB_S = pvs.Calculator(registrationName=registrationName, Input=dB)
            dB_S.AttributeType = 'Cell Data'
            dB_S.Function = f"-dot(dB, iHat*{n_geo[0]}+jHat*{n_geo[1]}+kHat*{n_geo[2]})/{Normalization}"
            dB_S.ResultArrayName = registrationName

            # Remove zeros that occur when dB_S = 0. This modifies dB_S!
            dB_St = pvs.Threshold(registrationName="dB_St", Input=dB_S)
            dB_St.Scalars = ['CELLS', registrationName]
            dB_St.LowerThreshold = 1e-16
            dB_St.UpperThreshold = 1e8
            #SetColorBar(('CELLS', 'dB_Ns'), 'Δ$B_N$', dB_N)

            sliceXY = pvs.Slice(registrationName="dB_S y=0 slice", Input=dB_St)
            sliceXY.SliceType = 'Plane'
            sliceXY.SliceType.Normal = [0.0, 1.0, 0.0]
            sliceXY.Triangulatetheslice = 0
            pvs.Hide3DWidgets(proxy=sliceXY.SliceType)
            SetColorBar(('CELLS', 'dB_S'), '$\delta B_S/\|\Delta B_N\|$', sliceXY, WindowLocation='Lower Right Corner', RGBPoints=RGBPointsNegative)

            renderView1 = pvs.GetActiveView()
            sliceXYDisplay = pvs.GetDisplayProperties(sliceXY, view=renderView1)
            sliceXYDisplayTF = pvs.GetColorTransferFunction('dB_S', sliceXYDisplay, separate=True)
            sliceXYDisplayTF.RescaleTransferFunction(1e-11, 1e-04)
            sliceXYDisplayTF = pvs.GetOpacityTransferFunction('dB_S', sliceXYDisplay, separate=True)
            sliceXYDisplayTF.RescaleTransferFunction(1e-11, 1e-04)

            range = sliceXY.CellData.GetArray('dB_S').GetRange()
            with open('BATSRUS_dB_demo/dB_S.txt', 'a') as f:
                f.write("{}, {}".format(*range))

            if True:
                sliceXZ = pvs.Slice(registrationName="dB_N z=0 slice", Input=dB_Nt)
                sliceXZ.SliceType = 'Plane'
                sliceXZ.SliceType.Normal = [0.0, 0.0, 1.0]
                sliceXZ.Triangulatetheslice = 0
                pvs.Hide3DWidgets(proxy=sliceXZ.SliceType)
                SetColorBar(('CELLS', 'dB_N'), '$\delta B_N/\|\Delta B_N\|$', sliceXZ, WindowLocation="Upper Right Corner", RGBPoints=RGBPointsPositive)

                renderView1 = pvs.GetActiveView()
                sliceXZDisplay_dB_N = pvs.GetDisplayProperties(sliceXZ, view=renderView1)
                sliceXZDisplayTF = pvs.GetColorTransferFunction('dB_N', sliceXZDisplay_dB_N, separate=True)
                sliceXZDisplayTF.RescaleTransferFunction(1e-11, 1e-04)
                sliceXZDisplayTF = pvs.GetOpacityTransferFunction('dB_N', sliceXZDisplay_dB_N, separate=True)
                sliceXZDisplayTF.RescaleTransferFunction(1e-11, 1e-04)
                sliceXZDisplay_dB_N.SetScalarBarVisibility(renderView1, False)

                range = sliceXZ.CellData.GetArray('dB_N').GetRange()
                with open('BATSRUS_dB_demo/dB_N.txt', 'a') as f:
                    f.write("{}, {}".format(*range))

            if True:
                sliceXZ = pvs.Slice(registrationName="dB_S z=0 slice", Input=dB_St)
                sliceXZ.SliceType = 'Plane'
                sliceXZ.SliceType.Normal = [0.0, 0.0, 1.0]
                sliceXZ.Triangulatetheslice = 0
                pvs.Hide3DWidgets(proxy=sliceXZ.SliceType)
                SetColorBar(('CELLS', 'dB_S'), '$\delta B_S/\|\Delta B_N\|$', sliceXZ, WindowLocation="Lower Left Corner", RGBPoints=RGBPointsNegative)

                renderView1 = pvs.GetActiveView()
                sliceXZDisplay = pvs.GetDisplayProperties(sliceXZ, view=renderView1)
                sliceXZDisplayTF = pvs.GetColorTransferFunction('dB_S', sliceXZDisplay, separate=True)
                sliceXZDisplayTF.RescaleTransferFunction(1e-11, 1e-04)
                sliceXZDisplayTF = pvs.GetOpacityTransferFunction('dB_S', sliceXZDisplay, separate=True)
                sliceXZDisplayTF.RescaleTransferFunction(1e-11, 1e-04)
                sliceXZDisplay.SetScalarBarVisibility(renderView1, False)

                range = sliceXZ.CellData.GetArray('dB_S').GetRange()
                with open('BATSRUS_dB_demo/dB_S.txt', 'a') as f:
                    f.write("{}, {}".format(*range))

            # find source
            dB_Ny0slice = pvs.FindSource('dB_N z=0 slice')

            # set active source
            pvs.SetActiveSource(dB_Ny0slice)

            # get display properties
            dB_Ny0sliceDisplay = pvs.GetDisplayProperties(dB_Ny0slice, view=renderView1)
            dB_Ny0sliceDisplay.SetScalarBarVisibility(renderView1, False)

            if True:
                # find source
                dB_Nz0slice = pvs.FindSource('dB_N y=0 slice')

                # set active source
                pvs.SetActiveSource(dB_Nz0slice)

                # get display properties
                dB_Nz0sliceDisplay = pvs.GetDisplayProperties(dB_Nz0slice, view=renderView1)

                # get separate color transfer function/color map for 'dB_N'
                separate_dB_Nz0sliceDisplay_dB_NLUT = pvs.GetColorTransferFunction('dB_N', dB_Nz0sliceDisplay, separate=True)

                # get color legend/bar for separate_dB_Nz0sliceDisplay_dB_NLUT in view renderView1
                separate_dB_Nz0sliceDisplay_dB_NLUTColorBar = pvs.GetScalarBar(separate_dB_Nz0sliceDisplay_dB_NLUT, renderView1)

                # Properties modified on separate_dB_Nz0sliceDisplay_dB_NLUTColorBar
                separate_dB_Nz0sliceDisplay_dB_NLUTColorBar.WindowLocation = 'Any Location'
                separate_dB_Nz0sliceDisplay_dB_NLUTColorBar.Position = [0.84, 0.5]

        mvs.SetOrientationAxisLabel(Text='GSM')
        mvs.SetCamera(viewType="isometric")
        view = pvs.GetActiveViewOrCreate('RenderView')
        camera = view.GetActiveCamera() 
        camera.Zoom(1.8)
        view.StillRender()
        
        if True:
            renderView = pvs.GetActiveView()
            ImageResolution = [1080, 960]
            renderView.ViewSize = ImageResolution

            file_png = vtkfile + ".dB.png"
            mvs.logger.info("Writing " + file_png)
            pvs.SaveScreenshot(file_png, renderView, ImageResolution=ImageResolution)
            mvs.logger.info("Wrote " + file_png)

        if True:
            #renderView1 = pvs.GetActiveViewOrCreate('RenderView')

            layout1 = pvs.GetLayout()
            layout1.SplitHorizontal(0, 0.5)
            renderView2 = pvs.CreateView('RenderView')
            pvs.AssignViewToLayout(view=renderView2, layout=layout1, hint=2)

            sliceXY = pvs.Slice(registrationName="j_phi y=0 slice", Input=threshold1)
            sliceXY.SliceType = 'Plane'
            sliceXY.SliceType.Normal = [0.0, 0.0, 1.0]
            sliceXY.Triangulatetheslice = 0
            pvs.Hide3DWidgets(proxy=sliceXY.SliceType)
            SetColorBar(('CELLS', 'j_phi'), '$j_{\phi}$ [µA/m$^2$]', sliceXY, UseLogScale=False, WindowLocation="Lower Right Corner")

            range = sliceXZ.CellData.GetArray('j_phi').GetRange()
            with open('BATSRUS_dB_demo/j_phi.txt', 'a') as f:
                f.write("{}, {}".format(*range))

            sliceXZ = pvs.Slice(registrationName="j_phi z=0 slice", Input=threshold1)
            sliceXZ.SliceType = 'Plane'
            sliceXZ.SliceType.Normal = [0.0, 1.0, 0.0]
            sliceXZ.Triangulatetheslice = 0
            pvs.Hide3DWidgets(proxy=sliceXZ.SliceType)
            SetColorBar(('CELLS', 'j_phi'), '$j_{\phi}$ [µA/m$^2$]', sliceXZ, UseLogScale=False, WindowLocation="Upper Right Corner")

            renderView1 = pvs.GetActiveView()
            sliceXZDisplay = pvs.GetDisplayProperties(sliceXZ, view=renderView1)
            sliceXZDisplay.SetScalarBarVisibility(renderView1, False)

            range = sliceXZ.CellData.GetArray('j_phi').GetRange()
            with open('BATSRUS_dB_demo/j_phi.txt', 'a') as f:
                f.write("{}, {}".format(*range))

            mvs.SetOrientationAxisLabel(Text='GSM')
            mvs.SetCamera(viewType="isometric")
            camera = renderView1.GetActiveCamera() 
            camera.Zoom(1.8)
            view.StillRender()

            if True:
                ImageResolution = [1080, 960]
                renderView1.ViewSize = ImageResolution

                file_png = vtkfile + ".j_phi.png"
                mvs.logger.info("Writing " + file_png)
                pvs.SaveScreenshot(file_png, renderView1, ImageResolution=ImageResolution)
                mvs.logger.info("Wrote " + file_png)


def timestr(filename, date=None):
    import re
    parts = re.search('_e(\d{8})\-(\d{6})\-(\d{3})', filename).groups()
    time = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6] + "." + parts[2]
    if date is None:
        date = parts[0][0:4] + "-" + parts[0][4:6] + "-" + parts[0][6:8]

    return date + "T" + time


import os
if single == True:
    if "DIPTSUR2" in vtkfiles[0]:
        DateTime = timestr(vtkfiles[0], yyyymmdd="1859-09-02T")
    else:
        DateTime = timestr(vtkfiles[0])

    DateTime = DateTime.split(".")[0]
    mvs.ClearPipeline()
    RenderScene(vtkfiles[0], DateTime=DateTime)
else:
    for vtkfile in vtkfiles:
        if os.path.exists(vtkfile + ".dB.png"):
            print("Skipping " + vtkfile)
            continue

        if "DIPTSUR2" in vtkfiles[0]:
            DateTime = timestr(vtkfile, yyyymmdd="1859-09-02T")
        else:
            DateTime = timestr(vtkfile)

        DateTime = DateTime.split(".")[0]
        mvs.ClearPipeline()
        RenderScene(vtkfile, DateTime=DateTime)
