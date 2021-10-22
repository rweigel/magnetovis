from paraview.util.vtkAlgorithm import smdomain, smhint, smproperty, smproxy
import vtk
import vtk.util.vtkAlgorithm as valg

MENU_CAT = 'Test Category'

@smproxy.source(name='Earth', label='Earth')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
class CustomEarthSource(valg.VTKPythonAlgorithmBase):
    """A simple data source to produce a ``vtkEarthSource`` outlining the
    Earth's continents. This works well with our ``GlobeSource``.
    """
    def __init__(self, radius=6371.0e6):
        valg.VTKPythonAlgorithmBase.__init__(self,
                                             nInputPorts=0,
                                             nOutputPorts=1, outputType='vtkPolyData')
        self.__radius = radius
        #self.add_attribute("radius", 10)

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate the output"""
        pdo = self.GetOutputData(outInfo, 0)
        earth = vtk.vtkEarthSource()
        earth.SetRadius(self.__radius)
        earth.OutlineOff()
        earth.Update()
        earth.GetOutput()
        pdo.ShallowCopy(earth.GetOutput())
        return 1

    @smproperty.doublevector(name="Radius", default_values=6371.0e6)
    def set_radius(self, radius):
        """Set the radius of the globe. Defualt is 6.371.0e9 meters"""
        if self.__radius != radius:
            self.__radius = radius
            self.Modified()
