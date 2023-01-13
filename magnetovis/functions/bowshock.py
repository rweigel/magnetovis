def bowshock(model, model_opts=None):

  assert model in ['Fairfield71']

  return Fairfield71()


def Fairfield71():

  # https://vtk.org/doc/nightly/html/classvtkQuadric.html
  # F(x,y,z) = a0*x^2 + a1*y^2 + a2*z^2 + a3*x*y + a4*y*z + a5*x*z + a6*x + a7*y + a8*z + a9

  # Fairfield, 1971; https://doi.org/10.1029/JA076i028p06700
  # 0        =  B*x^2 +    y^2 +           A*x*y +                    D*x +  C*y        + E

  # Table 2, column 1 of Fairfield, 1971
  A =    0.0296
  B =   -0.0381
  C =   -1.280
  D =   45.644
  E = -652.10

  a0 = B
  a1 = 1.
  a2 = 0.
  a3 = A
  a4 = 0.
  a5 = 0.
  a6 = D
  a7 = C
  a8 = 0.
  a9 = E

  # The following is based on https://github.com/dbzhang800/VTKDemoForPyQt
  import vtk
  quadric = vtk.vtkQuadric()
  quadric.SetCoefficients(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9)

  sample = vtk.vtkSampleFunction()
  sample.SetSampleDimensions(5, 5, 0)
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

  # See comment below for explanation for the following step.
  # https://stackoverflow.com/a/22466974
  # The points lie in a plane, so we can sort them by angle
  # to put them in order of closeness to each other.
  angle = np.arctan2(xyz[:,1],xyz[:,0])
  idx = np.argsort(angle)
  xyz = xyz[idx,:]
  return xyz

  if False:
    # The output of the countour filter is a set of lines and if we create
    # a line by simply connecting the points, the line may not be smooth.
    # To see this copy the above code into a Programmable Source, color
    # by the _cell_ array vtkIdFilter_Ids and select "Interpret Values as
    # categories" in the colormap editor.
    idFilter = vtk.vtkIdFilter()
    idFilter.SetInputConnection(contourFilter.GetOutputPort())
    idFilter.Update()

    tubeFilter = vtk.vtkTubeFilter()
    tubeFilter.SetInputConnection(idFilter.GetOutputPort())
    tubeFilter.Update()

    output.ShallowCopy(tubeFilter.GetOutputDataObject(0))

