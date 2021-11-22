def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkStructuredGrid"


def ScriptRequestInformation(self, dimensions=[3,3,3]):

    # What is entered in the Script (RequestInformation) box for a Programmable Source
    # For vtkStructuredGrid this is needed. See
    # https://discourse.paraview.org/t/problem-displaying-structured-grid-when-loading-from-programmable-source/3051/2

    import logging
    logging.info("dimensions = [{}, {}, {}]".format(dimensions[0], dimensions[1], dimensions[2]))
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    outInfo.Set(executive.WHOLE_EXTENT(), 0, dimensions[0]-1, 0, dimensions[1]-1, 0, dimensions[2]-1)


def Script(time="2001-01-01T00:00:00", coord_sys='GSM', dimensions=[2, 2, 2],
            point_function="linspace(starts=(0., 0., 0.), stops=(1., 1., 1.))",
            point_array_functions=["xyz: position()", "abc: dipole()"]):

    assert isinstance(point_array_functions, list), "point_array_functions must be a list"
    assert isinstance(point_function, str), "point_function must be a str"

    # What is entered in the Script box for a Programmable Source
    
    import vtk
    import logging
    import numpy as np
    import magnetovis
    from magnetovis.vtk.set_arrays import set_arrays
    from magnetovis.vtk.get_arrays import get_arrays
    from magnetovis.vtk.set_points import set_points
    from magnetovis.util import iso2ints

    # Calls point function, with arg[0] of dimensions, e.g.,
    # linspace(dimensions, starts=(0., 0., 0.), stops=(1., 1., 1.))
    points = get_arrays(point_function, dimensions)

    if coord_sys != 'GSM':
        from hxform import hxform as hx
        assert time != None, 'If coord_sys in not GSM, time cannot be None'
        points = hx.transform(points, iso2ints(time), 'GSM', coord_sys, 'car', 'car')

    # For StructuredGrid this is needed.
    output.SetExtent([0, dimensions[0]-1, 0, dimensions[1]-1, 0, dimensions[1]-1])

    point_arrays = get_arrays(point_array_functions, points)
    set_points(output, points)
    set_arrays(output, point_data=point_arrays)
    magnetovis.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())


def DefaultRegistrationName(**kwargs):
    import magnetovis as mvs

    registrationName = "Structured Grid/{}/{}" \
                        .format(mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

    return registrationName


def SetDisplayProperties(programmableSource, renderView=None, displayProperties=None, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import logging
    import paraview.simple as pvs

    import magnetovis as mvs

    mvs.ColorByCellId(programmableSource, renderView=renderView, displayProperties=displayProperties)

    renderView.ResetCamera()

    camera = mvs.SetCamera(renderView=renderView, source=programmableSource, viewType="isometric")

    sourceOptions = programmableSource.ListProperties()

    #print(sourceOptions)
    #print(programmableSource.GetProperty('coord_sys'))

    if 'showTitle' in displayArguments and displayArguments['showTitle'] == True:
        info = mvs.ProxyInfo.GetInfo(programmableSource, origin='server')
        print(info)
        info = mvs.ProxyInfo.GetInfo(programmableSource)
        print(info)
        registrationName = info['registrationName']
        logging.info("registrationName = " + registrationName)
        title = pvs.Text(registrationName="   Title")
        title.Text = registrationName

        if renderView is None:
            renderView = pvs.GetActiveViewOrCreate('RenderView')
        pvs.Show(title, renderView)

    pvs.SetActiveSource(programmableSource)
