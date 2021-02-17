import numpy as np
from copy import deepcopy

"""
This script was to test out the creation of a torus where the
inner points are connected. The script also goes onto populate
the created torus with the logrithmic density of ___ 
according to the Gallagher, Craven, and Comfort model 
[Adv. Space Res. Vol. 8, pp 15-24, 1988]
https://doi.org/10.1016/0273-1177(88)90258-X

use:
    1. Run script
    2. open plasmaDensityGrid.vtk with paraview
    3. apply slice filter
"""

N = 50
debug = False

def logDen(r, theta, phi):
    a1 = 1.4
    a2 = 1.53
    a3 = -0.036
    a4 = 30.76
    a5 = 159.9
    a7 = 6.27
    Re = 6371.2
    
    MLT = (phi*180/np.pi/15.) - 12.
    x = deepcopy(MLT)
    if MLT >= 24: MLT = MLT - 24
    if MLT < 0: MLT = MLT + 24
    if x > 12: x = x - 24
    if x< - 12: x = x + 24
    
    a6 = -0.87 + 0.12 * np.exp(-x*x/9.)
    a8 = 0.7 * np.cos(2*np.pi* (MLT-21.)/24.) + 4.4
    a9 = 15.3 * np.cos(2*np.pi*MLT/24.) + 19.7
    
    F = a2 - np.exp(a3 * (1.-a4 * np.exp(6371.2*(1.-r)/a5)))
    C2LAM = np.cos(theta)*np.cos(theta)
    L = r/np.cos(C2LAM)
    G = (a6*r/C2LAM) + a7
    H = (1. + (r /(C2LAM*a8)) ** (2. * (a9 - 1.))) ** (-a9 / (a9 - 1.))
    
    n_log = a1 * F * G * H
    
    return n_log

rmin = 1.05
dr = 0.02
dtheta = np.pi/N 
dphi = 2.*np.pi/N

r_ax = np.arange(rmin,6,(6-rmin)/N) # make radius out to 6
theta_i = 28*np.pi/180 
theta_f = 152 * np.pi/180 
theta_step = (theta_f-theta_i)/N
theta_ax = np.arange(theta_i,theta_f,theta_step)
theta_ax = np.pi/2. - theta_ax # converting from colatitude to latitude
phi_ax = dphi*np.arange(N)

phi = np.kron(np.ones(N),phi_ax)
theta = np.kron(theta_ax,np.ones(N))
r = np.kron(r_ax, np.ones(N**2))
phi = np.kron(np.ones(N), phi)
theta = np.kron(np.ones(N), theta)

P = np.column_stack([r,theta,phi])

P_cartesian = np.nan*np.empty(P.shape)
# the conversion from spherical to cartesian is done with
# theta being latitude [-90,90] instead of 
# colattitude [0,180]
P_cartesian[:,0] = P[:,0]*np.cos(P[:,2])*np.cos(P[:,1])  # x = r cos(phi) cos(theta)
P_cartesian[:,1] = P[:,0]*np.sin(P[:,2])*np.cos(P[:,1])  # y = r sin(phi) cos(theta)
P_cartesian[:,2] = P[:,0]*np.sin(P[:,1])                 # z = r sin(theta)



ind = np.arange(N**3).reshape((N,N,N))
#PERIODIC IN PHI DIRECTION (indexed by k)
indPeriodic = np.zeros((N,N,N+1), dtype=int)
indPeriodic[:,:,:-1] = ind
indPeriodic[:,:,-1] = ind[:,:,0]

V_Periodic = []
for i in range(N-1):
    for j in range(N-1):
        for k in range(N):
            V_Periodic.append( (indPeriodic[i,j,k], indPeriodic[i+1,j,k], indPeriodic[i+1,j+1,k], indPeriodic[i,j+1,k],
                       indPeriodic[i,j,k+1], indPeriodic[i+1,j,k+1], indPeriodic[i+1,j+1,k+1], indPeriodic[i,j+1,k+1])
                    )
V_Periodic = np.array(V_Periodic, dtype=int)


if debug:
    l = 1
    for i in range(N-1):
        for j in range(N-1):
            k = N-1
            f = open('VTKTESTING_'+str(l)+'.vtk','w')
            f.write('# vtk DataFile Version 3.0\n')
            f.write('Unstructured_grid cells\n')
            f.write('ASCII\n')
            f.write('DATASET UNSTRUCTURED_GRID\n')
            f.write('POINTS %d float\n'%(2**3))
            towrite = [P_cartesian[index,:] for index in list(toappend)]
            np.savetxt(f,np.array(towrite), fmt = '%.3f')
            f.close()
            del f
            l+=1


scalarfield = []
for i in range(N**3):
    scalarfield.append(logDen(P[i,0],P[i,1],P[i,2]))
scalarfield = np.array(scalarfield)

nV_Periodic = V_Periodic.shape[0]
f = open('plasmaDensityGrid.vtk','w')
f.write('# vtk DataFile Version 3.0\n')
f.write('Unstructured_grid cells\n')
f.write('ASCII\n')
f.write('DATASET UNSTRUCTURED_GRID\n')
f.write('POINTS %d float\n'%(N**3))
np.savetxt(f,P_cartesian, fmt = '%.3f')
f.write('CELLS %d %d\n'%(nV_Periodic, 9*nV_Periodic))
np.savetxt(f,np.column_stack([8*np.ones(nV_Periodic), V_Periodic]), fmt='%d')
f.write('CELL_TYPES %d\n'%(nV_Periodic))
np.savetxt(f, 12*np.ones(nV_Periodic), fmt = '%d') #12 here stands for hexahedron, see http://www.computingforscientists.info/ParaView
f.write('POINT_DATA %d\n'%(N**3))
f.write('SCALARS magfield float 1\n')
f.write('LOOKUP_TABLE default\n')
np.savetxt(f, scalarfield, fmt = '%.3f')
f.close()
del f

