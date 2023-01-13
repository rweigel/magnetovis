import os
import glob
import importlib

# Each file here contains a single function. The following does
# the equivalent of, e.g.,
#   from .get_arrays import get_arrays
# for each .py file.
root = os.path.dirname(os.path.abspath(__file__))
files = glob.glob(os.path.join(root, "*.py"))
for file in files:
    file_name = os.path.basename(os.path.splitext(file)[0])
    # TODO: Do this with importlib instead of exec
    try:
        exec('from .' + file_name + " import " + file_name)
    except:
        pass # Demo or test file


del os
del glob
del importlib
del file_name
del files
del file
del root