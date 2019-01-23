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
star_name = 'DTau'
star_distance = 140
map_rad = (20 * m.pi)/(140 * 648000)

i_wlen = np.arange(121, 134)
wlen = [8.257153, 8.616133, 8.990722, 9.381597, 9.789465, 10.21506, 10.65917, 11.12258, 11.60613, 12.11072, 12.63723, 13.18664, 13.75993]

for r_in in [0.065]:
    for star_temperature in [4050]:
        #Add 5, 15
        for star_luminosity in [0.9, 5]:
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
                params={'r_in': r_in, 'do_peel_off': 'T', 'no_photon' : 10**4}
            )
