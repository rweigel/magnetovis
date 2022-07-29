def ClearPipeline():

    import paraview.simple as pvs
    [pvs.Delete(s) for s in pvs.GetSources().values()]
