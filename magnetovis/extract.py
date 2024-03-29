def extract_function_call(function, xml_encode=False):

    from magnetovis.functions import functions as mvsfunctions

    import magnetovis as mvs
    mvs.logger.info("Called.")

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
    """Extract keyword arguments given string or function reference

    kwargs = extract_kwargs(function, default_kwargs=None)
    
    function is string:
    -------------------
        If the magnetovis.functions.circle is a function with signature
        def circle(N, radius=1):

        extract_kwargs("magnetovis.functions.circle")
                    => {'radius': 1}

        magnetovis.functions may be omitted if the function is in that module:

        extract_kwargs("circle")
                    => {'radius': 1}

        extract_kwargs("circle(a, radius=2)")
                    => {'radius': 2}

        extract_kwargs("circle(a, radius=2)", default_kwargs={'radius': 3})
                    => {'radius': 3}


    function is function pointer:
    -----------------------------
    If a function `circle` is defined according to

        def circle(N, radius=2, center=[0, 0, 0]): pass

    then

        extract_kwargs(circle)
            => {"radius": 2, "center": [0, 0, 0]}

        extract_kwargs(circle, default_kwargs={"radius": 3})
            => {"radius": 3, "center": [0, 0, 0]}


    function is string and function not in magnetovis.functions 
    -----------------------------------------------------------
        In this case, the string is parsed

        extract_kwargs("abc")
                    => {}

        extract_kwargs("abc()")
                    => {}

        extract_kwargs("abc(radius=1)")
                    => {"radius": 1}

        extract_kwargs("abc", default_kwargs={"radius": 2}) 
                    => {"radius": 2}

        extract_kwargs("abc(radius=1)", default_kwargs={"radius": 2}) 
                    => {"radius": 2}

        extract_kwargs("abc(radius=1)", default_kwargs={"radius": 2, "ignored": -1}) 
                    => {"radius": 2}



    """

    import types
    import importlib
    from inspect import signature, Parameter

    import magnetovis as mvs

    mvs.logger.info("Called with function = {} and default kwargs of {}".format(function, default_kwargs))

    if isinstance(function, str):
        # e.g., function = "circle(radius=1, center=[0, 0, 0])"
        # https://stackoverflow.com/questions/2626582/running-exec-inside-function
        function_call_parts = function.split("(")
        if len(function_call_parts) == 1:
            # e.g.,
            #   magnetovis.Sources.StructuredGrid.Script
            # or
            #   circle
            if not function.startswith("magnetovis"):
                # e.g., circle
                function = "magnetovis.functions." + function

            module = ".".join(function.split(".")[0:-1])
            function = function.split(".")[-1]

            try:
                module = importlib.import_module(module)
                function = getattr(module, function)
                return extract_kwargs(function, default_kwargs=default_kwargs)
            except:
                return extract_kwargs(function + "()", default_kwargs=default_kwargs)

        function_call_parts[0] = "function_pointer"
        function_call = '('.join(function_call_parts)
        function_def = "def " + function_call + ": pass"
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

    if 'output' in kwargs:
      del kwargs['output']
    if 'inputs' in kwargs:
      del kwargs['inputs']

    mvs.logger.info("Returning kwargs of {}".format(kwargs))

    return kwargs


def test_extract_kwargs():

    assert extract_kwargs("abc") == {}
    assert extract_kwargs("abc()") == {}
    assert extract_kwargs("abc(a, b=1)") == {'b': 1}
    assert extract_kwargs("abc(a, b=1)", default_kwargs={'b': 2}) == {'b': 2}
    assert extract_kwargs("abc(a, b=1)", default_kwargs={'b': 2, 'c': 2}) == {'b': 2}
    assert extract_kwargs("abc(a, b=1, c=2)") == {'b': 1, 'c': 2}
    assert extract_kwargs("abc(a, b=1, c=2)", default_kwargs={'b': 2, 'c': 3}) == {'b': 2, 'c': 3}

    def check_circle():
        assert extract_kwargs("magnetovis.extract.__circle()") == {}
        assert extract_kwargs("magnetovis.extract.__circle") == {'radius': 1, 'center': (0, 0, 0)}
        assert extract_kwargs("magnetovis.extract.__circle", default_kwargs={'radius': 2}) == {'radius': 2, 'center': (0, 0, 0)}
        assert extract_kwargs("magnetovis.extract.__circle(N, radius=3)") == {'radius': 3}

    from magnetovis import extract
    def __circle(N, radius=1, center=(0, 0, 0)): pass
    # The following is equivalent to putting the above def outside of this function.
    setattr(extract, "__circle", __circle)
    check_circle()

    from magnetovis import functions
    # The following is equivalent to putting the above def in functions.py
    setattr(functions, "__circle", __circle)
    check_circle()

    def __circle(N, radius=1,
                center=(0, 0, 0)):
        pass
    setattr(functions, "__circle", __circle)
    check_circle()


def extract_script(function, sourceArguments, xml_encode=False):

    debug = False

    import inspect
    import magnetovis as mvs

    mvs.logger.info("Called with function = {}".format(function))

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

         if found_def_start is True and found_def_end == False and line.endswith(":"):
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

    return script, kwargs


if __name__ == "__main__":
    test_extract_kwargs()

