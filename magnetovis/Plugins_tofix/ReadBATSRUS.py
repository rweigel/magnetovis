from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

@smproxy.source(name="MagnetovisReadBATSRUS", label="MagnetovisReadBATSRUS")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class ReadBATSRUSPlugin(VTKPythonAlgorithmBase):
 
    def __init__(self, **default_values):

        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkPolyData')

    def RequestData(self, request, inInfo, outInfo):

        # Being executed in Plugin
        from vtkmodules.vtkCommonDataModel import vtkPolyData
        output = vtkPolyData.GetData(outInfo, 0)
        
        import vtk
        if self.filename:
            reader = vtk.vtkPolyDataReader()
            reader.SetFileName(self.filename)
            reader.Update()

        print("Reading " + self.filename)
        output = output.ShallowCopy(reader.GetOutput())

        return 1

    @smproperty.stringvector(name="FileName", default_values="/tmp/proton_pitch60_L2_motion.vtk")
    @smdomain.filelist()
    @smhint.filechooser(extensions="vtk", file_description="BATSRUS .out file")
    def SetFileName(self, name):
        self.filename = name


