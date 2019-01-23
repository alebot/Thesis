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
i_wlen = [49, 50, 51, 52, 53]
wlen = [8.516709, 9.478886, 10.54976, 11.74162, 13.06814]
star_name = 'ATau'
star_distance = 140
star_temperature = 4000
map_rad = (20 * m.pi)/(140 * 648000)
star_luminosity = 2
star_radius = m.sqrt(star_luminosity * (sun_temperature / star_temperature) ** 4)
r_in_range = [0.07, 0.1, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]


for r_in in r_in_range:
    simulation_name = star_name + ('R=%sAU' % (str(r_in)))
    cmn.calculate_visibility(simulation_name, i_wlen, wlen, star_name, map_rad)
    quit()
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
        params={'r_in': r_in, 'do_peel_off': 'T'}
    )