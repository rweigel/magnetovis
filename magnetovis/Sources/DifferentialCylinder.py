# When executed using
#   python DifferentialCylinder.py
# info about the points, elements, and their connectivity
# is printed. No object is actually created. This is useful
# for debugging the non-VTK parts of this script.

# This script can be copied into the Programable Source editor
# and executed.

import numpy as np

if 'output' in locals()
  debug = False
  import vtk

if debug == False:
  points = vtk.vtkPoints()

ro = 0
rf = 3
Nr = 3

Nφ = 4
φo = 0
φf = 360

zo = 0
zf = 1
Nz = 1
closed = True

assert Nφ > 0, "Nφ > 0 is required"
assert Nz > 0, "Nz > 0 is required"
assert φf-φo <= 360, "φf-φo < 360 is required"
if φf-φo == 360:
    assert Nφ > 2, "If φf-φo = 360, Nφ > 2 is required"
assert ro >= 0, "r >= 0 is required"
assert φf - φo, "φf - φo <= 0 is required"

dr = (rf-ro)/Nr
dφ = (φf - φo)*(np.pi/180.)/Nφ
dz = (zf-zo)/Nz

i = 0
w = 0
print(" Pt   x     y     z")
for k in range(0, 2*Nz):
    if debug == False:
      points.InsertNextPoint(0, 0, k*dz)
    print("{0:>3} {1:5.2f} {2:5.2f} {3:5.2f}".format(w, 0, 0, k*dz))
    w = w + 1
    for j in range(Nφ):
      for i in range(Nr):
        x = (ro + (i+1)*dr)*np.cos(j*dφ)
        y = (ro + (i+1)*dr)*np.sin(j*dφ)
        print("{0:>3} {1:5.2f} {2:5.2f} {3:5.2f}".format(w, x, y, k*dz))
        if debug == False:
            points.InsertNextPoint(x, y, k*dz)
        w = w + 1

if not closed:
    j = j + 1
    for i in range(Nr):
      x = (ro + (i+1)*dr)*np.cos(j*dφ)
      y = (ro + (i+1)*dr)*np.sin(j*dφ)
      print("{0:>3} {1:5.2f} {2:5.2f} {3:5.2f}".format(w, x, y, k*dz))
      if debug == False:
          points.InsertNextPoint(x, y, k*dz)
      w = w + 1

if debug == False:
  output = self.GetUnstructuredGridOutput()
  #output.Allocate(Nφ*Nz)
  output.Allocate(Nr*Nφ*Nz)

w = 0
for k in range(0, Nz):
  p0 = k*(Nr*Nφ + 1)
  p1 = p0 + 1
  p2 = p1 + Nr
  p3 = (k+1)*(Nr*Nφ + 1)
  p4 = p3 + 1
  p5 = p4 + Nr
  for j in range(0, Nφ-1):
    if debug == False:
      wedge = vtk.vtkWedge()
      wedge.GetPointIds().SetId(0, p0)
      wedge.GetPointIds().SetId(1, p1)
      wedge.GetPointIds().SetId(2, p2)
      wedge.GetPointIds().SetId(3, p3)
      wedge.GetPointIds().SetId(4, p4)
      wedge.GetPointIds().SetId(5, p5)
      output.InsertNextCell(wedge.GetCellType(), wedge.GetPointIds())
    print("Inserted wedge {0:>3}: {1:>3} {2:>3} {3:>3} {4:>3} {5:>3} {6:>3}".format(w, p0, p1, p2, p3, p4, p5))
    p1 = p1 + Nr
    p2 = p2 + Nr
    p4 = p4 + Nr
    p5 = p5 + Nr
    w = w + 1
  if closed:
      p2 = 1 + k*(Nr*Nφ + 1)
      p5 = p2 + (Nr*Nφ + 1)
  if debug == False:
    wedge = vtk.vtkWedge()
    wedge.GetPointIds().SetId(0, p0)
    wedge.GetPointIds().SetId(1, p1)
    wedge.GetPointIds().SetId(2, p2)
    wedge.GetPointIds().SetId(3, p3)
    wedge.GetPointIds().SetId(4, p4)
    wedge.GetPointIds().SetId(5, p5)
    output.InsertNextCell(wedge.GetCellType(), wedge.GetPointIds())
  print("Inserted wedge {0:>3}: {1:>3} {2:>3} {3:>3} {4:>3} {5:>3} {6:>3}".format(w, p0, p1, p2, p3, p4, p5))
  w = w + 1

w = 0
for k in range(0, Nz):
  for j in range(0, Nφ):
    for i in range(0, Nr-1):
      p0 = 1 + i + j*Nr + k*(Nr*Nφ+2)
      p1 = p0 + 1
      p2 = p1 + Nr
      p3 = p2 - 1
      p4 = p1 + Nr*Nφ 
      p5 = p4 + 1
      p6 = p5 + Nr
      p7 = p6 - 1
      print("Inserted hex   {0:>3}: {1:>3} {2:>3} {3:>3} {4:>3} {5:>3} {6:>3} {7:>3} {8:>3}".format(w, p0, p1, p2, p3, p4, p5, p6, p7))
      w = w + 1   

if debug == False:
  output.SetPoints(points)