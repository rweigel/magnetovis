def CreatePlugin(name):

    import importlib

    import magnetovis as mvs
    mvs.logger.info("Called.")

    from magnetovis import extract
    from magnetovis.paraview import PluginSetFunctions

    Script = importlib.import_module('magnetovis.Sources.' + name).Script
    OutputDataSetType = importlib.import_module('magnetovis.Sources.' + name).OutputDataSetType()
    ScriptRequestInformation = importlib.import_module('magnetovis.Sources.' + name).ScriptRequestInformation

    from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
    from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

    @smproxy.source(name="Magnetovis" + name, label="Magnetovis" + name)
    @smhint.xml('<ShowInMenu category="Magnetovis"/>')
    class Plugin(VTKPythonAlgorithmBase):

        import magnetovis as mvs
        mvs.logger.info("Called.")

        # This is used to populate Script text area
        ScriptBodyText, ScriptKwargs = extract.extract_script(Script, None, xml_encode=True)
        ScriptBodyText = "# If script modified, drop-down values will be ignored&#xa;" + ScriptBodyText

        # Ordering of GUI elements is alphabetical. See proposed fix for this at
        # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/2846

        SetTime = PluginSetFunctions.SetTime(ScriptKwargs["time"])
        SetCoordinateSystem = PluginSetFunctions.SetCoordinateSystem(ScriptKwargs["coord_sys"])
        SetDimensions = PluginSetFunctions.SetDimensions(ScriptKwargs["dimensions"])
        SetPointFunction = PluginSetFunctions.SetPointFunction(ScriptKwargs["point_function"])
        SetPointArrayFunctions = PluginSetFunctions.SetPointArrayFunctions(ScriptKwargs["point_array_functions"])
        SetScriptBodyText = PluginSetFunctions.SetScriptBodyText(ScriptBodyText)

        @smproperty.xml(PluginSetFunctions.GridPropertyGroupString())

        def __init__(self, **default_values):

            mvs.logger.info("Called.")

            VTKPythonAlgorithmBase.__init__(self,
                    nInputPorts=0,
                    nOutputPorts=1,
                    outputType=OutputDataSetType)

            #################################################
            # The following hack is used to automatically set
            # the default display properties after the source
            # is shown.
            def UpdateDisplayOptions(caller, event):
                import paraview.simple as pvs
                import magnetovis as mvs
                #print("Caller")
                #print(caller)
                #print("Event: " + str(event))
                sources = pvs.GetSources()
                for key in sources.keys():
                    if not hasattr(sources[key],'_default_display_properies_set'):
                        sources[key].add_attribute('_default_display_properies_set', True)
                        #print("Removing " + str(cb_id))
                        self.RemoveObserver(cb_id)
                        mvs.SetDisplayProperties(source=sources[key])
                else:
                    #print("Already set.")
                    pass

            cb_id = self.AddObserver('EndEvent', UpdateDisplayOptions)
            #print("cb_id = " + str(cb_id))
            #################################################

 
            self._logger = mvs.logger

            self.Script = Script
            ScriptBodyText, _ = extract.extract_script(Script, None, xml_encode=False)
            # Note the use of "\n" instead of &#xa; in comment when set as default.
            ScriptBodyText = "# If script modified, drop-down values will be ignored\n" + ScriptBodyText
            self.ScriptBodyTextOriginal = ScriptBodyText

            # Extract kwargs and defaults from point function
            def GetKwargs(self):
                from magnetovis import extract
                # TODO: Do once for each point array function            

                point_array_functions = self.point_array_functions.copy()
                if self.point_array_functions_modified == True:
                    self.point_array_functions_modified = False

                # Flatten list.
                # https://stackoverflow.com/a/952952
                point_array_functions = [item for sublist in self.point_array_functions for item in sublist]

                kwargs = {
                            'time': self.time,
                            'coord_sys': self.coord_sys,
                            'dimensions': self.dimensions,
                            'point_function': self.point_function,
                            'point_array_functions': point_array_functions
                }
                return kwargs

            self.GetKwargs = GetKwargs


        def RequestData(self, request, inInfo, outInfo):

            mvs.logger.info("Called.")

            if self.ScriptBodyText == self.ScriptBodyTextOriginal:
                from magnetovis import extract
                kwargs = self.GetKwargs(self)
                mvs.logger.info("Executing script using kwargs from menu of " + str(kwargs))
                ScriptBodyText, _ = extract.extract_script(self.Script, kwargs, xml_encode=False)
                # TODO: Update script in text area
            else:
                mvs.logger.info("Executing script in Script text area.")
                ScriptBodyText = self.ScriptBodyText

            import vtk
            # Equivalent to, e.g., vtkDataSet = vtk.StructuredGrid()
            vtkDataSet = getattr(vtk, OutputDataSetType)()
            output = vtkDataSet.GetData(outInfo, 0)
            #print(ScriptBodyText)
            exec(ScriptBodyText)

            mvs.logger.info("Finished execution of script.")

            return 1


        def RequestInformation(self, request, inInfoVec, outInfoVec):
            mvs.logger.info("Called.")

            ScriptRequestInformation(self, dimensions=self.dimensions)
            return 1

    return Plugin
