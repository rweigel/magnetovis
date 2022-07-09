# From magnetovis root directory, execute
#   magnetovis pvbatch magnetovis/Test/Test.py 

import os
import magnetovis as mvs

#dirs = ["Demos", "Sources"]
dirs = ["Sources"]
testonly = []
#testonly = ["Axis_demo.py", "Grid_demo.py"]
#testonly = ["Lines_demo.py","StructuredGrid_demo.py"]
#testonly = ["Axis_demo.py", "Curve_demo.py", "StructuredGrid_demo.py", "Satellite_demo.py"]
#testonly = ["Axis_demo.py"]

# https://gitlab.kitware.com/paraview/paraview/-/issues/21459
for dir in dirs:
    base = os.path.dirname(os.path.abspath(__file__))
    base = base + "/../" + dir

    mvs.logger.info("Reading " + base)

    ls = os.listdir(base)
    files_py = []
    for entry in ls:
        if entry.endswith("_demo.py"):
            if len(testonly) == 0:
                files_py.append(entry)
            else:
                if entry in testonly:
                    files_py.append(entry)

    #print(files_py)
    files_py.sort()

    import paraview.simple as pvs

    #pvs.Connect("localhost")
    #[pvs.Delete(s) for s in pvs.GetSources().values()]
    #pvs.ResetSession()

    for file_py in files_py:
        file_py_abspath = base + "/" + file_py
        #print("Connecting", flush=True)
        #pvs.Connect()
        #print("Connected", flush=True)
        mvs.logger.info("Executing " + file_py_abspath)
        exec(open(file_py_abspath).read())
        mvs.logger.info("Executed " + file_py_abspath)
        # See https://gitlab.kitware.com/paraview/paraview/-/issues/21109
        # for issues with font sizes not matching that on screen.
        for idx, renderView in enumerate(pvs.GetRenderViews()):
            file_png = base + "/Figures/" + file_py[0:-3] + "-" + str(idx+1) + '.png'
            mvs.logger.info("Writing " + file_png)
            pvs.Render(renderView)
            ImageResolution = [1368, 684]
            pvs.SaveScreenshot(file_png, renderView, ImageResolution=ImageResolution)
            mvs.logger.info("Wrote " + file_png)
            pvs.Delete(renderView)
            del renderView
            #pvs.Delete()

        # Reset session should not be needed.
        #pvs.ResetSession()

        if False:
            try:
                print("Disconnecting", flush=True)
                #pvs.Disconnect()
                print("Disconnected", flush=True)
            except:
                print("Disconnect failed.", flush=True)
                pass
