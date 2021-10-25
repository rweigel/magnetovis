from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

from magnetovis.Plugins.StructuredGrid import StructuredGridPlugin

@smproxy.source(name="MagnetovisT89c", label="Tsyganenko 89c")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class T89cPlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script
    from magnetovis.Objects.StructuredGrid import Script

    # This is used to populate Script text area
    Script = extract_script(Script, None, xml_encode=True)
    Script = "# If script modified, drop-down values will be ignored&#xa;" + Script

    # TODO: The panel_visibility is ignored here.
    panel_visibility = "never"
    DefaultPointFunction = "T89c(iopt=0, ps=0.0)"
 
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
            kwargs = extract_kwargs(self.point_function)
            kwargs['name'] = self.point_function.split("(")[0]
            kwargs = {
                    'extents': self.extents,
                    'point_array_functions': {"T89c": 
                                                {
                                                    "array_name": "B", 
                                                    "iopt": self.iopt,
                                                    "ps": self.ps
                                                }
                    },
                    'time': iso2ints(self.time),
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


    SetPointFunction = StructuredGridPlugin.SetPointFunctionWrapper(DefaultPointFunction, panel_visibility=panel_visibility)
    SetCoordinateSystem = StructuredGridPlugin.SetCoordinateSystem
    SetNxNyNz = StructuredGridPlugin.SetNxNyNz
    SetTime =  StructuredGridPlugin.SetTime
    SetXExtent =  StructuredGridPlugin.SetXExtent
    SetYExtent =  StructuredGridPlugin.SetYExtent
    SetZExtent =  StructuredGridPlugin.SetZExtent
    SetScript = StructuredGridPlugin.SetScript
