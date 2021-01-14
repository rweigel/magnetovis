import numpy as np

###########
N = 100
debug = False

def exampleCallable(r, theta, phi):
    return np.cos(3*phi)* r**3 * np.sin(5*theta)
###########

rmin = 1.
dr = 0.02
dtheta = np.pi/N 
dphi = 2.*np.pi/N

r_ax = rmin + dr*np.arange(N)
theta_ax = dtheta*np.arange(N) + dtheta/2.
phi_ax = dphi*np.arange(N)

phi = np.kron(np.ones(N),phi_ax)
theta = np.kron(theta_ax,np.ones(N))
r = np.kron(r_ax, np.ones(N**2))
phi = np.kron(np.ones(N), phi)
theta = np.kron(np.ones(N), theta)


P = np.column_stack([r,theta,phi])

P_cartesian = np.nan*np.empty(P.shape)
P_cartesian[:,0] = P[:,0]*np.cos(P[:,2])*np.sin(P[:,1])  # x = r cos(phi) sin(theta)
P_cartesian[:,1] = P[:,0]*np.sin(P[:,2])*np.sin(P[:,1])  # y = r sin(phi) sin(theta)
P_cartesian[:,2] = P[:,0]*np.cos(P[:,1])                 # z = r cos(theta)

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
            #print(np.array(towrite))
            f.close()
            del f
            l+=1


scalarfield = []
for i in range(N**3):
    scalarfield.append(exampleCallable(P[i,0],P[i,1],P[i,2]))
scalarfield = np.array(scalarfield)

nV_Periodic = V_Periodic.shape[0]

f = open('UNSTRUCTURED_GRID-volumesPeriodic.vtk','w')
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

