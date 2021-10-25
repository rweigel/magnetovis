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

def extract_kwargs(function_call):

    # https://stackoverflow.com/questions/2626582/running-exec-inside-function
    function_call_parts = function_call.split("(")
    function_call_parts[0] = "function_pointer"
    function_call = '('.join(function_call_parts)
    function_def = "def " + function_call + ": pass"
    #print(function_def)
    exec_dict = {}
    exec(function_def, exec_dict)

    function_pointer = exec_dict["function_pointer"]
    #print(function_pointer)

    sourceArguments = None
    from inspect import signature, Parameter
    kwargs = {}
    for x, p in signature(function_pointer).parameters.items():
        if (p.default is not Parameter.empty) and p.kind == Parameter.POSITIONAL_OR_KEYWORD:
            kwargs[x] = p.default

    return kwargs

def extract_script(function, sourceArguments, xml_encode=False):

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

    if debug: print(function)

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

        self.displayArguments = displayArguments
        # Create display properties object
        self.displayProperties = pvs.Show(self.programmableSource, self.renderView)

        self.displayProperties = self.displayFunction(self.displayArguments)

        # Update the view to ensure updated data information
        # TODO: Needed?
        self.renderView.Update()

        if showSource == False:
            pvs.Hide(self.programmableSource, self.renderView)

        return self


def curve(Npts, coord_sys="GSM"):
    points = np.zeros((Npts,3))
    points[:,0] = np.arange(Npts)
    points[:,1] = np.zeros(Npts)
    points[:,2] = np.zeros(Npts)

    return points

def position(points, coord_sys="GSM"):
    return points

def radius(points):
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    return r

def IGRF(points, time="2001-01-01", coord_sys="GSM"):

    M=7.788E22
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    B = np.zeros(points.shape)
    r[r < 1] = np.nan
    B[:,0] = 3*M*points[:,0]*points[:,2]/r**5 # Bx = 3*M*x*z/r^5
    B[:,1] = 3*M*points[:,1]*points[:,2]/r**5 # By = 3*M*y*z/r^5
    B[:,2] = M*(3*points[:,2]**2-r**2)/r**5   # Bz = M(3*z^2 - r^2)/r^5

    return B

def T01(points, M=7.788E22, parmod=None, ps=0.0):

    import numpy as np
    r = np.linalg.norm(points, axis=1)
    B = np.zeros(points.shape)
    r[r < 1] = np.nan
    B[:,0] = 3*M*points[:,0]*points[:,2]/r**5 # Bx = 3*M*x*z/r^5
    B[:,1] = 3*M*points[:,1]*points[:,2]/r**5 # By = 3*M*y*z/r^5
    B[:,2] = M*(3*points[:,2]**2-r**2)/r**5   # Bz = M(3*z^2 - r^2)/r^5

    return B

def T89c(points, iopt=0, ps=0.0):

    import numpy as np
    from geopack.geopack import dip, recalc
    from geopack import t89

    ut = 100    # 1970-01-01/00:01:40 UT.

    ps = recalc(ut)
    print(ps)

    B = np.zeros(points.shape)
    for i in range(points.shape[0]):
        r = np.linalg.norm(points[i,:])
        if r < 1:
            B[i,0] = np.nan
            B[i,1] = np.nan
            B[i,2] = np.nan
        else:
            b0xgsm,b0ygsm,b0zgsm = dip(points[i,0], points[i,1], points[i,2])
            dbxgsm,dbygsm,dbzgsm = t89.t89(iopt, ps, points[i,0], points[i,1], points[i,2])
            B[i,0] = b0xgsm + dbxgsm
            B[i,1] = b0ygsm + dbygsm
            B[i,2] = b0zgsm + dbzgsm

    return B


def dipole(points, M=7.788E22):
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    B = np.zeros(points.shape)
    r[r < 1] = np.nan
    #r[r==0] = np.nan
    B[:,0] = 3*M*points[:,0]*points[:,2]/r**5 # Bx = 3*M*x*z/r^5
    B[:,1] = 3*M*points[:,1]*points[:,2]/r**5 # By = 3*M*y*z/r^5
    B[:,2] = M*(3*points[:,2]**2-r**2)/r**5   # Bz = M(3*z^2 - r^2)/r^5

    return B


# TODO: Automate the following by reading magnetovis/Objects directory

from magnetovis.Objects import Satellite # Allow import magnetovis as mvs; mvs.Satellite(...)
from magnetovis.Objects.Satellite import Script, ScriptRequestInformation, OutputDataSetType, _Display
file = "Satellite"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "displayFunction": _Display,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp


from magnetovis.Objects import Line # Allow import magnetovis as mvs; mvs.Line(...)
from magnetovis.Objects.Line import Script, ScriptRequestInformation, OutputDataSetType, _Display
file = "Line"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "displayFunction": _Display,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Objects import Axis # Allow import magnetovis as mvs; mvs.Axis(...)
from magnetovis.Objects.Axis import Script, ScriptRequestInformation, OutputDataSetType, _Display
file = "Axis"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "displayFunction": _Display,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp


from magnetovis.Objects import Plane # Allow import magnetovis as mvs; mvs.Plane(...)
from magnetovis.Objects.Plane import Script, ScriptRequestInformation, OutputDataSetType, _Display
file = "Plane"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "displayFunction": _Display,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Objects import StructuredGrid # Allow import magnetovis as mvs; mvs.StructuredGrid(...)
from magnetovis.Objects.StructuredGrid import Script, ScriptRequestInformation, OutputDataSetType, _Display
file = "StructuredGrid"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "displayFunction": _Display,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp

from magnetovis.Objects import MultiLine # Allow import magnetovis as mvs; mvs.MultiLine(...)
from magnetovis.Objects.MultiLine import Script, ScriptRequestInformation, OutputDataSetType, _Display
file = "MultiLine"
temp = type(file, (object, ), {
   "sourceFunction": Script,
   "sourceOutputDataSetType": OutputDataSetType(),
   "sourceRequestInformationFunction": ScriptRequestInformation,
   "displayFunction": _Display,
   "registrationName": file,
   "__init__": BaseClass.__init__,
   "SetDisplayOptions": BaseClass.SetDisplayOptions
})
globals()[file] = temp
