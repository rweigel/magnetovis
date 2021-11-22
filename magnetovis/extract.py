def extract_function_call(function, xml_encode=False):

    from magnetovis.functions import functions as mvsfunctions

    if isinstance(function, str):
        function = getattr(mvsfunctions, function)

    kwargs = extract_kwargs(function)

    call_str = function.__name__ + "("
    for key in kwargs:
        if isinstance(kwargs[key], str):
            call_str = call_str + '{} = "{}", '.format(key, kwargs[key])
        else:
            call_str = call_str + '{} = {}, '.format(key, kwargs[key])

    call_str = call_str[0:-2] + ")"

    if xml_encode is True:
        call_str = call_str.replace("\n","&#xa;").replace("'","&#39;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")

    return call_str

def extract_kwargs(function, default_kwargs=None):

    import types
    from inspect import signature, Parameter

    kwargs = {}
    if isinstance(function, str):
        # e.g., function = "circle(radius=1, center=[0, 0, 0])"
        # https://stackoverflow.com/questions/2626582/running-exec-inside-function
        function_call_parts = function.split("(")
        if len(function_call_parts) == 1:
            return {}
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
            continue

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

if False:
    def myfun(a, b=1,
        c=2):
        abc = 1
    print(extract_script(myfun,[]))