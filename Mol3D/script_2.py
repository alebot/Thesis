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

plt.rcParams.update(pgf_with_latex)
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
simulations_names = np.array([])
#
# for r_in in [1]:
#     for star_temperature in [7000, 9000]:
#         for star_luminosity in [20]:
#             star_radius = m.sqrt(star_luminosity * (sun_temperature / star_temperature) ** 4)
#             simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
#             cmn.run_simulation(
#                 star_name,
#                 star_temperature,
#                 star_radius,
#                 star_distance,
#                 simulation_name,
#                 run_temperature=True,
#                 run_rm=True,
#                 run_visibility=True,
#                 i_wlen=i_wlen,
#                 wlen=wlen,
#                 params={'r_in': r_in, 'do_peel_off': 'T'}
#             )
#
# star_name = 'VTau'
# for r_in in [1]:
#     for star_temperature in [3900, 9000]:
#         for star_luminosity in [1, 5, 50]:
#             star_radius = m.sqrt(star_luminosity * (sun_temperature / star_temperature) ** 4)
#             simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
#             cmn.run_simulation(
#                 star_name,
#                 star_temperature,
#                 star_radius,
#                 star_distance,
#                 simulation_name,
#                 run_temperature=True,
#                 run_rm=True,
#                 run_visibility=True,
#                 i_wlen=i_wlen,
#                 wlen=wlen,
#                 params={'r_in': r_in, 'do_peel_off': 'T'}
#             )

#TODO density simulation
star_name = 'MTau'
for r_in in [0.1]:
    for star_temperature in [3900, 4500, 5000, 7000, 9000]:
        if (star_temperature==3900):
            star_luminosities = [5, 120, 50]
        else:
            star_luminosities = [1, 5, 20, 50]
        for star_luminosity in star_luminosities:
            #Skip 3900K lum 1
            star_radius = m.sqrt(star_luminosity * (sun_temperature / star_temperature) ** 4)
            simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
            cmn.run_simulation(
                star_name,
                star_temperature,
                star_radius,
                star_distance,
                simulation_name,
                run_temperature=True,
                run_rm=True,
                run_visibility=True,
                i_wlen=i_wlen,
                wlen=wlen,
                params={'r_in': r_in, 'do_peel_off': 'T', 'mass_dust': 1e-3}
            )
