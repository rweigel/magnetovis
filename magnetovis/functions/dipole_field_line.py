def dipole_field_line(n, r_min=1, phi=0, L=2):
  """Returns cartesian x, y, z for r = L*sin^2(theta)"""

  import numpy as np

  theta_min = np.arcsin(np.sqrt(r_min/L))
  theta_max = np.pi - theta_min

  thetas = np.linspace(theta_min, theta_max, num=n)
  #print(thetas*180/np.pi)

  r = L*np.sin(thetas)

  x = r*np.cos(phi)*np.sin(thetas)
  y = r*np.sin(phi)*np.sin(thetas)
  z = r*np.cos(thetas)

  return np.column_stack([x, y, z])