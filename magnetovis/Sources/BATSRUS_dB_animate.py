import glob
import imageio

import numpy as np

run_id = "divB_simple1"
run_id = "Brian_Curtis_042213_2"

var_left = 'dB'
var_right = 'j_phi'

if run_id == "divB_simple1":
    dir_left = '/Volumes/My Passport for Mac/git-data/dwelling/divB_simple1/GM/'
    dir_right = dir_left

if run_id == "DIPTSUR2":
    dir_left = '/Volumes/My Passport for Mac/git-data/sblake/DIPTSUR2/GM/IO2'
    dir_right = dir_left

if run_id == "Brian_Curtis_042213_2":
    dir_left = '/Volumes/WDMyPassport5GB-1/git-data/Curtis/data/Brian_Curtis_042213_2/GM_CDF'
    dir_right = dir_left

files_left = glob.glob(f'{dir_left}/3d*.{var_left}.png')
images = []
for pngfile in files_left:
    left  = imageio.imread(pngfile)
    right = imageio.imread(pngfile.replace(dir_left, dir_right).replace(var_left, var_right))
    images.append(np.hstack((left, right)))
    #image_list.append(np.hstack((left, right[:,:,0:3])))

outfile = f'./BATSRUS_dB_demo/{run_id}-{var_left}-{var_right}.mp4'
print('Writing ' + outfile)
imageio.mimwrite(outfile, images, fps=5)
print('Wrote ' + outfile)
