import magnetovis as mvs
import paraview.simple as pvs

kwargs = {
            "time": "2001-01-01T00:00:00",
            "coord_sys": "GSM",
            "point_function": "linspace(starts=(-1, -1, -1), stops=(1, 1, 1))",
            "dimensions": [3, 3, 3],
            "point_array_functions": ["dipole1: dipole(M=2)", "xyz1: position()"]
        }

kwargs["registrationName"] = "Structured Grid/{}/{}".format(mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

MagnetovisStructuredGrid1 = pvs.MagnetovisStructuredGrid(**kwargs)
displayProperties = mvs.SetDefaultDisplayProperties(MagnetovisStructuredGrid1)



def UpdateDisplayOptions(caller, event):
    import magnetovis as mvs
    import paraview.simple as pvs
    #print("Event: " + event)
    # TODO: Figure out how to get source out of caller object (which is a SMSourceProxy).
    #source = pvs.GetActiveSource()
    #source.RemoveObserver('UpdateInformationEvent')
    #mvs.SetDefaultDisplayProperties(pvs.GetActiveSource())

#MagnetovisStructuredGrid1.AddObserver('UpdateInformationEvent', UpdateDisplayOptions)
