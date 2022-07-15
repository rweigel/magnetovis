# Execute using
#   magnetovis BATSRUS_demo.py

'''
# Demo #1
'''
import magnetovis as mvs
batsrus = mvs.BATSRUS(file='/tmp/3d__var_2_e20190902-041000-000.vtk')
mvs.SetTitle("Default file")

'''
# Demo #2
'''
import magnetovis as mvs
file = 'http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000'
mvs.BATSRUS(file=file)
mvs.SetTitle("File passed as URL")

'''
# Demo #3
'''
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.BATSRUS()
mvs.SetTitle("Cells colored by block_id")
import paraview.simple as pvs

'''
# Demo #4
'''
import magnetovis as mvs
batsrus = mvs.BATSRUS(file='/tmp/3d__var_2_e20190902-041000-000.vtk')
mvs.SetTitle("Default file")

import paraview.simple as pvs
cellSize1 = pvs.CellSize(registrationName='  CellSize', Input=batsrus)
pvs.SetActiveSource(cellSize1)
renderView1 = pvs.GetActiveViewOrCreate('RenderView')
cellSize1Display = pvs.Show(cellSize1, renderView1, 'UnstructuredGridRepresentation')
cellSize1Display.Representation = 'Surface With Edges'
cellSize1Display.ColorArrayName = ['CELLS', 'Volume']
pvs.ColorBy(cellSize1Display, ('CELLS', 'Volume'))
cellSize1Display.SetScalarBarVisibility(renderView1, True)
pvs.Hide(batsrus)


'''
# Demo #5
'''
import magnetovis as mvs
mvs.CreateViewAndLayout()
batsrus = mvs.BATSRUS()
mvs.SetTitle("Cells colored by block_id")

import paraview.simple as pvs
renderView1 = pvs.GetActiveViewOrCreate('RenderView')
batsrusDisplay = pvs.Show(batsrus, renderView1, 'UnstructuredGridRepresentation')
pvs.ColorBy(batsrusDisplay, ('CELLS', 'block_id'))
# Trigger showing of colorbar (there is a better way)
pvs.Hide(batsrus)
pvs.Show(batsrus)
