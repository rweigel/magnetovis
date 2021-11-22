# From this directory, execute
#   magnetovis --script=StructuredGrid.py

import paraview.simple as pvs
import magnetovis as mvs

kwargs = {
        "time": "2001-01-01T00:00:00",
        "coord_sys": "GSM",
        "point_function": "linspace()",
        "point_array_functions": ["dipole(M=2)"],
        "dimensions": [3, 3, 3]
    }

registrationName = "Dipole on Structured Grid/{}/{}" \
                    .format(mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])
kwargs["registrationName"] = registrationName

MagnetovisStructuredGrid1 = mvs.StructuredGrid(**kwargs)
displayProperties = mvs.SetDisplayProperties(MagnetovisStructuredGrid1, displayArguments={'showTitle': True})

if False:
    layout2 = pvs.CreateLayout(name='Layout #2')
    pvs.SetActiveView(None)
    renderView2 = pvs.CreateView('RenderView')
    pvs.AssignViewToLayout(view=renderView2, layout=layout2, hint=0)
    sphere1 = pvs.Sphere(registrationName='Sphere1')
    sphere1Display = pvs.Show(sphere1, renderView2, 'GeometryRepresentation')
    renderView2.ResetCamera()
