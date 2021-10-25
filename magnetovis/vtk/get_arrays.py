def get_arrays(array_functions, points):

    from magnetovis.functions import functions as mvsfunctions

    if array_functions is None:
        return None

    data_dict = {}
    for function, kwargs in array_functions.items():
        if 'array_name' in kwargs:
            name = kwargs['array_name']
            del kwargs['array_name']
        else:
            name = function
        # TODO: Handle duplicate name case
        # Call the function
        data = getattr(mvsfunctions, function)(points, **kwargs)
        print("get_arrays(): getting " + name)
        data_dict[name] = data

    return data_dict
