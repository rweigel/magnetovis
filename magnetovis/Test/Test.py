import os

base = os.path.dirname(os.path.abspath(__file__))
base = base + "/../Demos"

print("Reading " + base)

ls = os.listdir(base)
files_py = []
for entry in ls:
    if entry.endswith(".py"):
        files_py.append(entry)
#print(files_py)
files_py.sort()

import paraview.simple as pvs

# The commented out lines cause random crashes.
# No crashes when pvs.Delete() loop is used.
#pvs.Disconnect()

for file_py in files_py:
    file_png = base + "/Figures/" + file_py[0:-3] + '.png'
    file_py = base + "/" + file_py
    #print("Connecting", flush=True)
    #pvs.Connect()
    #print("Connected", flush=True)
    print("Executing " + file_py, flush=True)
    exec(open(file_py).read())
    print("Executed " + file_py, flush=True)
    renderView1 = pvs.GetActiveViewOrCreate('RenderView')
    #renderView1.Update()
    pvs.ResetCamera()
    print(renderView1)
    print("Writing " + file_png, flush=True)
    pvs.SaveScreenshot(file_png, renderView1, ImageResolution=[1024, 768], TransparentBackground=1, FontScaling="Do not scale fonts")
    print("Wrote " + file_png, flush=True)
    #pvs.ResetSession()
    for view in pvs.GetRenderViews():
        pvs.Delete(view)
    try:
        print("Disconnecting", flush=True)
        #pvs.Disconnect()
        print("Disconnected", flush=True)
    except:
        print("Disconnect failed.", flush=True)
        pass
