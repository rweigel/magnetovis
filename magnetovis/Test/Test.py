# Execute using
#   magnetovis test

import os
import magnetovis as mvs

#dirs = ["Demos", "Sources"]
#dirs = ["Demos"]
#dirs = ["Sources", "Filters", "Plugins/demos","Demos"]
#dirs = ["Sources","Plugins/demos"]
dirs = ["Sources","Plugins/demos", "Filters","Demos"]
#dirs = ["Plugins/demos"]
testonly = []
#testonly = ["Rotate_demo.py", "Axis_demo.py"]
#testonly = ["GridData_demo.py"]
#testonly = ["GridData_demo.py"]
#excludes = []
excludes = ["BATSRUS_demo.py", "BATSRUS_dB_demo.py", "MySource_demo.py", "MyFilter_demo.py"]
#excludes = ["BATSRUS_demo.py", "MySource_demo.py", "MyFilter_demo.py"]

ImageResolution = [1920, 1080]

md_file = os.path.dirname(os.path.abspath(mvs.__file__))
md_file = os.path.join(md_file, "Test/README.md")
if os.path.exists(md_file):
    os.remove(md_file)
md_fh = open(md_file, "a")

def splitscript(demo_script):

  import re
  starts = []
  for match in re.finditer("# Demo ", demo_script):
      starts.append(match.start())

  if len(starts) == 1:
    return [demo_script]

  parts = []
  for idx in range(len(starts)-1):
      parts.append(demo_script[starts[idx]:starts[idx+1]])
  parts.append(demo_script[starts[idx+1]:]) 

  return parts

for dir in dirs:

  base = os.path.dirname(os.path.abspath(mvs.__file__))
  base = base + "/" + dir

  base2 = os.path.dirname(os.path.abspath(mvs.__file__))
  base2 = os.path.join(base2, "Test")

  mvs.logger.info("Reading " + base)

  ls = os.listdir(base)
  files_py = []
  for entry in ls:
    if entry.endswith("_demo.py") and entry not in excludes:
        if len(testonly) == 0:
          files_py.append(entry)
        else:
          if entry in testonly:
            files_py.append(entry)

  files_py.sort()

  for file_py in files_py:

    file_py_abspath = base + "/" + file_py

    demo_script = open(file_py_abspath, encoding='utf-8').read()

    fname = file_py.replace("_demo","")

    if dir.startswith("Plugins"):
      demo_type = "Plugin"
    if dir.startswith("Sources"):
      demo_type = "Source"
    if dir.startswith("Filters"):
      demo_type = "Filter"
    if dir.startswith("Demos"):
      demo_type = "Script"

    md_fh.write("## " + fname.replace(".py", "") + " (" + demo_type + ")\n\n")
    md_fh.write(f"Source file: [{fname}](https://github.com/rweigel/magnetovis/tree/main/magnetovis/{dir}/{fname}) | ")
    md_fh.write(f"Demo file: [{file_py}](https://github.com/rweigel/magnetovis/tree/main/magnetovis/{dir}/{file_py})\n\n")

    import paraview.simple as pvs
    #print("------")
    #print(pvs.GetRenderViews())
    #print("------")

    mvs.logger.info("Executing " + file_py_abspath)
    exec(demo_script)
    mvs.logger.info("Executed " + file_py_abspath)

    #print("++++++")
    #print(pvs.GetRenderViews())
    #print("++++++")

    if True:
      script_parts = splitscript(demo_script)
      #print(script_parts)

      rvs = pvs.GetRenderViews()
      for idx, renderView in enumerate(rvs):
        file_png = dir + "/" + file_py[0:-3] + "-" + str(idx+1) + '.png'

        if idx > len(script_parts)-1:
          print("---------------------- Warning -----------------------")
          print("------ Number of renderViews != number of demos. -----")
          print("------------------------------------------------------")
          # This has been observed to happen when a (redundant) Show() is executed
          # after the call to create the object in Plugins/GridData_demo.py.
        else:
          md_fh.write("### Demo " + str(idx+1) + "\n\n")
          md_fh.write("```python\n" + script_parts[idx] + "\n```\n\n")
          md_fh.write("![" + file_py + "](" + "__BASE_DIR__" + file_png + ")\n\n")

        file_png = base2 + "/" + file_png

        # Next line is important. See
        # https://discourse.paraview.org/t/legend-fonts-get-messed-up-saving-screenshot-using-pvpython/3954
        renderView.ViewSize = ImageResolution

        dir_png, _ = os.path.split(file_png)
        if not os.path.exists(dir_png):
          mvs.logger.info("Created " + dir_png)
          os.makedirs(dir_png)

        mvs.logger.info("Writing " + file_png)

        pvs.SaveScreenshot(file_png, renderView, ImageResolution=ImageResolution)
        mvs.logger.info("Wrote " + file_png)
        layout = pvs.GetLayout(view=renderView)
        pvs.Delete(layout)
        del layout
        pvs.Delete(renderView)
        del renderView

        #print("x-----")
        #print(pvs.GetRenderViews())
        #print("x-----")

      for source in pvs.GetSources().values():
        pvs.Delete(source)
        del source


    #print("000000")
    #print(pvs.GetRenderViews())
    #print("000000")

md_fh.close()
print("Wrote: " + md_file)

md_file_string = open(md_file, encoding='utf-8').read()
with open(md_file, 'w', encoding='utf-8') as f:
  print("Setting paths in " + md_file)
  f.write(md_file_string.replace("__BASE_DIR__",""))

if len(testonly) == 0:
  base = os.path.dirname(os.path.abspath(mvs.__file__))
  readme = open(os.path.join(base, "..", "README.md"), encoding='utf-8').read()

  with open(os.path.join(base, "..", "README.md.last"), 'w', encoding='utf-8') as f:
    f.write(readme)

  comment_str = "<!-- Demos Start -->"
  readme_split = readme.split(comment_str)
  readme_split[1] = comment_str + "\n" + readme.replace("__BASE_DIR__","magnetovis/Test/")

  with open(os.path.join(base, "..", "README.md"), 'w', encoding='utf-8') as f:
    f.write(readme_split[0] + readme_split[1])
  print("Updated " + os.path.join(base, "..", "README.md"))

