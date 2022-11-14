# Execute using
#   magnetovis test

import os
import magnetovis as mvs

dirs = ["Demos", "Sources"]
#dirs = ["Sources", "Filters", "Plugins"]
testonly = []
#testonly = ["Rotate_demo.py", "Axis_demo.py"]
#testonly = ["GridData_demo.py"]
excludes = []
#excludes = ["BATSRUS_demo.py", "BATSRUS_dB_demo.py", "MySource_demo.py", "MyFilter_demo.py"]
excludes = ["BATSRUS_demo.py", "MySource_demo.py", "MyFilter_demo.py"]

ImageResolution = [1920, 1080]

if len(testonly) == 0:
    md_file = os.path.dirname(os.path.abspath(mvs.__file__))
    md_file = os.path.join(md_file, "Test/README.md")
    if os.path.exists(md_file):
        os.remove(md_file)
    f = open(md_file, "a")

for dir in dirs:

  base = os.path.dirname(os.path.abspath(mvs.__file__))
  base = base + "/" + dir

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

  import paraview.simple as pvs

  base2 = os.path.dirname(os.path.abspath(mvs.__file__))
  base2 = os.path.join(base2, "Test")
  for file_py in files_py:

    file_py_abspath = base + "/" + file_py

    demo_script = open(file_py_abspath, encoding='utf-8').read()

    if len(testonly) == 0:
      fname = file_py.replace("_demo","")
      f.write("## " + fname.replace(".py", "") + "\n\n")
      f.write(f"Source file: [{fname}](https://github.com/rweigel/magnetovis/tree/main/magnetovis/{dir}/{fname}) | ")
      f.write(f"Demo file: [{file_py}](https://github.com/rweigel/magnetovis/tree/main/magnetovis/{dir}/{file_py})\n\n")

    mvs.logger.info("Executing " + file_py_abspath)
    exec(demo_script)
    mvs.logger.info("Executed " + file_py_abspath)

    if len(testonly) == 0:
        import re
        script_parts = re.split("# Demo", demo_script)

    # Loop over layouts
    for idx, renderView in enumerate(pvs.GetRenderViews()):

      file_png = dir + "/" + file_py[0:-3] + "-" + str(idx+1) + '.png'

      if len(testonly) == 0:
        body = script_parts[idx+1].split("\n")
        head = body[0].strip()
        script = "\n".join(body[1:]).strip()
        f.write("### Demo " + head + "\n\n")
        f.write("```python\n" + script + "\n```\n\n")
        f.write("![" + file_py + "](" + "magnetovis/Test/" + file_png + ")\n\n")

      file_png = base2 + "/" + file_png

      # Next line is important. See
      # https://discourse.paraview.org/t/legend-fonts-get-messed-up-saving-screenshot-using-pvpython/3954
      renderView.ViewSize = ImageResolution

      mvs.logger.info("Writing " + file_png)

      pvs.SaveScreenshot(file_png, renderView, ImageResolution=ImageResolution)
      mvs.logger.info("Wrote " + file_png)
      layout = pvs.GetLayout(view=renderView)
      pvs.Delete(layout)
      pvs.Delete(renderView)
      del layout
      del renderView

    for source in pvs.GetSources().values():
      pvs.Delete(source)

if len(testonly) == 0:
  f.close()
  base = os.path.dirname(os.path.abspath(mvs.__file__))
  readme = open(os.path.join(base, "..", "README.md"), encoding='utf-8').read()
  gallery = open(os.path.join(base, "Test", "README.md"), encoding='utf-8').read()

  comment_str = "<!-- Demos Start -->"
  readme_split = readme.split(comment_str)
  readme_split[1] = comment_str + "\n" + gallery

  with open(os.path.join(base, "..", "README.md.last"), 'w', encoding='utf-8') as f:
    f.write(readme)

  with open(os.path.join(base, "..", "README.md"), 'w', encoding='utf-8') as f:
    f.write(readme_split[0] + readme_split[1])
