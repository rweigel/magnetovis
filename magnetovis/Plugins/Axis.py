# same imports as earlier.
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase

# new module for ParaView-specific decorators.
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

@smproxy.source(name="MagnetovisAxis", label="Axis")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class AxisPlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script
    from magnetovis.Objects.Axis import Script

    # This is used to populate Script text area
    Script = extract_script(Script, None, xml_encode=True)
    Script = "# If script modified, drop-down values will be ignored&#xa;" + Script

    def __init__(self, **default_values):
        #print(**default_values)        
        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkPolyData')

        from magnetovis import extract_script
        from magnetovis.Objects.Axis import Script

        # Note the use of "\n" instead of &#xa; in comment set above.
        Script = extract_script(Script, None, xml_encode=False)
        Script = "# If script modified, drop-down values will be ignored\n" + Script
        self.OriginalScript = Script

    def RequestData(self, request, inInfo, outInfo):
        print("RequestData called")

        from magnetovis import extract_script
        from magnetovis.Objects.Axis import Script

        if self.OriginalScript == self.Script:
            kwargs = {
                'time': [*self.date, *self.time],
                'extent': self.extent,
                'coord_sys': self.coord_sys,
                'direction': self.direction
                }
            Script = extract_script(Script, kwargs, xml_encode=False)
            print("Executing script using drop-down values.")
            # It does not seem possible to update script here to reflect
            # values in drop-downs when they change.
        else:
            print("Executing script using script that was modified.")
            Script = self.Script

        exec(Script)
        return 1

    # Ordering of GUI elements is alphabetical. See proposed fix for this at
    # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/2846
    @smproperty.xml("""<IntVectorProperty 
        name="Date" 
        command="SetDate" 
        number_of_elements="3"
        default_values="2000 1 1">
       <Documentation>Year, Month, and Day</Documentation>
     </IntVectorProperty>""")
    def SetDate(self, year, month, day):
        print("SetDate called.")
        self.date = [year, month, day]
        self.Modified()

    @smproperty.xml("""<IntVectorProperty 
        name="Time" 
        command="SetTime" 
        number_of_elements="3"
        default_values="0 0 0">
       <Documentation>Hour, Minute, and Second</Documentation>
     </IntVectorProperty>""")
    def SetTime(self, hour, minute, second):
        print("SetTime called.")
        self.time = [hour, minute, second]
        self.Modified()

    @smproperty.xml("""<DoubleVectorProperty 
        name="Extent" 
        command="SetExtent" 
        number_of_elements="2"
        default_values="-40 40">
       <Documentation>Extent of axis</Documentation>
     </DoubleVectorProperty>""")
    def SetExtent(self, lower, upper):
        print("SetExtent called.")
        self.extent = [lower, upper]
        self.Modified()

    @smproperty.xml("""<IntVectorProperty 
        name="Direction" 
        command="SetDirection" 
        number_of_elements="1"
        default_values="0">
       <EnumerationDomain name="enum">
         <Entry value="0" text="X"/>
         <Entry value="1" text="Y"/>
         <Entry value="2" text="Z"/>
       </EnumerationDomain>
     </IntVectorProperty>""")
    def SetDirection(self, idx):
        print("SetDirection called with idx = " + str(idx))
        values = ["X", "Y", "Z"]
        self.direction = values[idx]
        self.Modified()

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


    @smproperty.stringvector(name="Script", command="SetScript", default_values=Script,  panel_visibility="never")
    @smhint.xml(r"<Widget type='multi_line' syntax='python'/>")
    def SetScript(self, Script):
        print("SetScript called.")
        self.Script = Script
        self.Modified()



