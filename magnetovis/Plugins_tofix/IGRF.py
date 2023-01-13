from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

from magnetovis.Plugins.StructuredGrid import StructuredGridPlugin

@smproxy.source(name="MagnetovisIGRF", label="MagnetovisIGRF")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class IGRFPlugin(VTKPythonAlgorithmBase):

    from magnetovis.Objects.StructuredGrid import Script
    from magnetovis import extract_script, extract_kwargs, extract_function_call

    ScriptKwargs = extract_kwargs(Script)

    point_function_name = list(ScriptKwargs["point_function"])[0]
    PointFunction = extract_function_call(point_function_name, xml_encode=True)

    ArrayFunction = extract_function_call("IGRF", xml_encode=True)

    # This is used to populate Script text area
    Script = extract_script(Script, None, xml_encode=True)
    Script = "# If script modified, drop-down values will be ignored&#xa;" + Script
 
    def __init__(self, **default_values):

        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkStructuredGrid')

        StructuredGridPlugin.__init__(self)

        # Extract kwargs and defaults from point function
        # TODO: Do once for each point function
        def GetKwargs(self):
            from magnetovis import extract_kwargs, iso2ints
            kwargs = {
                    'extents': self.extents,
                    'point_array_functions': {"IGRF": 
                                                {
                                                    "array_name": "B"
                                                }
                    },
                    'time': self.time,
                    'coord_sys': self.coord_sys,
                    'Nx': self.Nx,
                    'Ny': self.Ny,
                    'Nz': self.Nz
            }
            return kwargs

        self.GetKwargs = GetKwargs

    RequestData = StructuredGridPlugin.RequestData
    RequestInformation = StructuredGridPlugin.RequestInformation

    from magnetovis import PluginSetFunctions
    SetPointFunction = PluginSetFunctions.SetPointFunction(PointFunction)
    #SetArrayFunction = PluginSetFunctions.SetArrayFunction(ArrayFunction, panel_visibility="advanced")

    SetCoordinateSystem = StructuredGridPlugin.SetCoordinateSystem
    SetNxNyNz = StructuredGridPlugin.SetNxNyNz
    SetTime =  StructuredGridPlugin.SetTime
    SetXExtent =  StructuredGridPlugin.SetXExtent
    SetYExtent =  StructuredGridPlugin.SetYExtent
    SetZExtent =  StructuredGridPlugin.SetZExtent
    SetScript = StructuredGridPlugin.SetScript
