# same imports as earlier.
from vtkmodules.vtkCommonDataModel import vtkDataSet
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.numpy_interface import dataset_adapter as dsa


# new module for ParaView-specific decorators.
from paraview.util.vtkAlgorithm import smproxy, smproperty, smdomain

# to add a source, instead of a filter, use the `smproxy.source` decorator.
@smproxy.source(label="Magnetovis/Line Plugin")
class LinePlugin(VTKPythonAlgorithmBase):

    default_values = {"n_pts": 10}

    def __init__(self, **default_values):
        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkPolyData')

    def RequestData(self, request, inInfo, outInfo):
        print("here")
        n_pts = self.n_pts
        from vtkmodules.vtkCommonDataModel import vtkPolyData
        import vtk
        output = vtkPolyData.GetData(outInfo, 0)
        points = vtk.vtkPoints()
        for i in range(0, n_pts):
            x = i*10/n_pts
            y = 0
            z = 0
            points.InsertPoint(i, x, y, z)

        output.SetPoints(points)

        aPolyLine = vtk.vtkPolyLine()

        aPolyLine.GetPointIds().SetNumberOfIds(n_pts)
        for i in range(0, n_pts):
            aPolyLine.GetPointIds().SetId(i, i)

        output.Allocate(1, 1)
        output.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())

        return 1

    #@smproperty.intvector(name="n_pts", documentation="Text", default_values=default_values["n_pts"])
    @smproperty.xml("""
        <IntVectorProperty name="n_pts"
            number_of_elements="1"
            default_values="4"
            command="SetThetaResolution">
           <IntRangeDomain name="range" />
           <Documentation>Set number of points</Documentation>
        </IntVectorProperty>""")
    def SetThetaResolution(self, x):
        print("SetNPts: n_pts = " + str(x))
        self.Modified()
        self.n_pts = x

    @smproperty.xml("""
        <DoubleVectorProperty name="Center"
            number_of_elements="3"
            default_values="0 0 0"
            command="SetCenter">
            <DoubleRangeDomain name="range" />
            <Documentation>Set center of the superquadric</Documentation>
        </DoubleVectorProperty>""")
    def SetCenter(self, x, y, z):
        #self._realAlgorithm.SetCenter(x,y,z)
        self.Modified()
