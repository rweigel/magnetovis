# name is the kwarg name passed to the plugin.
# label must match name otherwise a, e.g., "StructuredGrid has no attribute 'time'" is thrown.
# See https://discourse.paraview.org/t/bug-in-how-label-is-handled-in-python-based-source-plugin/8342
# and
# https://discourse.paraview.org/t/python-plugin-smproxy-keyword-arguments-arent-working-as-expected/4869

def GridPropertyGroupString():

    return """  <PropertyGroup label="Date and Time in ISO8601 format (YYYY-MM-DD[THH[:MM[:SS]]])">
                    <Property function="time" name="time"/>
                </PropertyGroup>
                <PropertyGroup label="Coordinate system">
                    <Property function="coord_sys" name="coord_sys"/>
                </PropertyGroup>
                <PropertyGroup label="Dimensions (Nx, Ny, Nz)">
                    <Property function="dimensions" name="dimensions"/>
                </PropertyGroup>
                <PropertyGroup label="Point creation function call">
                    <Property function="point_function" name="point_function"/>
                </PropertyGroup>
                <PropertyGroup label="Point array name: Point array creation function call">
                    <Property function="point_array_functions" name="point_array_functions"/>
                </PropertyGroup>"""    

def SetID(default_values):
  from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain
  @smproperty.stringvector(name="selfID", label="selfID", command="SetID", documentation="", default_values=default_values)
  def SetID(self, ID):
      self.mvs.logger.info(name + " = " + ID)
      setattr(self, name, ID)
      self.Modified()
  return SetID

def SetTime(default_values, name="time", label="time", panel_visibility="default"):
    from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain
    @smproperty.stringvector(name=name, label=label, command="SetTime", documentation="Time in ISO8601 format (YYYY-MM-DD[THH[:MM[:SS]]])", default_values=default_values)
    def SetTime(self, Time):
        self.mvs.logger.info(name + " = " + Time)
        setattr(self, name, Time)
        self.Modified()
    return SetTime


def SetCoordinateSystem(default_values, name="coord_sys", panel_visibility="default"):
    from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain
    # TODO: Set XML Entries based on the following list.
    values = ["MAG", "GEI", "GEO", "GSE", "GSM", "SM"]
    default_values = values.index(default_values)
    @smproperty.xml("""<IntVectorProperty 
        name="{}" 
        command="SetCoordinateSystem" 
        number_of_elements="1"
        default_values="{}">
       <EnumerationDomain name="enum">
         <Entry value="0" text="MAG"/>
         <Entry value="1" text="GEI"/>
         <Entry value="2" text="GEO"/>
         <Entry value="3" text="GSE"/>
         <Entry value="4" text="GSM"/>
         <Entry value="5" text="SM"/>
       </EnumerationDomain>
       <Documentation>Coordinate System</Documentation>
     </IntVectorProperty>""".format(name, default_values))
    def SetCoordinateSystem(self, idx):
        self.mvs.logger.info("idx = " + str(idx))
        values = ["MAG", "GEI", "GEO", "GSE", "GSM", "SM"]
        setattr(self, name, values[idx])
        self.Modified()

    return SetCoordinateSystem


def SetDimensions(default_values, name="dimensions", label="dimensions", panel_visibility="default"):
    from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain
    @smproperty.intvector(name=name, label=label, command="SetDimensions", documentation="Nx, Ny, Nz", default_values=default_values)
    def SetDimensions(self, Nx, Ny, Nz):
        self.mvs.logger.info("Nx, Ny, Nz = {}, {}, {}".format(Nx, Ny, Nz))
        setattr(self, name, [Nx, Ny, Nz])
        self.Modified()
    return SetDimensions


def SetPointFunction(default_values, name="point_function", label="point_function", panel_visibility="default"):
    from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain
    @smproperty.stringvector(name=name, label="point_function", command="SetPointFunction", default_values=default_values, panel_visibility=panel_visibility)
    def SetPointFunction(self, PointFunction):
        self.mvs.logger.info(name + " = " + PointFunction)
        setattr(self, name, PointFunction)
        self.Modified()
    return SetPointFunction


def SetPointArrayFunctions(default_values, name="point_array_functions", label=None, panel_visibility="default"):
    from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain
    if label is None:
        label = name
    @smproperty.xml("""<StringVectorProperty 
        name="{}"
        label="{}"
        command="SetPointArrayFunctions"
        element_types="2"
        number_of_elements="{}"
        number_of_elements_per_command="1"
        repeat_command="1"
        default_values_delimiter="_!_"
        default_values="{}">
        <Documentation short_help=''></Documentation>
        </StringVectorProperty>""".format(name, name, len(default_values), "_!_".join(default_values)))
    def SetPointArrayFunctions(self, *PointArrayFunctions):
        # This function is called once for each row after the Apply button is clicked.        
        if not hasattr(self, 'point_array_functions') or \
                self.point_array_functions_modified == False:
            # This is set to False after RequestData is called.
            self.point_array_functions = []

        self.point_array_functions_modified = True
        self.point_array_functions.append(PointArrayFunctions)
        self.Modified()
    return SetPointArrayFunctions


# Keep this because it demonstrates a string entry widget with two columns.
def SetPointArrayFunctionsOld(default_values, name="point_array_functions", label=None, panel_visibility="default"):
    from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain
    if label is None:
        label = name
    @smproperty.xml("""<StringVectorProperty 
        name="{}"
        label="{}"
        command="SetPointArrayFunctions"
        element_types="2 2"
        number_of_elements="4"
        number_of_elements_per_command="2"
        repeat_command="1"
        default_values_delimiter=":"
        default_values="{}">
        <Documentation short_help=''></Documentation>
        </StringVectorProperty>""".format(name, name, ":".join(default_values)))
    def SetPointArrayFunctionsOld(self, *PointArrayFunctions):
        # This function is called once for each row after the Apply button is clicked.        
        # Ideally we would be able set self.point_array_functions = [] before the first call.
        # Instead, self.point_array_functions = [] is set in GetKwargs of the plugin after
        # a copy is made.
        if not hasattr(self, '_call'):
            self._call = 1
            self._external_call = False
        else:
            if self._external_call == False:
                self._call = self._call + 1
            else:
                self._call = 0
        if self._call > 2:
            self._external_call = True
            self.point_array_functions = []

        self.mvs.logger.info("PointArrayFunctions")
        self.mvs.logger.info(PointArrayFunctions)
        if not hasattr(self, 'point_array_functions'):
            self.point_array_functions = []
        self.point_array_functions.append(PointArrayFunctions)
        #setattr(self, name, self.point_array_functions)
        self.Modified()
    return SetPointArrayFunctions


def SetScriptBodyText(default_values, name="Script", label="Script", panel_visibility="advanced"):
    from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain
    @smproperty.stringvector(name=name, label=name, command="SetScriptBodyText", default_values=default_values, panel_visibility=panel_visibility)
    @smhint.xml(r"<Widget type='multi_line' syntax='python'/>")
    def SetScriptBodyText(self, ScriptBodyText):
        self.ScriptBodyText = ScriptBodyText
        self.Modified()
    return SetScriptBodyText
