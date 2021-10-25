# same imports as earlier.
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase

# new module for ParaView-specific decorators.
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

@smproxy.source(label="MagnetovisPlane")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class PlanePlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script
    from magnetovis.Objects.Plane import Script, ScriptRequestInformation
    Script = extract_script(Script, None, xml_encode=True)

    def __init__(self, **default_values):
        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkStructuredGrid')

    def RequestData(self, request, inInfo, outInfo):

        n_pts = self.Npts
        exec(self.Script)

        return 1

    def RequestInformation(self, request, inInfoVec, outInfoVec):
        from magnetovis.Plane import ScriptRequestInformation
        ScriptRequestInformation(self, Nx=2, Ny=2, Nz=1)
        return 1

    @smproperty.intvector(name="Npts", label="Npts", documentation="Text", default_values=9)
    def SetNpts(self, Npts):
        self.Npts = Npts
        self.Modified()

    @smproperty.stringvector(name="Script", command="SetScript", default_values=Script)
    @smhint.xml(r"<Widget type='multi_line' syntax='python'/>")
    def SetScript(self, Script):
        self.Script = Script
        self.Modified()


