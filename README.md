# Install

## User

A PyPi package is not yet available. To install, use

```
pip install 'git+https://github.com/rweigel/magnetovis' --upgrade
```

## Developer

```
git clone https://github.com/rweigel/magnetovis
pip install --editable .
```

# Use

```
magnetovis --script=magnetovis_demo.py
```

# Notes

See `docs/Region_Notes.md` for documentation on how magnetosphere regions were computed.

Creating VTK objects with Python
* https://stackoverflow.com/questions/59273490/python-read-vtk-file-add-data-set-then-write-vtk
* https://blog.kitware.com/improved-vtk-numpy-integration/