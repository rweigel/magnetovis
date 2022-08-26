# import magnetovis; exec(magnetovis.demo("Plasmasphere"))

# import magnetovis as mvs; mvs.ClearPipeline(); exec(open("/Users/weigel/git/magnetovis/untitled.py", encoding="utf-8").read())

# Demo 1
from urllib.request import urlretrieve
url = 'http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000.vtk'
vtkfile = "/tmp/" + url.split("/")[-1]

import os
if not os.path.exists(vtkfile):
  print("Downloading " + url)
  urlretrieve(url, vtkfile)

import magnetovis as mvs
batsrus = mvs.BATSRUS(file=vtkfile, setPresentationProperties=False)
mvs.SetTitle()

import paraview.simple as pvs
pvs.Hide(batsrus)

rBody = 1.5
rCurrents = 1.8 # Not used

# Add radial distance of cell center for use by threshold filter
registrationName = "Add CellCenter_R"
calculator = pvs.Calculator(registrationName=registrationName, Input=batsrus)
calculator.AttributeType = 'Cell Data'
calculator.Function = "(CellCenter_X^2 + CellCenter_Y^2 + CellCenter_Z^2)^0.5"
calculator.ResultArrayName = "CellCenter_R"


threshold1 = pvs.Threshold(registrationName=f"Cells w/ CellCenter_R > rBody = {rBody}", Input=calculator)
threshold1.Scalars = ['CELLS', 'CellCenter_R']
threshold1.LowerThreshold = rBody
threshold1.UpperThreshold = 1e9

def SetColorBar(color_by, name, source, UseLogScale=1):

    ckwargs =  {
        'scalarBar': {
                        'Title': r"$" + name.replace("|","\|") + "$ [nT]",
                        'ComponentTitle': '',
                        'HorizontalTitle': 1,
                        'TitleJustification': 'Left',
                        'Visibility': 1,
                        'ScalarBarLength': 0.8
                    },
        'colorTransferFunction': {
                                    "separate": True,
                                    "UseLogScale": False
                                }
    }
    mvs.SetColoring(color_by, source=source, **ckwargs)

#view = pvs.GetActiveViewOrCreate('RenderView')
#calculatorDisplay = pvs.Show(calculator, view, 'GeometryRepresentation')

# Biot-Savart formula
# dB = dV*(µ_o/4π)(J x (r-r'))/|r-r'|^5
# r is cell center
# r' is vector from origin to dV

# [B] = [µ_o][j][V^3]/[r^3]
#  j has units of µA/m^2.
#  r has units of R_E = 6371 km (check that this is value used in simulation)
#  Volume has units of R_E^3

# Units for [V^3] and [r^3] cancel leaving
# [B] = [µ_o][j]

# If [j] is in µA/m^2, the result of
# B = µ_o*[j in µA/m^2] has units of µT

# Given that µ_o = 4π*1e-7 [N/A^2],
# [B] = [µ_o/4π in MKS][j in µA/m^2] = 1e-7*1e-6 [T] = 1e-13 [T]
# Multiplying by a factor of 10,000 puts the result in nT.

# Point to compute ΔB
(X,Y,Z) = (1.0, 0.0, 0.0)
s = pvs.Sphere(registrationName="ΔB point", Radius=0.1, Center=(X,Y,Z))

bs_E = f"10000*CellVolume*( j_Z*({X}-CellCenter_X) - j_X*({Z}-CellCenter_Z) )"
bs_E = bs_E + f"/(({X}-CellCenter_X)^2+({Y}-CellCenter_Y)^2+({Z}-CellCenter_Z)^2)^(5/2)"

registrationName = 'ΔB_E'
dB_E = pvs.Calculator(registrationName=registrationName, Input=threshold1)
dB_E.AttributeType = 'Cell Data'
dB_E.Function = bs_E
dB_E.ResultArrayName = 'ΔB_E'
SetColorBar(('CELLS', 'ΔB_E'), 'ΔB_E', dB_E, UseLogScale=False)

if False:
    dB_E_p = pvs.Threshold(registrationName=registrationName + " > 0", Input=dB_E)
    dB_E_p.Scalars = ['CELLS', registrationName]
    dB_E_p.LowerThreshold = 1e-16
    dB_E_p.UpperThreshold = 1e8
    SetColorBar(('CELLS', 'ΔB_E'), 'ΔB_E > 0', dB_E_p)

if False:

    sliceXZ = pvs.Slice(registrationName="y=0 slice", Input=dB_E_p)
    sliceXZ.SliceType = 'Plane'
    sliceXZ.SliceType.Normal = [0.0, 1.0, 0.0]
    sliceXZ.Triangulatetheslice = 0
    pvs.Hide3DWidgets(proxy=sliceXZ.SliceType)
    SetColorBar(('CELLS', 'ΔB_E'), 'ΔB_E > 0', sliceXZ)

    sliceXY = pvs.Slice(registrationName="z=0 slice", Input=dB_E_p)
    sliceXY.SliceType = 'Plane'
    sliceXY.SliceType.Normal = [0.0, 0.0, 1.0]
    sliceXY.Triangulatetheslice = 0
    pvs.Hide3DWidgets(proxy=sliceXY.SliceType)
    SetColorBar(('CELLS', 'ΔB_E'), 'ΔB_E > 0', sliceXY)

    # Need to do extra calc. in order to use log scale colorbar
    registrationName = 'ΔB_W'
    dB_W = pvs.Calculator(registrationName=registrationName, Input=threshold1)
    dB_W.AttributeType = 'Cell Data'
    dB_W.Function = "-" + bs_E
    dB_W.ResultArrayName = registrationName
    SetColorBar(('CELLS', 'ΔB_W'), 'ΔB_W', dB_W, UseLogScale=0)

    dB_W_p = pvs.Threshold(registrationName=registrationName + " > 0", Input=dB_W)
    dB_W_p.Scalars = ['CELLS', registrationName]
    dB_W_p.LowerThreshold = 1e-16
    dB_W_p.UpperThreshold = 1e8
    SetColorBar(('CELLS', 'ΔB_W'), 'ΔB_W > 0', dB_W_p)

    sliceXZ = pvs.Slice(registrationName="y=0 slice", Input=dB_W_p)
    sliceXZ.SliceType = 'Plane'
    sliceXZ.SliceType.Normal = [0.0, 1.0, 0.0]
    sliceXZ.Triangulatetheslice = 0
    pvs.Hide3DWidgets(proxy=sliceXZ.SliceType)
    SetColorBar(('CELLS', 'ΔB_W'), 'ΔB_W > 0', sliceXZ)

    sliceXY = pvs.Slice(registrationName="z=0 slice", Input=dB_W_p)
    sliceXY.SliceType = 'Plane'
    sliceXY.SliceType.Normal = [0.0, 0.0, 1.0]
    sliceXY.Triangulatetheslice = 0
    pvs.Hide3DWidgets(proxy=sliceXY.SliceType)
    pvs.Show(sliceXY)
    SetColorBar(('CELLS', 'ΔB_W'), 'ΔB_W > 0', sliceXY)

    renderView1 = pvs.GetActiveViewOrCreate('RenderView')
    sliceXZDisplay = pvs.GetDisplayProperties(sliceXZ, view=renderView1)
    sliceXZDisplay.SetScalarBarVisibility(renderView1, False)
    sliceXYDisplay = pvs.GetDisplayProperties(sliceXY, view=renderView1)
    sliceXYDisplay.SetScalarBarVisibility(renderView1, False)

mvs.SetCamera(viewType="isometric")

