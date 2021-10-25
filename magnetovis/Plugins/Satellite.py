# same imports as earlier.
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase

# new module for ParaView-specific decorators.
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

@smproxy.source(name="MagnetovisSatellite", label="Satellite")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class SatellitePlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script
    from magnetovis.Objects.Satellite import Script

    # This is used to populate Script text area
    Script = extract_script(Script, None, xml_encode=True)
    Script = "# If script modified, drop-down values will be ignored&#xa;" + Script

    panel_visibility = "never"

    def __init__(self, **default_values):
        #print(**default_values)        
        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkPolyData')

        from magnetovis import extract_script
        from magnetovis.Objects.Satellite import Script

        # Note the use of "\n" instead of &#xa; in comment set above.
        Script = extract_script(Script, None, xml_encode=False)
        Script = "# If script modified, drop-down values will be ignored\n" + Script
        self.OriginalScript = Script

    def RequestData(self, request, inInfo, outInfo):
        print("RequestData called")

        from magnetovis import extract_script
        from magnetovis.Objects.Satellite import Script

        if self.OriginalScript == self.Script:
            kwargs = {
                'satellite_id': self.satellite_id,
                'time_o': self.time_o,
                'time_f': self.time_f,
                'coord_sys': self.coord_sys
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
        name="SatelliteID" 
        command="SetSatelliteID" 
        number_of_elements="1"
        default_values="0">
       <EnumerationDomain name="enum">
         <Entry value="0" text="ace"/>
         <Entry value="1" text="active"/>
         <Entry value="2" text="aec"/>
       </EnumerationDomain>
     </IntVectorProperty>""")
    def SetSatelliteID(self, idx):
        print("SetSatelliteID called with idx = " + str(idx))
        values = ["ace", "active", "aec"]
        self.satellite_id = values[idx]
        self.Modified()


    # Ordering of GUI elements is alphabetical. See proposed fix for this at
    # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/2846
    @smproperty.xml("""<StringVectorProperty 
        name="StartTime" 
        command="SetStartTime" 
        number_of_elements="1"
        default_values="2000-01-01T00:00:00">
       <Documentation>Start time string</Documentation>
     </StringVectorProperty>""")
    def SetStartTime(self, value):
        print("SetStartTime called.")
        self.time_o = value
        self.Modified()


    @smproperty.xml("""<StringVectorProperty 
        name="StopTime" 
        command="SetStopTime" 
        number_of_elements="1"
        default_values="2000-01-02T00:00:00">
       <Documentation>Stop time string</Documentation>
     </StringVectorProperty>""")
    def SetStopTime(self, value):
        print("SetStopTime called.")
        self.time_f = value
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


    @smproperty.stringvector(name="Script", command="SetScript", default_values=Script, panel_visibility=panel_visibility)
    @smhint.xml(r"<Widget type='multi_line' syntax='python'/>")
    def SetScript(self, Script):
        print("SetScript called.")
        self.Script = Script
        self.Modified()
