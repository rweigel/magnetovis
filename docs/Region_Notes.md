# Mismatch in Region transtion and boundary

According to the SSCWeb the magnetopause is supposed to separate the Magnetosphere 
and Magnetosheath regions. The Bowshock is supposed to separete the Magnetosheath
and Interplanetary Medium.  [SSCWeb](https://sscweb.gsfc.nasa.gov/users_guide/ssc_reg_doc.shtml)

> Spacecraft Regions:
> The Interplanetary Medium, Magnetosheath, and Magnetosphere regions are defined by model 
> boundaries for the magnetopause and bow shock surfaces.

SSCWeb states that they are using the Sibeck Roelof 1993 Magnetopause model 
however from analyzing the JAVA code they appear to be using the Sibeck Lopez Roelof 1991
magnetopause model instead. An exert from SSCWeb is listed below and an analysis of 
the Tipsod JAVA source code is in the section 
<strong>Sibeck 1991 Magnetopause model used in Tipsod and Magnetovis.</strong> below

> For the Magnetopause, the Roelof and Sibeck model (JGR, 98, 21421, 1993) is employed. The model 
> represents the boundary as a "quadratic function" in aberrated GSE coordinates;...

When collecting data from [SSCWeb locator form](https://sscweb.gsfc.nasa.gov/cgi-bin/Locator.cgi)
and selecting Spacecraft Region and Distance from Magnetopause or Bowshock there is a mismatch
in the data. The boundary of the magnetopause according to the distance column does not coincide
with the change in the spacecraft region column. Same goes for Bowshock. 

## SSCWeb locator form

The chart below was generated from [SSCWeb locator form](https://sscweb.gsfc.nasa.gov/cgi-bin/Locator.cgi)
which shows distance from the magnetopause to the satellite. Positive numbers
mean that the satellite is outside the magnetopause and negative numbers means 
the satellite is outside the magnetopause. The satellite is cluster 1 which 
makes the transition around 19:51 according to the magnetopause distance 
column however the region does not switch until 20:02 to 20:03.
```
  LOCATOR_GENERAL OUTPUT: 

    User: sscweb
    Date: Tue 22-Sep-2020 (266) 22:54:16
  Status: request completed successfully


GROUP 1    Satellite   Resolution   Factor
            cluster1       60         1

           Start Time           Stop Time 
           2002   1 19.75000    2002   1 20.08333


 Coord/            Min/Max      Range Filter          Filter
Component   Output Markers    Minimum     Maximum    Mins/Maxes
GSE X        YES      -         -           -             -   
GSE Y        YES      -         -           -             -   
GSE Z        YES      -         -           -             -   


Addtnl             Min/Max      Range Filter          Filter
Options     Output Markers    Minimum     Maximum    Mins/Maxes
dMagPause    YES      -         -           -             -   

Output the following regions:
    Spacecraft

Magnetic field model:
    Internal: IGRF
    External: Tsyganenko 89C 
    External: Tsyganenko 89C     Kp:  3-,3,3+
    Stop trace altitude (km):   100.00

Output - File: 
         lines per page: 0
 
Formats and units:
    Day/Time format: YYYY DDD HH:MM
    Degrees/Hemisphere format: Decimal degrees with 2 place(s).
        Longitude 0 to 360, latitude -90 to 90.
    Distance format: Earth radii with 2 place(s).

cluster1
      Time                 GSE (RE)               dMpause  Spacecraft
yyyy ddd hh:mm      X          Y          Z        (RE)      Region  

2002   1 19:46       2.25      10.53       8.47      -0.06 D_Msphere 
2002   1 19:47       2.26      10.55       8.46      -0.05 D_Msphere 
2002   1 19:48       2.27      10.56       8.46      -0.03 D_Msphere 
2002   1 19:49       2.28      10.58       8.46      -0.02 D_Msphere 
2002   1 19:50       2.29      10.59       8.45      -0.01 D_Msphere 
2002   1 19:51       2.30      10.61       8.45       0.01 D_Msphere 
2002   1 19:52       2.31      10.62       8.45       0.02 D_Msphere 
2002   1 19:53       2.32      10.64       8.44       0.04 D_Msphere 
2002   1 19:54       2.33      10.65       8.44       0.05 D_Msphere 
2002   1 19:55       2.35      10.67       8.44       0.06 D_Msphere 
2002   1 19:56       2.36      10.68       8.43       0.08 D_Msphere 
2002   1 19:57       2.37      10.70       8.43       0.09 D_Msphere 
2002   1 19:58       2.38      10.71       8.43       0.10 D_Msphere 
2002   1 19:59       2.39      10.73       8.42       0.12 D_Msphere 
2002   1 20:00       2.40      10.74       8.42       0.13 D_Msphere 
2002   1 20:01       2.41      10.75       8.42       0.14 D_Msphere 
2002   1 20:02       2.42      10.77       8.41       0.16 D_Msphere 
2002   1 20:03       2.43      10.78       8.41       0.17 D_Msheath 
2002   1 20:04       2.44      10.80       8.41       0.18 D_Msheath 
2002   1 20:05       2.45      10.81       8.40       0.20 D_Msheath 
```

The next chart was generated the same way but this time searching for the 
transition between the Interplanery Medium and the Magnetosheath. 
Once again the boundary layer should be the bowshock according to 
SSCWeb but the columns don't match. 

```
LOCATOR_GENERAL OUTPUT: 

    User: sscweb
    Date: Thu 24-Sep-2020 (268) 10:55:19
  Status: request completed successfully


GROUP 1    Satellite   Resolution   Factor
            cluster1       60         1

           Start Time           Stop Time 
           2002   2 10.00000    2002   2 11.25000


 Coord/            Min/Max      Range Filter          Filter
Component   Output Markers    Minimum     Maximum    Mins/Maxes
GSE X        YES      -         -           -             -   
GSE Y        YES      -         -           -             -   
GSE Z        YES      -         -           -             -   


Addtnl             Min/Max      Range Filter          Filter
Options     Output Markers    Minimum     Maximum    Mins/Maxes
dBowSck      YES      -         -           -             -   

Output the following regions:
    Spacecraft

Magnetic field model:
    Internal: IGRF
    External: Tsyganenko 89C 
    External: Tsyganenko 89C     Kp:  3-,3,3+
    Stop trace altitude (km):   100.00

Output - File: 
         lines per page: 0
 
Formats and units:
    Day/Time format: YYYY DDD HH:MM
    Degrees/Hemisphere format: Decimal degrees with 2 place(s).
        Longitude 0 to 360, latitude -90 to 90.
    Distance format: Earth radii with 2 place(s).

cluster1
      Time                 GSE (RE)               dBowShk  Spacecraft
yyyy ddd hh:mm      X          Y          Z        (RE)      Region  

2002   2 10:01       8.84      16.70       2.12      -0.17 D_Msheath 
2002   2 10:02       8.84      16.70       2.11      -0.17 D_Msheath 
2002   2 10:03       8.85      16.70       2.10      -0.17 D_Msheath 
2002   2 10:04       8.85      16.70       2.09      -0.16 D_Msheath 
2002   2 10:05       8.86      16.70       2.08      -0.16 D_Msheath 
2002   2 10:06       8.86      16.70       2.07      -0.16 D_Msheath 
2002   2 10:07       8.87      16.70       2.06      -0.15 D_Msheath 
2002   2 10:08       8.87      16.70       2.05      -0.15 D_Msheath 
2002   2 10:09       8.88      16.70       2.04      -0.15 D_Msheath 
2002   2 10:10       8.88      16.71       2.03      -0.14 D_Msheath 
2002   2 10:11       8.89      16.71       2.02      -0.14 D_Msheath 
2002   2 10:12       8.89      16.71       2.01      -0.14 Intpl_Med 
2002   2 10:13       8.89      16.71       2.00      -0.14 Intpl_Med 
2002   2 10:14       8.90      16.71       1.99      -0.14 Intpl_Med 
2002   2 10:15       8.90      16.71       1.99      -0.13 Intpl_Med 
2002   2 10:16       8.91      16.71       1.98      -0.13 Intpl_Med 
2002   2 10:17       8.91      16.71       1.97      -0.12 Intpl_Med 
2002   2 10:18       8.92      16.71       1.96      -0.12 Intpl_Med 
2002   2 10:19       8.92      16.71       1.95      -0.11 Intpl_Med 
2002   2 10:20       8.93      16.71       1.94      -0.11 Intpl_Med 
2002   2 10:21       8.93      16.71       1.93      -0.10 Intpl_Med 
2002   2 10:22       8.94      16.71       1.92      -0.10 Intpl_Med 
2002   2 10:23       8.94      16.71       1.91      -0.09 Intpl_Med 
2002   2 10:24       8.95      16.71       1.90      -0.09 Intpl_Med 
2002   2 10:25       8.95      16.71       1.89      -0.09 Intpl_Med 
2002   2 10:26       8.96      16.71       1.88      -0.08 Intpl_Med 
2002   2 10:27       8.96      16.71       1.87      -0.08 Intpl_Med 
2002   2 10:28       8.97      16.71       1.86      -0.08 Intpl_Med 
2002   2 10:29       8.97      16.71       1.85      -0.07 Intpl_Med 
2002   2 10:30       8.98      16.71       1.84      -0.07 Intpl_Med 
2002   2 10:31       8.98      16.71       1.83      -0.07 Intpl_Med 
2002   2 10:32       8.99      16.71       1.82      -0.07 Intpl_Med 
2002   2 10:33       8.99      16.71       1.81      -0.07 Intpl_Med 
2002   2 10:34       8.99      16.71       1.80      -0.07 Intpl_Med 
2002   2 10:35       9.00      16.71       1.79      -0.07 Intpl_Med 
2002   2 10:36       9.00      16.71       1.78      -0.07 Intpl_Med 
2002   2 10:37       9.01      16.71       1.77      -0.07 Intpl_Med 
2002   2 10:38       9.01      16.71       1.77      -0.07 Intpl_Med 
2002   2 10:39       9.02      16.71       1.76      -0.04 Intpl_Med 
2002   2 10:40       9.02      16.71       1.75      -0.03 Intpl_Med 
2002   2 10:41       9.03      16.71       1.74      -0.03 Intpl_Med 
2002   2 10:42       9.03      16.71       1.73      -0.03 Intpl_Med 
2002   2 10:43       9.04      16.71       1.72      -0.02 Intpl_Med 
2002   2 10:44       9.04      16.71       1.71      -0.02 Intpl_Med 
2002   2 10:45       9.05      16.71       1.70      -0.02 Intpl_Med 
2002   2 10:46       9.05      16.71       1.69      -0.01 Intpl_Med 
2002   2 10:47       9.05      16.72       1.68      -0.01 Intpl_Med 
2002   2 10:48       9.06      16.72       1.67      -0.01 Intpl_Med 
2002   2 10:49       9.06      16.72       1.66      -0.01 Intpl_Med 
2002   2 10:50       9.07      16.71       1.65      -0.00 Intpl_Med 
2002   2 10:51       9.07      16.72       1.64       0.00 Intpl_Med 
2002   2 10:52       9.08      16.71       1.63       0.01 Intpl_Med 
2002   2 10:53       9.08      16.71       1.62       0.01 Intpl_Med 
2002   2 10:54       9.09      16.71       1.61       0.01 Intpl_Med 
2002   2 10:55       9.09      16.71       1.60       0.02 Intpl_Med 
2002   2 10:56       9.10      16.71       1.59       0.02 Intpl_Med 
2002   2 10:57       9.10      16.71       1.58       0.02 Intpl_Med 
2002   2 10:58       9.10      16.71       1.57       0.03 Intpl_Med 
2002   2 10:59       9.11      16.71       1.56       0.03 Intpl_Med 
2002   2 11:00       9.11      16.71       1.55       0.03 Intpl_Med 
2002   2 11:01       9.12      16.71       1.54       0.03 Intpl_Med 
2002   2 11:02       9.12      16.71       1.54       0.04 Intpl_Med 
2002   2 11:03       9.13      16.71       1.53       0.04 Intpl_Med 
2002   2 11:04       9.13      16.71       1.52       0.04 Intpl_Med 
2002   2 11:05       9.14      16.71       1.51       0.05 Intpl_Med 
2002   2 11:06       9.14      16.71       1.50       0.05 Intpl_Med 
2002   2 11:07       9.15      16.71       1.49       0.05 Intpl_Med 
2002   2 11:08       9.15      16.71       1.48       0.06 Intpl_Med 
2002   2 11:09       9.15      16.71       1.47       0.06 Intpl_Med 
2002   2 11:10       9.16      16.71       1.46       0.06 Intpl_Med 
2002   2 11:11       9.16      16.71       1.45       0.07 Intpl_Med 
2002   2 11:12       9.17      16.71       1.44       0.07 Intpl_Med 
2002   2 11:13       9.17      16.71       1.43       0.07 Intpl_Med 
2002   2 11:14       9.18      16.71       1.42       0.08 Intpl_Med 
2002   2 11:15       9.18      16.71       1.41       0.08 Intpl_Med 
```

Both Tipsod and Magnetovis produce very similar magnetopause models 
(Sibeck, Lopez, and Sibeck 1991) and bowshock models (Fairfield 1971) 
which closely match the distance columns but not the regions column.

## Instructions for Tipsod 4D Orbit Viewer magnetopause and bowshock

Follow the install directions [here](https://sscweb.gsfc.nasa.gov/tipsod/)

1. After opening the program input for magnetopause:
fr = 2002-01-01 19:35
to = 2002-01-01 20:05
OR  for bowshock input:
fr = 2002-01-02 10:45
to = 2002-01-02 11:30

2. select coordinates = GSE
3. check box Cluster-1(FM5/Rumba) and turn it's color to Red.
4. Click "Graph Orbits"
5. On the new 3D viewer screen that pops up check the box "magnetopause" (or "bowshock").
6. switch to the window labeled "Position" check the box "Bowshock" under the header
"distance to (RE)" a new column will appear in the table labeled "magnetopause" 
(or "bowshock"). 
7. Change the current position of the satellite by going back to 
the 3D Viewer window and moving the progress bar at the top of the window. 
8. observe the satellite moving on the 3D viewer window and the distance 
change in the "Position" window. 

## Instructions - Magnetovis for bowshock and magnetopause

copy the code below into a python file and save it. 
```python 
import objects 
objects.magnetopause(time=None, Bz=None, Psw=2.04, 
                          model='Roelof_Lopez_Sibeck91', coord_sys='GSE', 
                          color=[0.1,0.8,0.3,0.5], choice='Psw',
                          representation='Surface')
    
objects.satellite(time_o = '2002-01-01T19:50:00.000Z', 
                  time_f = '2002-01-01T20:00:00.000Z', 
                  satellite_id = 'cluster1', coord_sys='GSE',
                  representation='Point Gaussian',
                  shader_preset='Sphere',
                  color=None, tube_radius=None,
                  region_colors = {
                      'D_Msheath' : [0.0,0.0,0.0,0.7],
                      'N_Msheath' : [0.5,0.0,0.0,0.7],
                      'D_Msphere' : [1.0,0.0,0.0,0.7],
                      'N_Msphere' : [1.0,0.5,0.0,0.7],
                      'D_Psphere' : [0.0,1.0,0.0,0.7],
                      'N_Psphere' : [0.0,1.0,0.5,0.7],
                      'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                      'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                      'HLB_Layer' : [0.0,1.0,1.0,0.7],
                      'LLB_Layer' : [1.0,0.0,1.0,0.7],
                      'Intpl_Med' : [1.0,1.0,1.0,0.7]
                      },
                  )

objects.bowshock(time=None, Bz=None, Psw=2.04, 
                 model='Fairfield71', coord_sys='GSE', 
                 mpause_model='Roelof_Lopez_Sibeck91',
                 color=[0.1,0.8,0.3,0.7], choice='Psw',
                 representation='Surface')
    
objects.satellite(time_o = '2002-01-02T11:05:00.000Z', 
                  time_f = '2002-01-02T11:15:00.000Z', 
                  satellite_id = 'cluster1', coord_sys='GSE',
                  representation='Point Gaussian',
                  shader_preset='Sphere',
                  color=None, tube_radius=None,
                  region_colors = {
                      'D_Msheath' : [0.0,0.0,0.0,0.7],
                      'N_Msheath' : [0.5,0.0,0.0,0.7],
                      'D_Msphere' : [1.0,0.0,0.0,0.7],
                      'N_Msphere' : [1.0,0.5,0.0,0.7],
                      'D_Psphere' : [0.0,1.0,0.0,0.7],
                      'N_Psphere' : [0.0,1.0,0.5,0.7],
                      'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                      'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                      'HLB_Layer' : [0.0,1.0,1.0,0.7],
                      'LLB_Layer' : [1.0,0.0,1.0,0.7],
                      'Intpl_Med' : [1.0,1.0,1.0,0.7]
                      },
                  )
```

Next execute in terminal, replacing PYTHONFILE with your saved file. 
```bash
PYTHONPATH=/Users/Angel/opt/anaconda3/envs/python2.7/lib/python2.7/site-packages:. /Applications/ParaView-5.7.0.app/Contents/MacOS/paraview --script=[PYTHONFILE]
```

* note the PYTHONPATH variable will be different for your system.

# Sibeck 1991 Magnetopause model used in Tipsod and Magnetovis.

Tipsod 4D Orbit Viewer renders a magnetopause model from the  
paper: Solar Wind Control of the Magnetopause Shape, Location, and Motion
by Sibeck, Lopez, Roelof 1991. 
DOI: [https://doi.org/10.1029/90JA02464](https://doi.org/10.1029/90JA02464)

Specifically they are using equation (2) which states:

<a href="https://www.codecogs.com/eqnedit.php?latex=R^{2}&plus;A_{0}x^{2}&plus;B_{0}\left(\frac{p_{0}}{p}\right)^{\frac{1}{6}}x&plus;C_{0}\left(\frac{p_{0}}{p}\right)^{\frac{1}{3}}=0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?R^{2}&plus;A_{0}x^{2}&plus;B_{0}\left(\frac{p_{0}}{p}\right)^{\frac{1}{6}}x&plus;C_{0}\left(\frac{p_{0}}{p}\right)^{\frac{1}{3}}=0" title="R^{2}+A_{0}x^{2}+B_{0}\left(\frac{p_{0}}{p}\right)^{\frac{1}{6}}x+C_{0}\left(\frac{p_{0}}{p}\right)^{\frac{1}{3}}=0" /></a>


Where:
p<sub>0</sub> = 2.04 nPa
A<sub>0</sub> = 0.14
B<sub>0</sub> = 18.2
C<sub>0</sub> = -217.2
p = 2.04 nPa

The Tipsod Java code implemented can be found [here](https://sscweb.gsfc.nasa.gov/tipsod/src.zip) in the script MHDPause.java in the directory gov.nasa.gsfc.spdf.orb.utils.

Here is the comment from MHDPause.java which details there process.

```java
/*  ****************************************
 **** Sibeck's Magnetopause Surface ****
 ****************************************
 po = 2.04
 s1 = 0.14
 s2 = 18.2
 s3 = -217.2
 t1 = s2/(2 s1) = 65.0
 t2 = sqrt(t1**2 - s3/s1) = 76.0028195
 xmin = -45.0
 rho = (po/psw)**(1/6)
 r**2 = y**2+z**2 = s1*[(t2*rho)**2-(x+t1*rho)**2]
 ***********************************************
 */
 ```

<strong> 
note that while  the commented code and the Roelof, Lopez, Sibeck 1991 paper both state 
that the pressure ratio should be raised to the 1/6 power both magnetovis and tipsod 
actually raise the ratio to the 1/6.6 power. As of yet there is no justification
for the change.
</strong>











