def dipole(r, m=[0, 0, 1], k=1e-7, vectorized=True, r_nan=1.0):
  """Coordinate-free form of field for electric or magnetic dipole

    B = k ( 3(m dot r_hat)r_hat - m )/|r|^3
      = k ( 3(m dot r)r/|r|^5 - m/|r|^3 )
      = k ( 3(m_x*r_x + m_y*r_y + m_z*r_z)r - m/|r|^3)

    r = [x, y, z]

    and the default constant is that for a magnetic dipole in MKS:

    k = k_m = mu_o/(4*pi) = 1 e-7 [H/m] ([H/m] = [N/A^2])

    for an electric dipole in MKS, use

    k = k_e = 1/(4*pi*epsilon_o) = 8.9875517923 e9 [N·m^2/C^2]

  """
  import numpy as np

  r = np.array(r)

  if vectorized == True:
    r_mag = np.linalg.norm(r, axis=1)
    r_mag = np.reshape(r_mag, (r_mag.shape[0], 1))
    r_mag = np.tile(r_mag, (1, 3))
    m_dot_r = np.dot(r, m)
    m_dot_r = np.reshape(m_dot_r, (m_dot_r.shape[0], 1))
    m_dot_r = np.tile(m_dot_r, (1, 3))
    m = np.tile(m, (r.shape[0], 1))
    with np.errstate(divide='ignore'):
      B = k * ( 3.0*(m_dot_r/np.power(r_mag, 5.0))*r - m/np.power(r_mag, 3.0) )
  else:
    B = np.full(r.shape, np.nan)
    for i in range(r.shape[0]):
        r_mag = np.linalg.norm(r[i,:], axis=0)
        with np.errstate(divide='ignore'):
          for j in range(3):
              N = (m[0]*r[i,0] + m[1]*r[i,1] + m[2]*r[i,2])*r[i,j]
              B[i,j] = k * (3*N/np.power(r_mag, 5) - m[j]/np.power(r_mag, 5) )

  if r_nan is not None:
    B[r_mag <= r_nan] = np.nan

  return B


if __name__ == "__main__":
  print(dipole([[1, 0, 0], [-1, 0, 0]], m=[1, 0, 0], vectorized=False))
  print(dipole([[1, 0, 0], [-1, 0, 0]], m=[1, 0, 0], vectorized=True))

  print(dipole([[0, 1, 0], [0, -1, 0]], m=[0, 1, 0], vectorized=False))
  print(dipole([[0, 1, 0], [0, -1, 0]], m=[0, 1, 0], vectorized=True))

  print(dipole([[0, 0, 1], [0, 0, -1]], m=[0, 0, 1], vectorized=False))
  print(dipole([[0, 0, 1], [0, 0, -1]], m=[0, 0, 1], vectorized=True))

