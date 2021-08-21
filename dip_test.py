import magnetovis as mvs

time = [2015,3,20,0,0,0] # time not used if coord_sys = GSM
coord_sys = 'GSM'
extend=[[-21,-21,-21],[21,21,21]]
NxNyNz=[22,22,22]
coord_sys='GSM'
M=7.788E22
mvs.dipole_field(time, extend, NxNyNz, coord_sys, M)
