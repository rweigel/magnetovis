# File cannot be read. See
#  https://github.com/SWxTREC/enlilviz/issues/13
#
# File wsa_enlil.t22z.suball.nc downloaded from 
#  https://nomads.ncep.noaa.gov/pub/data/nccf/com/wsa_enlil/prod/
#
import matplotlib.pyplot as plt
import enlilviz as ev
import enlilviz.plotting as evplot

run = ev.io.load_example()
print(run)
import enlilviz as ev
run = ev.read_enlil2d('wsa_enlil.t22z.suball.nc')
print(run)
