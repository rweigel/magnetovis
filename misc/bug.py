import paraview.simple as pvs

source = pvs.ProgrammableSource()
source.Script = "import numpy as np"

print(len(locals())) # 9
print(source) # <paraview.servermanager.ProgrammableSource object at 0x128d238b0>
pvs.Show(source)
print(source) # <function source at 0x12848e550>
print(len(locals())) # 638
print(hasnumpy) # True
