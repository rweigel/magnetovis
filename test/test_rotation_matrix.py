# these tests requires scipy

from magnetovis import rotation_matrix
import numpy as np
from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R
from timeit import timeit

# setting tolerance levels for numpy's allclose funtion
rtol, atol = 1e-12, 1e-12

# test rotation matrix creation when the rotation axis is parallel to
# x, y, or z axis
rot_axes = ['x','y','z']
angles =  np.random.randint(-360,360,100)
for angle in angles:
    for rot_axis in rot_axes:
        # scipy method https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_rotvec.html
        # scipy matrix https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_matrix.html
        if rot_axis == 'x':
            scipy_rotmat = R.from_rotvec(np.radians(angle)*np.array([1,0,0])).as_matrix()
            mvs_rotmat = rotation_matrix([1,0,0], angle)
        if rot_axis == 'y':
            scipy_rotmat = R.from_rotvec(np.radians(angle)*np.array([0,1,0])).as_matrix()
            mvs_rotmat = rotation_matrix([0,1,0], angle)
        if rot_axis == 'z':
            scipy_rotmat = R.from_rotvec(np.radians(angle)*np.array([0,0,1])).as_matrix()
            mvs_rotmat = rotation_matrix([0,0,1], angle)

        assert np.allclose(scipy_rotmat, mvs_rotmat, rtol=1e-12, atol=1e-12)

# test rotation matrix creation for an arbitrary axis direction
rot_axes = np.random.randint(-100,100,(100,3))
for angle in angles:
    for rot_axis in rot_axes:
        scipy_rotmat = R.from_rotvec(np.radians(angle)*rot_axis/norm(rot_axis)).as_matrix()
        mvs_rotmat = rotation_matrix(rot_axis, angle)
        assert np.allclose(scipy_rotmat, mvs_rotmat, rtol=1e-12, atol=1e-12)

print("accuracy test concludes that\n"+
       f"   abs(scipy_rotmat - mvs_rotmat) <= {atol} + {rtol} * abs(mvs_rotmat)" )

# time test for creation of rotation matrix
scipy_setup = """
from scipy.spatial.transform import Rotation as R
"""
mvs_setup = """
from magnetovis import rotation_matrix
"""
numpy_setup = """
import numpy as np
from numpy.linalg import norm
"""
angle_n_axis_stmt = """
angle = np.random.randint(-360,360)
rot_axis = np.random.randint(-100,100,3)
"""
scipy_stmt = """
R.from_rotvec(np.radians(angle)*rot_axis/norm(rot_axis)).as_matrix()
"""
mvs_stmt = """
rotation_matrix(rot_axis, angle)
"""
scipy_time = timeit(angle_n_axis_stmt+scipy_stmt, numpy_setup+scipy_setup, number=10000)
mvs_time = timeit(angle_n_axis_stmt+mvs_stmt, numpy_setup+mvs_setup, number=10000)

print(f"scipy time (s) {scipy_time}")
print(f"mvs time   (s) {mvs_time}")
print(f"time relative difference: {abs(mvs_time - scipy_time)/((scipy_time+mvs_time)/2)}")
print(f"ratio of scipy time to mvs time: {scipy_time/mvs_time}")
