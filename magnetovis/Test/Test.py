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
testonly = ["Axis_demo.py"]

#FontScaling = "Do not scale fonts"
FontScaling = "Scale fonts proportionally"
ImageResolution = [1920, 1080]

for dir in dirs:
    base = os.path.dirname(os.path.abspath(mvs.__file__))
    base = base + "/" + dir

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

    files_py.sort()

    import paraview.simple as pvs

    md_file = os.path.dirname(os.path.abspath(mvs.__file__))
    md_file = os.path.join(md_file,"Test/README.md")
    if os.path.exists(md_file):
        os.remove(md_file)
    f = open(md_file, "a")

    base2 = os.path.dirname(os.path.abspath(mvs.__file__))
    base2 = os.path.join(base2, "Test")
    for file_py in files_py:
        file_py_abspath = base + "/" + file_py
        mvs.logger.info("Executing " + file_py_abspath)
        demo_script = open(file_py_abspath).read()
        f.write("# " + file_py + "\n")
        f.write("```\n" + demo_script + "\n```\n")
        exec(demo_script)
        mvs.logger.info("Executed " + file_py_abspath)

        # See https://gitlab.kitware.com/paraview/paraview/-/issues/21109
        # for issues with font sizes not matching that on screen.
        for idx, renderView in enumerate(pvs.GetRenderViews()):
            file_png = "Figures/" + file_py[0:-3] + "-" + str(idx+1) + '.png'
            f.write("![" + file_py + "](" + file_png + ")\n")
            file_png = base2 + "/" + file_png

            mvs.logger.info("Writing " + file_png)
            pvs.Render(renderView)
            #pvs.SaveScreenshot(file_png, renderView,
            #    FontScaling=FontScaling, ImageResolution=ImageResolution)
            pvs.SaveScreenshot(file_png, renderView, ImageResolution=ImageResolution)
            mvs.logger.info("Wrote " + file_png)
            layout = pvs.GetLayout(view=renderView)
            pvs.Delete(layout)
            pvs.Delete(renderView)

        for source in pvs.GetSources().values():
            pvs.Delete(source)
        #del layout
        #del source
        #del renderView
 
    f.close()

