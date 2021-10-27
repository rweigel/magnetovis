from magnetovis.objects import *

def iso2ints(isostr):
    import re
    tmp = re.split("-|:|T|Z", isostr)
    if len(tmp) > 6:
        tmp = tmp[0:5]

    int_list = []
    for str_int in tmp:
        if str_int != "Z" and str_int != '':
            int_list.append(int(str_int))

    return int_list


def extract_kwargs(function, default_kwargs=None):

    import types
    from inspect import signature, Parameter

    kwargs = {}
    if isinstance(function, str):
        # e.g., function = "circle(radius=1, center=[0, 0, 0])"
        # https://stackoverflow.com/questions/2626582/running-exec-inside-function
        function_call_parts = function.split("(")
        function_call_parts[0] = "function_pointer"
        function_call = '('.join(function_call_parts)
        function_def = "def " + function_call + ": pass"
        #print(function_def)
        exec_dict = {}
        exec(function_def, exec_dict)
        function_pointer = exec_dict["function_pointer"]
    else:
        function_pointer = function

    # Based on https://stackoverflow.com/a/54009257
    kwargs = {}
    for x, p in signature(function_pointer).parameters.items():
        if (p.default is not Parameter.empty) and p.kind == Parameter.POSITIONAL_OR_KEYWORD:
            kwargs[x] = p.default

    for x, p in signature(function_pointer).parameters.items():
        if (p.default is not Parameter.empty) and p.kind == Parameter.POSITIONAL_OR_KEYWORD:
            if default_kwargs is not None and x in default_kwargs:
                kwargs[x] = default_kwargs[x]
            else:
                kwargs[x] = p.default

    return kwargs


def extract_script(function, sourceArguments, xml_encode=False):

    import inspect

    debug = False

    kwargs = extract_kwargs(function, default_kwargs=sourceArguments)

    head = ""
    for key in kwargs:
        if isinstance(kwargs[key], str):
            head = head + '{} = "{}"\n'.format(key, kwargs[key])
        else:
            head = head + '{} = {}\n'.format(key, kwargs[key])
    head = head + "\n"

    if debug: print(function)

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

    script = head + "\n".join(lines[body_start:])

    if xml_encode is True:
        script = script.replace("\n","&#xa;").replace("'","&#39;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")

    return script

class BaseClass:

    def __init__(self, registrationName=None, sourceArguments=None, renderSource=True, displayArguments=None):

        import paraview.simple as pvs

        debug = False

        if debug:
            print("__init__ called for " + registrationName)
            print("   sourceArguments:  " + str(sourceArguments))
            print("   displayArguments: " + str(displayArguments))
            print("   renderSource:     " + str(renderSource))

        self.programmableSource = pvs.ProgrammableSource()
        self.programmableSource.Script = extract_script(self.sourceFunction, sourceArguments)

        if hasattr(self, "sourceOutputDataSetType"):
            self.programmableSource.OutputDataSetType = self.sourceOutputDataSetType

        if hasattr(self, "sourceRequestInformationFunction"):
            self.programmableSource.ScriptRequestInformation = extract_script(self.sourceRequestInformationFunction, sourceArguments)

        if registrationName is not None:
            self.registrationName = registrationName

        pvs.RenameSource(self.registrationName, self.programmableSource)

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

        # Create display properties object
        self.displayArguments = displayArguments
        self.displayProperties = pvs.Show(self.programmableSource, self.renderView)

        self.displayProperties = self.displayFunction(self.programmableSource, self.displayProperties, self.renderView, **self.displayArguments)

        # Update the view to ensure updated data information
        # TODO: Needed?
        self.renderView.Update()

        if showSource == False:
            pvs.Hide(self.programmableSource, self.renderView)

        return self

# TODO: Automate the following by reading magnetovis/Objects directory

from magnetovis.Objects import Axis # Allow import magnetovis as mvs; mvs.Axis(...)
from magnetovis.Objects.Axis import Script, ScriptRequestInformation, OutputDataSetType, Display
file = "Axis"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "displayFunction": Display,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Objects import Curve # Allow import magnetovis as mvs; mvs.Curve(...)
from magnetovis.Objects.Curve import Script, ScriptRequestInformation, OutputDataSetType, Display
file = "Curve"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "displayFunction": Display,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Objects import Lines # Allow import magnetovis as mvs; mvs.Lines(...)
from magnetovis.Objects.Lines import Script, ScriptRequestInformation, OutputDataSetType, Display
file = "Lines"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "displayFunction": Display,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Objects import Satellite # Allow import magnetovis as mvs; mvs.Satellite(...)
from magnetovis.Objects.Satellite import Script, ScriptRequestInformation, OutputDataSetType, Display
file = "Satellite"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "displayFunction": Display,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Objects import Plane # Allow import magnetovis as mvs; mvs.Plane(...)
from magnetovis.Objects.Plane import Script, ScriptRequestInformation, OutputDataSetType, Display
file = "Plane"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "displayFunction": Display,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Objects import StructuredGrid # Allow import magnetovis as mvs; mvs.StructuredGrid(...)
from magnetovis.Objects.StructuredGrid import Script, ScriptRequestInformation, OutputDataSetType, Display
file = "StructuredGrid"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "displayFunction": Display,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp


