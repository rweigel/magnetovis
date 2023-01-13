from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

from magnetovis.Plugins.StructuredGrid import StructuredGridPlugin

@smproxy.source(name="MagnetovisT89c", label="MagnetovisT89c")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class T89cPlugin(VTKPythonAlgorithmBase):

    from magnetovis.Objects.StructuredGrid import Script
    from magnetovis import extract_script, extract_kwargs, extract_function_call

    ScriptKwargs = extract_kwargs(Script)

    point_function_name = list(ScriptKwargs["point_function"])[0]
    PointFunction = extract_function_call(point_function_name, xml_encode=True)

    ArrayFunction = extract_function_call("T89c", xml_encode=True)

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
                    'point_array_functions': {"T89c": 
                                                {
                                                    "array_name": "B", 
                                                    "iopt": self.iopt,
                                                    "ps": self.ps
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

    @smproperty.xml("""<IntVectorProperty 
        name="Inputs" 
        command="SetInputs" 
        number_of_elements="1"
        default_values="1">
       <EnumerationDomain name="enum">
         <Entry value="0" text="Use measurements for inputs (if available)"/>
         <Entry value="1" text="Use menu values for inputs"/>
       </EnumerationDomain>
     </IntVectorProperty>""")
    def SetInputs(self, Inputs):
        print("SetInputs called with Use = " + str(Inputs))
        self.Inputs = Inputs
        self.Modified()


    @smproperty.xml("""<IntVectorProperty 
        name="KpRange" 
        command="SetKpRange" 
        number_of_elements="1"
        default_values="0">
       <EnumerationDomain name="enum">
         <Entry value="0" text="0, 0+"/>
         <Entry value="1" text="1-, 1, 1+"/>
         <Entry value="2" text="2-, 2, 2+"/>
         <Entry value="3" text="3-, 3, 3+"/>
         <Entry value="4" text="4-, 4, 4+"/>
         <Entry value="5" text="5-, 5, 5+"/>
         <Entry value="6" text="6-"/>
       </EnumerationDomain>
     </IntVectorProperty>""")
    def SetKpRange(self, iopt):
        print("SetKpRange called with iopt = " + str(iopt))
        self.iopt = iopt
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="DipoleTilt" 
        command="SetDipoleTilt" 
        number_of_elements="1"
        default_values="0.0">
       <Documentation>Geo-dipole tilt angle in radins</Documentation>
     </DoubleVectorProperty>""")
    def SetDipoleTilt(self, ps):
        print("SetDipoleTilt called with ps = " + str(ps))
        self.ps = ps
        self.Modified()
