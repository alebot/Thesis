from util.constants import *
import util.util as u
import matplotlib.pyplot as plt
import numpy as np
import os
import math as m
import shutil
from astropy.io import fits
from astropy import wcs
import inter_tools as it
import csv
import util.common as cmn
import ccdproc as c

# plt.rcParams.update(pgf_with_latex)
i_wlen = np.arange(121, 134)
wlen = [8.257153, 8.616133, 8.990722, 9.381597, 9.789465, 10.21506, 10.65917, 11.12258, 11.60613, 12.11072, 12.63723, 13.18664, 13.75993]

star_name = 'CTau'
star_distance = 140
map_rad = (20 * m.pi)/(140 * 648000)

star_temperature_min = 4500
star_temperature_max = 9500

star_luminosity_min = 1
star_luminosity_max = 50
r_in = 3
simulation_names = np.empty(0)
labels = np.empty(0)
r_in = 1
#
# for star_luminosity in [1, 5, 50]:
#     for star_temperature in [3900, 9000]:
#         simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
#         simulation_names = np.append(simulation_names, simulation_name)
#         labels = np.append(labels, '$L=%s \\rm{L_{\odot}}, T=%s \\rm{K}$' %  (str(star_luminosity), str(star_temperature)))
#
# for k in [0, 6, 12]:
#     title = 'Brightness distribution for $\lambda = %s \mu m $' % str(wlen[k])
#     cmn.plot_brightness_2D(simulation_names, labels, i_wlen[k]+1, title, 10)


star_name = 'VTau'
for star_luminosity in [1, 5, 50]:
    for star_temperature in [3900, 9000]:
        simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
        simulation_names = np.append(simulation_names, simulation_name)
        labels = np.append(labels, '$L=%s \\rm{L_{\odot}}, T=%s \\rm{K}$' %  (str(star_luminosity), str(star_temperature)))

# title = 'Visibility profile for TTauri star $R_{in}=%s \\rm{AU}, \lambda = %s \mu m $' % (str(r_in), str(wlen[k]))
# cmn.plot_visibility(simulation_names, labels, i_wlen, wlen, star_name, title)

cmn.plot_temperatures(simulation_names, labels)
quit()

# cmn.calculate_visibility("CTauRin=1L=20T=5000", i_wlen, wlen, 'CTau', map_rad)
#
# for star_luminosity in [1, 5, 50]:
#     simulation_names = np.empty(0)
#     labels = np.empty(0)
#
#     for star_temperature in [3900, 9000]:
#         simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
#         simulation_names = np.append(simulation_names, simulation_name)
#         labels = np.append(labels, '$T=%s \\rm{K}$' % str(star_temperature))
#     for k in [0, 6, 12]:
#         title = "Monochromatic flux for $L=%s \\rm{L_{\odot}} at \lambda = %s \mu m$" % (str(star_luminosity),  str(wlen[k]))
#         cmn.plot_brightness(simulation_names, labels, i_wlen[k]+1, title)