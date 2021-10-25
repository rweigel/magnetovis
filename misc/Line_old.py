# same imports as earlier.
from vtkmodules.vtkCommonDataModel import vtkDataSet
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.numpy_interface import dataset_adapter as dsa

# new module for ParaView-specific decorators.
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

# to add a source, instead of a filter, use the `smproxy.source` decorator.
def extract_script(function, sourceArguments):

    debug = False

    import inspect

    def extract_kwargs(function, sourceArguments):

        # Based on https://stackoverflow.com/a/54009257
        from inspect import signature, Parameter
        head = ""
        for x, p in signature(function).parameters.items():
            if (p.default is not Parameter.empty) and p.kind == Parameter.POSITIONAL_OR_KEYWORD:
                if sourceArguments is not None and x in sourceArguments:
                    arg = sourceArguments[x]
                else:
                    arg = p.default

                if isinstance(arg, str):
                    head = head + '{} = "{}"\n'.format(x, arg)
                else:
                    head = head + '{} = {}\n'.format(x, arg)

        return head

    head = extract_kwargs(function, sourceArguments)

    lines = inspect.getsource(function)
    lines = lines.split("\n")
    found_def_start = False
    found_def_end = False
    found_first_indent = False
    body_start = 0
    for i, line in enumerate(lines):
      if debug: print(i,line)
      if not found_first_indent:

         if line.startswith("def"):
            found_def_start = True
            if debug: print("Found def start: " + line)

         if found_def_start is True and line.endswith(":"):
            found_def_end = True
            if debug: print("Found def end: " + line)

         if found_def_start and found_def_end:
            indent_size = len(line) - len(line.lstrip())
            if indent_size > 0:
               found_first_indent = True
               if debug: print("Indent size: " + str(indent_size))
               body_start = i
               lines[i] = line[indent_size:]
               if debug: print("Unindented line: "); print(i,lines[i])
         else:
            lines[i] = ""
      else:
         lines[i] = line[indent_size:]
         if debug: print("Unindented line: "); print(i,lines[i])

    return head + "\n".join(lines[body_start:])

def planescript():
    points = [[-40., -40.,   0.],[ 40., -40.,   0.],[-40.,  40.,   0.],[ 40.,  40.,   0.]]

    import vtk
    from vtk.numpy_interface import dataset_adapter as dsa

    from vtkmodules.vtkCommonDataModel import vtkPolyData

    #executive = self.GetExecutive()
    #outInfo = executive.GetOutputInformation(0)
    #outInfo.Set(executive.WHOLE_EXTENT(), 0, 1, 0, 1, 0, 1)
    #iv = vtk.vtkInformationVector()
    #iv.Append(outInfo)
    #output = vtkPolyData.GetData(iv, 0)
    output = vtkPolyData.GetData(outInfo, 0)

    pvtk = dsa.numpyTovtkDataArray(points)
    pts = vtk.vtkPoints()
    pts.Allocate(4)
    pts.SetData(pvtk)
    output.SetPoints(pts)
    if False:
        for name, array in data_arrays.items():
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetPointData().AddArray(vtkArray)

@smproxy.source(label="Magnetovis/Line_old", name="LinePlugin_old")
class LinePlugin_old(VTKPythonAlgorithmBase):

    def __init__(self, **default_values):
        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkPolyData')
        print(default_values)

    def RequestData(self, request, inInfo, outInfo):
        n_pts = self.Npts
        #Points = self.Points
        #print(Points)
        #print(Points(1,10))

        # Sources, readers, and filters all produce data.
        # https://docs.paraview.org/en/latest/UsersGuide/understandingData.html

        # Content that one could enter into the Programmable Source
        # text area in the ParaView GUI.
        import vtk
        if False:
            #print(list(pvs.GetSources().keys())[list(pvs.GetSources().values()).index(pvs.GetActiveSource())][0])
            #source = pvs.FindSource(self.sourceName)
            #print(source)
            sourceData = paraview.servermanager.Fetch(self.programmableSource)

            for idx in range(0, sourceData.GetPointData().GetNumberOfArrays()):
                data = sourceData.GetPointData().GetArray(idx)
                name = sourceData.GetPointData().GetArrayName(idx)
                print("Name: " + name)
                print("Data: ")
                print(vtk_to_numpy(data))

            output = self.GetPolyDataOutput()
            import vtk
            ss = vtk.vtkSphereSource()
            ss.Update()
            print(ss.GetOutput())
            print(ss)
            output = output.ShallowCopy(ss.GetOutput())

        print(self)

        import vtk
        from vtkmodules.vtkCommonDataModel import vtkPolyData
        output = vtkPolyData.GetData(outInfo, 0)

        # TODO: Do this with dataset adapter
        points = vtk.vtkPoints()
        for i in range(0, n_pts):
            x = i
            y = 0
            z = 0
            points.InsertPoint(i, x, y, z)

        output.SetPoints(points)

        aPolyLine = vtk.vtkPolyLine()

        aPolyLine.GetPointIds().SetNumberOfIds(n_pts)
        for i in range(0, n_pts):
            aPolyLine.GetPointIds().SetId(i, i)

        output.Allocate(1, 1)
        output.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())

        return 1

    def RequestInformation(self, request, inInfoVec, outInfoVec):
        from magnetovis.Line import ScriptRequestInformation 
        ScriptRequestInformation(self, request, inInfoVec, outInfoVec)
        return 1

    from magnetovis.Line import Script
    tmp = extract_script(Script, None)
    #tmp = extract_script(planescript, None)
    tmp = tmp.replace("\n","&#xa;")
    print(tmp)
    #print(self.Script2)

    @smproperty.stringvector(name="Script", command="SetScript", default_values=tmp)
    @smhint.xml(r"<Widget type='multi_line' syntax='python'/>")
    def SetScript(self, text):
        self.script = text
        self.Modified()


    @smproperty.stringvector(name="Script2", command="SetScript2", default_values=tmp)
    @smhint.xml(r"<Widget type='multi_line' syntax='python'/>")
    def SetScript2(self, text):
        def GeneratePoints(i, n_pts):
            x = 10*i/n_pts
            y = 0
            z = 0
            return x, y, z
        self.script2 = GeneratePoints
        self.Modified()


    @smproperty.intvector(name="Npts", documentation="Text", default_values=9)
    def SetNpts(self, Npts):
        self.Npts = Npts
        self.Modified()


