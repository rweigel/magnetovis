import magnetovis as mvs

kwargs = {
        "time": "2001-01-01",
        "coord_sys": "GSM",
        "point_function": "linspace()",
        "point_array_functions": ["dipole(M=2)"],
        "dimensions": [4, 3, 3]
    }

registrationName = "Dipole on Rectilinear Grid/{}/{}".format(mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

kwargs["registrationName"] = registrationName
MagnetovisRectilinearGrid1 = mvs.RectilinearGrid(**kwargs)
displayProperties = mvs.SetDisplayProperties(MagnetovisRectilinearGrid1)
