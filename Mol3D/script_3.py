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
i_wlen = [36]
wlen = [2.118170]
star_name = 'GTest'
star_distance = 140
map_rad = (20 * m.pi)/(140 * 648000)

star_temperature = 6300

star_luminosity_min = 1
star_luminosity_max = 50
r_in = 1
simulations_names = np.array([])

labels = np.array([])
for n in range(5,8):
    for star_luminosity in [0.6, 9, 15, 23]:
        star_radius = m.sqrt(star_luminosity * (sun_temperature / star_temperature) ** 4)
        simulation_name = star_name + ('L=%sNph%s' % (str(star_luminosity), str(n)))
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
            params={'r_in': r_in, 'do_peel_off': 'T', 'no_photon' : 10**n}
        )

