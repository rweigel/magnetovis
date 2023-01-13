url = 'http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000.vtk'
vtkfile = "/tmp/" + url.split("/")[-1]

import os
if not os.path.exists(vtkfile):
  from urllib.request import urlretrieve
  print("Downloading " + url, flush=True)
  urlretrieve(url, vtkfile)

if False:
    # If a VTK file does not exist, create it using the following.
    url = 'http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000'
    vtkfile = "/tmp/" + url.split("/")[-1]
    import os
    if not os.path.exists(vtkfile):
      try:
        import swmfio
      except:
        print('\n\nInstall swmfio using')
        print('pip install "swmfio@git+https://github.com/GaryQ-physics/swmfio@main#egg=swmfio"\n')
        raise ModuleNotFoundError("Package swmfio must be installed.")

      import logging
      swmfio.logger.setLevel(logging.INFO)
      filebase = swmfio.dlfile(url, progress=True)
      vtkfile = swmfio.write_vtk(filebase)

