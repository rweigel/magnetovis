from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

from magnetovis.Plugins.StructuredGrid import StructuredGridPlugin

@smproxy.source(name="MagnetovisDipole", label="MagnetovisDipole")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class DipolePlugin(VTKPythonAlgorithmBase):

    from magnetovis.Objects.StructuredGrid import Script
    from magnetovis import extract_script, extract_kwargs, extract_function_call

    ScriptKwargs = extract_kwargs(Script)

    point_array_function_name = "dipole"
    ArrayFunction = extract_function_call(point_array_function_name, xml_encode=True)

    point_array_function_kwargs = extract_kwargs(ArrayFunction)
    M = point_array_function_kwargs["M"]

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
            from magnetovis import extract_kwargs

            # TODO: Do once for each array function
            point_array_function_name = self.ArrayFunction.split("(")[0]
            point_array_function_kwargs = extract_kwargs(self.ArrayFunction)
            point_array_function_kwargs['array_name'] = point_array_function_name

            kwargs = {
                    'extents': self.extents,
                    'point_array_functions': {point_array_function_name: point_array_function_kwargs},
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

    # Ordering of GUI elements is alphabetical. See proposed fix for this at
    # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/2846

    @smproperty.xml("""<DoubleVectorProperty 
        name="DipoleMoment" 
        label="Dipole Moment"
        command="SetDipoleMoment" 
        number_of_elements="1"
        default_values="{}">
       <Documentation>Dipole moment in A/m^2</Documentation>
     </DoubleVectorProperty>""".format(M))
    def SetDipoleMoment(self, DipoleMoment):
        print("SetDipoleMoment called.")
        self.M = DipoleMoment
        self.Modified()

    from magnetovis import PluginSetFunctions

    SetArrayFunction = PluginSetFunctions.SetArrayFunction(ArrayFunction, panel_visibility="never")
    SetCoordinateSystem = PluginSetFunctions.SetCoordinateSystem({})
    SetTime = PluginSetFunctions.SetTime({})
    SetScript = PluginSetFunctions.SetScript(Script)

    SetNxNyNz = StructuredGridPlugin.SetNxNyNz
    SetXExtent =  StructuredGridPlugin.SetXExtent
    SetYExtent =  StructuredGridPlugin.SetYExtent
    SetZExtent =  StructuredGridPlugin.SetZExtent
