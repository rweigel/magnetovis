from magnetovis import rotation_matrix
import numpy as np
from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R


# test rotation matrix creation when the rotation axis is parallel to
# x, y, or z axis
rot_axes = ['x','y','z']
angles =  np.random.randint(-360,360,100)
for angle in angles:
    for rot_axis in rot_axes:
        # scipy method https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_rotvec.html
        # scipy matrix https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_matrix.html
        if rot_axis == 'x':
            fr_rotmat = R.from_rotvec(np.radians(angle)*np.array([1,0,0])).as_matrix()
            mvs_rotmat = rotation_matrix([1,0,0], angle)
        if rot_axis == 'y':
            fr_rotmat = R.from_rotvec(np.radians(angle)*np.array([0,1,0])).as_matrix()
            mvs_rotmat = rotation_matrix([0,1,0], angle)
        if rot_axis == 'z':
            fr_rotmat = R.from_rotvec(np.radians(angle)*np.array([0,0,1])).as_matrix()
            mvs_rotmat = rotation_matrix([0,0,1], angle)

        assert np.allclose(fr_rotmat, mvs_rotmat, rtol=1e-12, atol=1e-12)


# test rotation matrix creation for an arbitrary axis direction
rot_axes = np.random.randint(-100,100,(100,3))
for angle in angles:
    for rot_axis in rot_axes:
        r_fr = R.from_rotvec(np.radians(angle)*rot_axis/norm(rot_axis)).as_matrix()
        mvs_rotmat = rotation_matrix(rot_axis, angle)
        assert np.allclose(r_fr, mvs_rotmat, rtol=1e-12, atol=1e-12)
