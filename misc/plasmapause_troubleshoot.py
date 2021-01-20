import numpy as np

###########
N = 50
debug = False

def exampleCallable(r, theta, phi):
    theta = np.pi/2. - theta
    a1 = 1.4
    a2 = 1.53
    a3 = -0.036
    a4 = 30.76
    a5 = 159.9
    a7 = 6.27
    Re = 6371.2
    
    MLT = (phi*180/np.pi/15.) - 12.
    x = MLT
    if MLT > 24:
        MLT = MLT - 24
    if MLT < 0:
        MLT + MLT + 24
    if x > 12:
        x = x - 24
    if x<0:
        x = x + 24
    
    a6 = -0.87 + 0.12 * np.exp(-x**2/9.)
    a8 = 0.7 * np.cos(2*np.pi* (MLT-21.)/24.) + 4.4
    a9 = 15.3 * np.cos(2*np.pi*MLT/24.) + 19.7
    
    F = a2 - np.exp(a3 * (1.-a4 * np.exp(Re*(1.-r)/a5)))
    C2LAM = (np.cos(theta))**2
    L = r/np.cos(C2LAM)
    G = (a6*r/C2LAM) + a7
    H = (1. + (L / a8) ** (2. * (a9 - 1.))) ** (-a9 / (a9 - 1.))
    
    n_log = a1 * F * G * H
    
    return n_log
    # return np.cos(3*phi)* r**3 * np.sin(5*theta)
###########

rmin = 1.05
dr = 0.02
dtheta = np.pi/N 
dphi = 2.*np.pi/N

# r_ax = rmin + dr*np.arange(N)
r_ax = np.arange(rmin,6,(6-rmin)/N) # make radius out to 6
# theta_ax = dtheta*np.arange(N) + dtheta/2. #np.arange(-np.pi/2,np.pi/2,dtheta) + dtheta/2.# dtheta*np.arange(N) #+ dtheta/2.
theta_i = 28*np.pi/180 
theta_f =152 * np.pi/180 
theta_step = (theta_f-theta_i)/N
theta_ax = np.arange(theta_i,theta_f,theta_step)
# print('theta',theta_ax*180/np.pi)
phi_ax = dphi*np.arange(N)
# print('phi',phi_ax*180/np.pi)

phi = np.kron(np.ones(N),phi_ax)
# print('phikron',phi*180/np.pi)
theta = np.kron(theta_ax,np.ones(N))
r = np.kron(r_ax, np.ones(N**2))
phi = np.kron(np.ones(N), phi)
theta = np.kron(np.ones(N), theta)
print(max(r))

P = np.column_stack([r,theta,phi])

P_cartesian = np.nan*np.empty(P.shape)
# print(P_cartesian)
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
f = open('blahUNSTRUCTURED_GRID-volumesPeriodic.vtk','w')
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

