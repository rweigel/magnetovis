import swmfio

import logging
swmfio.logger.setLevel(logging.INFO)

import os
import glob
#files = glob.glob('/Volumes/My Passport for Mac/git-data/dwelling/divB_simple1/GM/3d__*.out')
files = glob.glob('/Volumes/WDMyPassport5GB-1/git-data/Curtis/data/Brian_Curtis_042213_2/GM_CDF/3d__*.cdf')
for file in files:
    if os.path.exists(file + ".vtk"):
        print("Skipping " + file)
        continue
    batsclass = swmfio.read_batsrus(file)
    vtkfile = swmfio.write_vtk(batsclass)
