from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

from magnetovis.Plugins.StructuredGrid import StructuredGridPlugin

@smproxy.source(name="MagnetovisT01", label="MagnetovisT01")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class T01Plugin(VTKPythonAlgorithmBase):

    from magnetovis.Objects.StructuredGrid import Script
    from magnetovis import extract_script, extract_kwargs, extract_function_call

    ScriptKwargs = extract_kwargs(Script)

    point_function_name = list(ScriptKwargs["point_function"])[0]
    PointFunction = extract_function_call(point_function_name, xml_encode=True)

    ArrayFunction = extract_function_call("T01", xml_encode=True)

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
                    'point_array_functions': {"T01": 
                                                {
                                                    "array_name": "B", 
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


    @smproperty.xml("""<DoubleVectorProperty 
        name="Pdyn" 
        command="SetPdyn" 
        number_of_elements="1"
        default_values="5.0">
       <Documentation>Solar wind pressure in nPa</Documentation>
     </DoubleVectorProperty>""")
    def SetPdyn(self, Pdyn):
        print("SetPdyn called with Pdyn = " + str(Pdyn))
        self.Pdyn = Pdyn
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="Dst" 
        command="SetDst" 
        number_of_elements="1"
        default_values="-10.0">
       <Documentation>Dst index in nT</Documentation>
     </DoubleVectorProperty>""")
    def SetDst(self, Dst):
        print("SetDst called with Dst = " + str(Dst))
        self.Dst = Dst
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="IMFBy" 
        label="IMF Bz"
        command="SetIMFBy" 
        number_of_elements="1"
        default_values="0.0">
       <Documentation>IMF By in nT</Documentation>
     </DoubleVectorProperty>""")
    def SetIMFBy(self, IMFBy):
        print("SetIMFBy called with IMFBy = " + str(IMFBy))
        self.IMFBy = IMFBy
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="G1Index"
        label="g1 index" 
        command="SetG1Index" 
        number_of_elements="1"
        default_values="0.0">
       <Documentation>g1 index</Documentation>
     </DoubleVectorProperty>""")
    def SetG1Index(self, G1Index):
        print("SetG1Index called with G1Index = " + str(G1Index))
        self.G1Index = G1Index
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="G2Index"
        label="g2 index" 
        command="SetG2Index" 
        number_of_elements="1"
        default_values="0.0">
       <Documentation>g2 index</Documentation>
     </DoubleVectorProperty>""")
    def SetG2Index(self, G2Index):
        print("SetG1Index called with G2Index = " + str(G2Index))
        self.G2Index = G2Index
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
