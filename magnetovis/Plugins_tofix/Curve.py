from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase

from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

# Label is what appears in pipeline with 1, 2, ... appended.
# Label is also what appears in the Sources -> Magnetovis drop-down menu.
# Name is how it is called, e.g., pvs.MagentovisCurve()
@smproxy.source(name="MagnetovisCurve", label="MagnetovisCurve")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class CurvePlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script, extract_kwargs, extract_function_call
    from magnetovis.Objects.Curve import Script

    ScriptKwargs = extract_kwargs(Script)

    point_function_name = list(ScriptKwargs["point_function"])[0]
    PointFunction = extract_function_call(point_function_name, xml_encode=True)

    point_array_function_name = list(ScriptKwargs["point_array_functions"])[0]
    ArrayFunction = extract_function_call(point_array_function_name, xml_encode=True)

    # This is used to populate Script text area
    Script = extract_script(Script, None, xml_encode=True)
    Script = "# If script modified, drop-down values will be ignored&#xa;" + Script

    def __init__(self, **default_values):
        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkPolyData')

        from magnetovis import extract_script
        from magnetovis.Objects.StructuredGrid import Script

        self.FullScript = Script
        Script = extract_script(Script, None, xml_encode=False)
        # Note the use of "\n" instead of &#xa; in comment set above.
        Script = "# If script modified, drop-down values will be ignored\n" + Script
        self.OriginalScript = Script

        def GetKwargs():
            from magnetovis import extract_kwargs, iso2ints

            point_function_kwargs = extract_kwargs(self.PointFunction)
            point_function_name = self.PointFunction.split("(")[0]

            # TODO: Do once for each array function
            point_array_function_name = self.ArrayFunction.split("(")[0]
            point_array_function_kwargs = extract_kwargs(self.ArrayFunction)
            point_array_function_kwargs['array_name'] = point_array_function_name

            kwargs = {
                        'time': self.time,
                        'coord_sys': self.coord_sys,
                        'Npts': self.Npts,
                        'point_function': {point_function_name: point_function_kwargs},
                        'point_array_functions': {point_array_function_name: point_array_function_kwargs}
            }

            return kwargs

        self.GetKwargs = GetKwargs

    def RequestData(self, request, inInfo, outInfo):

        print("RequestData called")

        if self.OriginalScript == self.Script:
            from magnetovis import extract_script
            Script = extract_script(self.FullScript, self.GetKwargs(self), xml_encode=False)
            print("Executing script using menu values.")
            # It does not seem possible to update script here to reflect
            # values in drop-downs when they change.
        else:
            print("Executing script using script that was modified.")
            Script = self.Script

        exec(Script)

        return 1

    from magnetovis import PluginSetFunctions

    SetTime = PluginSetFunctions.SetTime({})
    SetCoordinateSystem = PluginSetFunctions.SetCoordinateSystem({})
    SetPointFunction = PluginSetFunctions.SetPointFunction(PointFunction)
    SetArrayFunction = PluginSetFunctions.SetArrayFunction(ArrayFunction)
    SetScript = PluginSetFunctions.SetScript(Script)

    @smproperty.intvector(name="Npts", label="Npts", documentation="Number of points", default_values=ScriptKwargs["Npts"])
    def SetNpts(self, Npts):
        self.Npts = Npts
        self.Modified()

