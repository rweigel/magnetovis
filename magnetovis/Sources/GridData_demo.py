# Execute using
#   magnetovis GridData_demo.py

"""
Demo #1
"""

import magnetovis as mvs
mvs.GridData(OutputDataSetType="vtkImageData")
mvs.SetTitle("Dataset Type = vtkImageData")

"""
Demo #2
"""

import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.GridData(OutputDataSetType="vtkRectilinearGrid")
mvs.SetTitle("Dataset Type = vtkRectilinearGrid")

"""
Demo #3
"""

import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.GridData(OutputDataSetType="vtkStructuredGrid")
mvs.SetTitle("Dataset Type = vtkStructuredGrid")

"""
Demo #4
"""

import magnetovis as mvs
mvs.CreateViewAndLayout()

kwargs = {
        "time": "2001-01-01T00:00:00",
        "coord_sys": "GSM",
        "dimensions": [4,4,4],
        "point_array_functions": [
                                "dipole()",
                                "radius()"
                            ],
        "cell_array_functions": [
                                "r: radius()"
                            ],
        "dimensions": [10, 10, 10]
    }

registrationName = "Dipole on Structured Grid/{}/{}" \
                    .format(mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])
kwargs["registrationName"] = registrationName

mvs.Axis(direction="X", extent=[0, 1.5], vtkTubeFilterSettings=['Radius: 0.02'])
mvs.Axis(direction="Y", extent=[0, 1.5], vtkTubeFilterSettings=['Radius: 0.02'])
mvs.Axis(direction="Z", extent=[0, 1.5], vtkTubeFilterSettings=['Radius: 0.02'])

sg2 = mvs.GridData(**kwargs)

dkwargs = {
        "display": {
            "Representation": "Surface With Edges",
            "Opacity": 1.0,
            "AmbientColor": [1, 1, 0],
            "DiffuseColor": [1, 1, 0],
            "Visibility": 1
        },
        'coloring': {
            'colorBy': ('POINTS', 'dipole'),
            'scalarBar': {
                            'Title': r"$\|\mathbf{B}\|$ [nT]",
                            'ComponentTitle': '',
                            'HorizontalTitle': 1,
                            'TitleJustification': 'Left',
                            'Visibility': 1,
                            'DrawNanAnnotation': 1,
                            'ScalarBarLength': 0.9
                        },
            'colorTransferFunction': {
                                        'UseLogScale': 1,
                                        'AutomaticRescaleRangeMode': 1,
                                        'AutomaticRescaleRangeMode': "Grow and update on 'Apply'",
                                        'NumberOfTableValues': 4
                                    }
        }
}

#mvs.SetViewProperties(view=None, **vkwargs)
mvs.SetDisplayProperties(**dkwargs)
#mvs.SetDisplayProperties(source=None, view=None, **dkwargs)
#mvs.SetColorProperties(source=None, *ckwargs)
#mvs.SetCameraProperties(view=None, camera=None, *ckwargs)
mvs.SetCamera(Azimuth=225.0)
mvs.SetTitle(r"$\alpha$/β", title=registrationName)
