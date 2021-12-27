def get_arrays(functions, points, **kwargs):

    debug = False

    import magnetovis as mvs
    mvs.logger.info("Called with functions = {}".format(functions))

    from magnetovis.functions import functions as mvsfunctions
    from magnetovis.extract import extract_kwargs

    if functions is None:
        return None
    
    functions_was_string = False
    if isinstance(functions, str):
        functions_was_string = True
        functions = [functions]

    data_dict = {}
    array_names = []
    for function in functions:
        function_split = function.split(":")
        if len(function_split) == 1:
            array_name_given = None
            function_call = function_split[0]
            kwargs = extract_kwargs(function_call)
        else:
            array_name_given = function_split[0]
            # TODO: Handle duplicate name case
            function_call = function_split[1]
            kwargs = {}

        function_split2 = function_call.split("(")

        if debug: 
            print("get_arrays(): function_split = " + str(function_split))
            print("get_arrays(): array_name_given = " + str(array_name_given))
            print("get_arrays(): function_call = " + function_call)
            print("get_arrays(): function_split2 = " + str(function_split2))

        function_name = function_split2[0].lstrip()
        if array_name_given is None:
            array_name = function_name
        else:
            array_name = array_name_given

        assert array_name not in array_names, "Duplicate array name " + array_name
        array_names.append(array_name)

        if debug:
            if len(function_split2) == 1:
                print("get_arrays(): Calling " + function_name + "(points)")
            else:
                function_kwargs = function_split2[1]
                print("get_arrays(): Calling " + function_name + "(points, " + function_kwargs)

        # Call the function
        data = getattr(mvsfunctions, function_name)(points, **kwargs)
        data_dict[array_name] = data

    if functions_was_string == 1 and array_name_given is None:
        return data_dict[array_name]
    else:
        return data_dict


if False:

    import numpy as np
    print(get_arrays(["dipole(M=1)"], np.ones((1,3))))

    print(get_arrays("dipole", np.ones((1,3))))
    print(get_arrays("dipole()", np.ones((1,3))))
    print(get_arrays("dipole(M=1)", np.ones((1,3))))

    print(get_arrays("d: dipole", np.ones((1,3))))
    print(get_arrays("d: dipole()", np.ones((1,3))))
    print(get_arrays("d: dipole(M=1)", np.ones((1,3))))

    print(get_arrays(["d1: dipole", "d2: dipole(M=1)"], np.ones((1,3))))
