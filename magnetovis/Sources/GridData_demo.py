# Execute using
#    magnetovis --script=GridData_demo.py
import magnetovis as mvs

"""
Demo #1
"""

mvs.GridData(OutputDataSetType="vtkImageData")

"""
Demo #2
"""
mvs.CreateViewAndLayout()
mvs.GridData(OutputDataSetType="vtkRectilinearGrid")

"""
Demo #3
"""

mvs.CreateViewAndLayout()
mvs.GridData(OutputDataSetType="vtkStructuredGrid")

"""
Demo #4
"""

mvs.CreateViewAndLayout()

kwargs = {
        "time": "2001-01-01T00:00:00",
        "coord_sys": "GSM",
        "point_array_functions": ["dipole(M=2)"],
        "dimensions": [10, 10, 10]
    }

registrationName = "Dipole on Structured Grid/{}/{}" \
                    .format(mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])
kwargs["registrationName"] = registrationName

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
                            'Title': "$|\\mathbf{B}|$ [nT]",
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

mvs.SetDisplayProperties(**dkwargs)
mvs.SetCamera(Azimuth=225.0)
mvs.SetTitle(r"$\alpha$/β", title=registrationName)

tkwargs = {
            "registrationName": "",
            "display": {
                "FontSize": 22,
                "Color": [1, 1, 0],
                "Visibility": 1
            }
        }
