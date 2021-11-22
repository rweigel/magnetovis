def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkRectilinearGrid"


def ScriptRequestInformation(self, dimensions=[3,3,3]):

    # What is entered in the Script (RequestInformation) box for a Programmable Source
    import logging
    logging.info("dimensions = [{}, {}, {}]".format(dimensions[0], dimensions[1], dimensions[2]))
    # For vtkStructuredGrid this is needed. See
    # https://discourse.paraview.org/t/problem-displaying-structured-grid-when-loading-from-programmable-source/3051/2
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    outInfo.Set(executive.WHOLE_EXTENT(), 0, dimensions[0]-1, 0, dimensions[1]-1, 0, dimensions[2]-1)


def Script(time="2001-01-01", coord_sys='GSM', dimensions=[3, 3, 3], point_function="linspace", point_array_functions=["xyz: position()" , "abc: dipole()"]):

    # What is entered in the Script box for a Programmable Source
    
    import vtk
    import logging
    import numpy as np
    from magnetovis.vtk.set_arrays import set_arrays
    from magnetovis.vtk.get_arrays import get_arrays
    from magnetovis.vtk.set_points import set_points
    from magnetovis.util import iso2ints

    points = get_arrays(point_function, dimensions)

    if coord_sys != 'GSM':
        from hxform import hxform as hx
        assert time != None, 'If coord_sys in not GSM, time cannot be None'
        points = hx.transform(points, iso2ints(time), 'GSM', coord_sys, 'car', 'car')

    point_arrays = get_arrays(point_array_functions, points)
    #cell_arrays = get_arrays(cell_array_functions, cell_centers)

    output.SetExtent([0, dimensions[0]-1, 0, dimensions[1]-1, 0, dimensions[1]-1])

    set_points(self, output, points, dimensions=dimensions, grid_type='rectilinear')
    set_arrays(self, output, points, point_data=point_arrays)


def SetDisplayProperties(programmableSource, renderView=None, displayProperties=None, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import logging
    import paraview.simple as pvs
    import magnetovis as mvs

    mvs.ColorByCellId(programmableSource, renderView=renderView, displayProperties=displayProperties)

    renderView.ResetCamera()    

    camera = mvs.SetCamera(renderView=renderView, source=programmableSource, viewType="isometric")

    # TODO: Is there an easier way to get the registration Name?! 
    # https://public.kitware.com/pipermail/paraview/2017-January/038962.html
    registrationName = list(pvs.GetSources().keys())[list(pvs.GetSources().values()).index(pvs.GetActiveSource())][0]
    logging.info("registrationName = " + registrationName)

    # To access the kwargs used to create the programmableSource:
    #sourceOptions = programmableSource.ListProperties()
    #print(sourceOptions)
    #print(programmableSource.GetProperty('coord_sys'))

    title = pvs.Text(registrationName="   Title")
    title.Text = registrationName

    if renderView is None:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    pvs.Show(title, renderView)

    pvs.SetActiveSource(programmableSource)
