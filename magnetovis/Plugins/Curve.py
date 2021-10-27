from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase

from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

# Label is what appears in pipeline with 1, 2, ... appended.
# Label is also what appears in the Sources -> Magnetovis drop-down menu.
# Name is now it is called, e.g., pvs.MagentovisCurve()
@smproxy.source(name="MagnetovisCurve", label="MagnetovisCurve")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class CurvePlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script
    from magnetovis.Objects.Curve import Script

    DefaultScript = extract_script(Script, None, xml_encode=True)

    # TODO?: Extract DefaultPointFunction string from signature in Script
    # TODO?: Make explicit by using magnetovis.functions.circle()
    DefaultNpts = 9
    DefaultPointFunction = "circle()"

    ScriptVisible = "advanced"

    def __init__(self, **default_values):
        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkPolyData')

    def RequestData(self, request, inInfo, outInfo):

        from magnetovis import extract_kwargs, extract_script
        point_function_name = self.point_function.split("(")[0]
        kwargs = extract_kwargs(self.point_function)
        from magnetovis.Objects.Curve import Script
        Script = extract_script(Script, kwargs, xml_encode=False)        
        exec(Script)
        return 1

    @smproperty.intvector(name="Npts", label="Npts", documentation="Number of points", default_values=DefaultNpts)
    def SetNpts(self, Npts):
        self.Npts = Npts
        self.Modified()

    @smproperty.stringvector(name="PointFunction", command="SetPointFunction", default_values=DefaultPointFunction)
    def SetPointFunction(self, PointFunction):
        #print("SetPointFunction called with PointFunction = " + PointFunction)
        self.point_function = PointFunction
        self.Modified()

    @smproperty.stringvector(name="Script", command="SetScript", default_values=DefaultScript, panel_visibility=ScriptVisible)
    @smhint.xml(r"<Widget type='multi_line' syntax='python'/>")
    def SetScript(self, Script):
        self.Script = Script
        self.Modified()


