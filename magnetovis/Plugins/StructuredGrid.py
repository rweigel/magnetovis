from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

@smproxy.source(name="MagnetovisStructuredGrid", label="MagnetovisStructuredGrid")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class StructuredGridPlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script
    from magnetovis.Objects.StructuredGrid import Script

    # This is used to populate Script text area
    Script = extract_script(Script, None, xml_encode=True)
    Script = "# If script modified, drop-down values will be ignored&#xa;" + Script

    panel_visibility = "never"

    SetPointFunction = None

    def __init__(self, **default_values):
        print("StructuredGrid __init__ called.")        
        print("default_values:")
        print(default_values)

        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkStructuredGrid')

        from magnetovis import extract_script
        from magnetovis.Objects.StructuredGrid import Script

        self.FullScript = Script
        # Note the use of "\n" instead of &#xa; in comment set above.
        Script = extract_script(Script, None, xml_encode=False)
        Script = "# If script modified, drop-down values will be ignored\n" + Script
        self.OriginalScript = Script
        self.extents = [[], [], []]

        # Extract kwargs and defaults from point function
        # TODO: Do once for each point function
        def GetKwargs(self):
            from magnetovis import extract_kwargs, iso2ints
            kwargs = extract_kwargs(self.point_function)
            point_function_name = self.point_function.split("(")[0]
            kwargs['name'] = point_function_name
            kwargs = {
                    'extents': self.extents,
                    'point_functions': {point_function_name: kwargs},
                    'time': iso2ints(self.time),
                    'coord_sys': self.coord_sys,
                    'Nx': self.Nx,
                    'Ny': self.Ny,
                    'Nz': self.Nz
            }
            return kwargs

        self.GetKwargs = GetKwargs
        #print(super().SetPointFunction)
    
    def RequestData(self, request, inInfo, outInfo):

        print("RequestData called")

        from magnetovis import extract_script
        if self.OriginalScript == self.Script:
            Script = extract_script(self.FullScript, self.GetKwargs(self), xml_encode=False)
            print("Executing script using menu values.")
            # It does not seem possible to update script here to reflect
            # values in drop-downs when they change.
        else:
            print("Executing script using script that was modified.")
            Script = self.Script

        exec(Script)

        return 1

    def RequestInformation(self, request, inInfoVec, outInfoVec):
        print("RequestInformation called.")
        from magnetovis.Objects.StructuredGrid import ScriptRequestInformation
        ScriptRequestInformation(self, Nx=self.Nx, Ny=self.Ny, Nz=self.Nz)
        return 1

    # Ordering of GUI elements is alphabetical. See proposed fix for this at
    # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/2846

    # TODO: Get default_values from kwargs of point_functions
    # TODO: Add one string vector per point_functions element

    @smproperty.stringvector(name="PointFunction", command="SetPointFunction", default_values="position()")
    def SetPointFunction(self, PointFunction):
        print("SetPointFunction called with PointFunction = " + PointFunction)
        self.point_function = PointFunction
        self.Modified()

    # To allow, e.g., DipolePlugin to use this with a different default_value
    def SetPointFunctionWrapper(default_values, panel_visibility="default"):
        @smproperty.stringvector(name="PointFunction", command="SetPointFunction", default_values=default_values, panel_visibility=panel_visibility)
        def SetPointFunction(self, PointFunction):
            print("SetPointFunction called with PointFunction = " + PointFunction)
            self.point_function = PointFunction
            self.Modified()
        return SetPointFunction

    @smproperty.xml("""<IntVectorProperty 
        name="CoordinateSystem" 
        command="SetCoordinateSystem" 
        number_of_elements="1"
        default_values="4">
       <EnumerationDomain name="enum">
         <Entry value="0" text="MAG"/>
         <Entry value="1" text="GEI"/>
         <Entry value="2" text="GEO"/>
         <Entry value="3" text="GSE"/>
         <Entry value="4" text="GSM"/>
         <Entry value="5" text="SM"/>
       </EnumerationDomain>
     </IntVectorProperty>""")
    def SetCoordinateSystem(self, idx):
        print("SetCoordinateSystem called with idx = " + str(idx))
        values = ["MAG", "GEI", "GEO", "GSE", "GSM", "SM"]
        self.coord_sys = values[idx]
        self.Modified()

    @smproperty.intvector(name="NxNyNz", label="Nx, Ny, Nz", documentation="Nx, Ny, Nz", default_values=[3,3,3])
    def SetNxNyNz(self, Nx, Ny, Nz):
        print("SetNxNyNz called.")
        self.Nx = Nx
        self.Ny = Ny
        self.Nz = Nz
        self.Modified()

    @smproperty.xml("""<StringVectorProperty 
        name="Time" 
        command="SetTime" 
        number_of_elements="1"
        default_values="2000-01-01T00:00:00">
       <Documentation>Time string</Documentation>
     </StringVectorProperty>""")
    def SetTime(self, value):
        print("SetTime called.")
        self.time = value
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="XExtent" 
        label="XMin, XMax"
        command="SetXExtent" 
        number_of_elements="2"
        default_values="-40 40">
       <Documentation>XMin, XMax</Documentation>
     </DoubleVectorProperty>""")
    def SetXExtent(self, XMin, XMax):
        print("SetXExtent called.")
        self.extents[0] = [XMin, XMax]
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="YExtent" 
        label="YMin, YMax"
        command="SetYExtent" 
        number_of_elements="2"
        default_values="-40 40">
       <Documentation>YMin, YMax</Documentation>
     </DoubleVectorProperty>""")
    def SetYExtent(self, YMin, YMax):
        print("SetYExtent called.")
        self.extents[1] = [YMin, YMax]
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="ZExtent" 
        label="ZMin, ZMax"
        command="SetZExtent" 
        number_of_elements="2"
        default_values="-40 40">
       <Documentation>ZMin, ZMax</Documentation>
     </DoubleVectorProperty>""")
    def SetZExtent(self, ZMin, ZMax):
        print("SetZExtent called.")
        self.extents[2] = [ZMin, ZMax]
        self.Modified()

    @smproperty.stringvector(name="Script", command="SetScript", default_values=Script, panel_visibility=panel_visibility)
    @smhint.xml(r"<Widget type='multi_line' syntax='python'/>")
    def SetScript(self, Script):
        self.Script = Script
        self.Modified()


