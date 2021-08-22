def exec_programmable_source(file, **kwargs):
  """Execute file using kwargs

  Execute a script that sets a local variable kwargs and then
  executes the given file. The file that is executed calls the
  function that creates a programmable source using the given kwargs.
  """

  import os
  import sys
  import paraview.simple as pvs

  file = os.path.join(os.getcwd(), file)

  # Create a new Programmable Source
  programmableSource1 = pvs.ProgrammableSource()

  if sys.version_info[0] < 3:
    # Python 2.
    programmableSource1.Script = "kwargs="+str(kwargs)+"\nexecfile('" + file + "',globals(),locals())"
  else:
    # Python 3.
    programmableSource1.Script = "kwargs="+str(kwargs)+"\nexec(open('" + file + "').read())"

  # Get active view
  renderView1 = pvs.GetActiveViewOrCreate('RenderView')

  # Show data in view
  programmableSource1Display = pvs.Show(programmableSource1, renderView1)

  # Trace defaults for the display properties.
  programmableSource1Display.Representation = 'Surface'

  # Update the view to ensure updated data information
  renderView1.Update()
