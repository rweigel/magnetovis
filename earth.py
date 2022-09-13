# Demo 1
import magnetovis as mvs

mvs.ClearPipeline()

# Geographic
mvs.Earth(time='2001-01-01', coord_sys="GEO")
(X, Y, Z) = (0.2795167448086866, 0.903810269383695, 0.32403300191204026)
import paraview.simple as pvs
s = pvs.Sphere(Radius=0.1, Center=(X,Y,Z))
pvs.Show(s)

if False:
  # GSM
  mvs.Earth(time='2001-01-01', coord_sys="GSM")
  (X, Y, Z) = [-0.3963430948923141, -0.9180665499032108, 0.008121642690819327]
  import paraview.simple as pvs
  s = pvs.Sphere(Radius=0.1, Center=(X,Y,Z))
  pvs.Show(s)

