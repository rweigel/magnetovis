from magnetovis.objects import *

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

class BaseClass:

    def __init__(self, sourceName=None, sourceArguments=None, renderSource=True, displayArguments=None):

        import paraview.simple as pvs

        print("__init__ called for " + sourceName)
        print("   sourceArguments:  " + str(sourceArguments))
        print("   displayArguments: " + str(displayArguments))
        print("   renderSource:     " + str(renderSource))

        self.programmableSource = pvs.ProgrammableSource()
        self.programmableSource.Script = extract_script(self.sourceFunction, sourceArguments)

        if hasattr(self, "sourceOutputDataSetType"):
            self.programmableSource.OutputDataSetType = self.sourceOutputDataSetType

        if hasattr(self, "sourceRequestInformationFunction"):
            self.programmableSource.ScriptRequestInformation = extract_script(self.sourceRequestInformationFunction, sourceArguments)

        if sourceName is not None:
            self.sourceName = sourceName

        pvs.RenameSource(self.sourceName, self.programmableSource)

        self.sourceArguments = sourceArguments
        if renderSource is True:
            self.SetDisplayOptions(displayArguments)
        else:
            self.displayProperties = None
            self.renderView = None

    def SetDisplayOptions(self, displayArguments):

        import paraview.simple as pvs

        if displayArguments is not None:
            if 'displayRepresentation' in displayArguments:
                # TODO: Get this from ParaView.
                validRepresentations = [
                                        'Surface', '3D Glyphs', 'Feature Edges',
                                        'Outline', 'Point Gaussian', 'Points',
                                        'Surface With Edges', 'Wireframe', 'Volume'
                                     ]

                assert displayArguments['displayRepresentation'] in validRepresentations, \
                        "Invalid displayRepresentation ({}). displayRepresentation must be one of: {}" \
                           .format(displayProperties['displayRepresentation'],
                                     validRepresentations)

        showSource = True
        renderView = None
        if displayArguments is not None:
            if 'showSource' in displayArguments:
                showSource = displayArguments['showSource']
                del displayArguments['showSource']
            if 'renderView' in displayArguments:
                renderView = displayArguments['renderView']
                del displayArguments['renderView']

        if renderView is None:
            self.renderView = pvs.GetActiveViewOrCreate('RenderView')

        if displayArguments is None:
            displayArguments = {}

        self.displayArguments = displayArguments
        # Create display properties object
        self.displayProperties = pvs.Show(self.programmableSource, self.renderView)

        self.displayProperties = self.displayFunction(displayArguments)

        # Update the view to ensure updated data information
        # TODO: Needed?
        self.renderView.Update()

        if showSource == False:
            pvs.Hide(self.programmableSource, self.renderView)

        return self

from magnetovis.Line import Script, _display
file = "Line"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "displayFunction": _display,
   "sourceName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Plane import Script, ScriptRequestInformation, OutputDataSetType, _display
file = "Plane"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "displayFunction": _display,
   "sourceName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

