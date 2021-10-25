# same imports as earlier.
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase

# new module for ParaView-specific decorators.
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

@smproxy.source(name="MagnetovisLine", label="SimpleLine")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class SimpleLinePlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script
    from magnetovis.Objects.Line import Script
    Script = extract_script(Script, None, xml_encode=True)

    def __init__(self, **default_values):
        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkPolyData')

    def RequestData(self, request, inInfo, outInfo):
        n_pts = self.Npts
        exec(self.Script)

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


