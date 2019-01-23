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
stars = np.genfromtxt(star_data, skip_header=1, dtype=None)
# #Do one simulation for test
#stars = [stars[0]]
i_wlen = [36, 51, 92]
wlen = [2.118170, 10.54976, 849.4667]
i_wlen_s = [27, 36, 51]
wlen_s = [0.8083358, 2.118170, 10.54976]
map_rad = np.arctan((20 * m.pi)/(140 * 648000))
# R_ou = 201
# star_distance = 140
# map_rad = (20 * m.pi)/(140 * 648000)
# cmn.calculate_visibility('FTestL=9', [35], [2.118170], 'FTest35', map_rad)
# cmn.calculate_visibility('FTestL=15', [35], [2.118170], 'FTest35', map_rad)
# cmn.calculate_visibility('FTestL=23', [35], [2.118170], 'FTest35', map_rad)
# cmn.plot_visibility_multi(['FTestL=9','FTestL=15', 'FTestL=23'], 'FTest35')
# cmn.calculate_visibility('TTestL=9', 36, 2.11817, 'MLum', map_rad)

# cmn.calculate_visibility_1Point('2Point21AU', [27, 36], [0.8083358, 2.11817], map_rad)

# for star in stars:
#     star_name = star[0].decode('UTF-8') + 'v2'
#     star_type = star[1]
#     star_distance = star[2]
#     star_temperature = star[3]ss
#     star_luminosity = star[4]
#     star_radius = m.sqrt(star_luminosity*(sun_temperature/star_temperature)**4)
#     star_luminosity_min = star[5]
#     star_luminosity_max = star[6]
#     luminosity_range = [star_luminosity_min,
#                         np.average([star_luminosity_min, star_luminosity]),
#                         star_luminosity,
#                         np.average([star_luminosity, star_luminosity_max]),
#                         star_luminosity_max]
#
#     print(star_temperature)
#     print(star_radius)
#     print(star_luminosity)
#     print(star_name)
#
cmn.plot_brightness_2D()
cmn.plot_brightness_diff('DRTauHotR1', 'FTestL=23', 26)
quit()
star_name = 'DRTau'
star_distance = 140
r_in_range = [1, 3]
for r_in in r_in_range:
    simulation_name = 'DRTauKold' + "R%s" % str(r_in)
    cmn.run_simulation(
        star_name,
        3917,
        3.44,
        star_distance,
        simulation_name,
        run_temperature=True,
        run_rm=True,
        run_visibility=True,
        i_wlen=[49,50,51],
        wlen=[9.478886, 10.54976 , 11.74162],
        params={'r_in': r_in, 'do_peel_off':'T', 'mass_dust': 0.002}
    )
    simulation_name = 'DRTauHot' + "R%s" % str(r_in)
    cmn.run_simulation(
        star_name,
        4060,
        2.1,
        star_distance,
        simulation_name,
        run_temperature=True,
        run_rm=True,
        run_visibility=True,
        i_wlen=[49, 50, 51],
        wlen=[9.478886, 10.54976, 11.74162],
        params={'r_in': r_in, 'do_peel_off': 'T', 'mass_dust': 0.002}
    )
quit()
star_name = 'TTest'

star_temperature = 4300
star_luminosity = 2
star_radius = m.sqrt(star_luminosity * (sun_temperature / star_temperature) ** 4)
star_luminosity_min = 1.1
star_luminosity_med = 20
star_luminosity_max = 50
luminosity_range = [star_luminosity, star_luminosity_min, star_luminosity_med]
dust_mass_range = [1e-3]
r_in_range = [2, 3, 4]
simulations_names = np.array([])
labels = np.array([])
filename = 'luminosity_r_in' + star_name + '.csv';
with open(filename, 'w') as fd:
    writer = csv.writer(fd, delimiter=",", lineterminator='\n')
    writer.writerow(['Luminosity', 'R_in', 'T_max', 'T_max < 1500 K'])
    for dust_mass in dust_mass_range:
        for r_in in r_in_range:
            simulation_name = star_name + ('M=%sR=%sAU' % (str(dust_mass), str(r_in)))
            cmn.run_simulation(
                star_name,
                star_temperature,
                star_radius,
                star_distance,
                simulation_name,
                run_temperature=True,
                run_rm=True,
                run_visibility=True,
                i_wlen=[49,50,51],
                wlen=[9.478886, 10.54976 , 11.74162],
                params={'r_in': r_in, 'do_peel_off':'T', 'mass_dust': dust_mass}
            )
# star_name = 'DRTau'
# r_ou = 200
# star_distance = 140
# i_wlen_s = [36, 51]
# wlen_s = [2.118170, 10.54976]
# mono_file = fits.open(results_dir + star_name + '_mono_continuum_map_mono.fits.gz')
# data = mono_file[0].data[0]
# w = wcs.WCS(mono_file[0].header, naxis=2)
#
# for y in range(1,5):
#     # data_test = data[0]
#     # pixcrd = w.wcs_world2pix([[0,0]], 1)
#     # pixcrd2 = w.wcs_world2pix([[0,y]], 1)
#     # data_test[int(pixcrd[0][0]), int(pixcrd[0][1])]=1
#     # data_test[int(pixcrd2[0][0]), int(pixcrd2[0][1])]=1
#     # mono_file.close()
#     # map_rad = np.arctan((r_ou * m.pi)/(star_distance * 648000))
#     # data[51] = data_test
#     # data[36] = data_test
#     # del data_test
#     # kband = np.array([])
#     # nband = np.array([])
#     #
#     date_dir = u.make_date_dir(visibility_dir)
#
#     filename = date_dir + 'visibilities_2D_' + str(y) + 'AU.csv';
#     # with open(filename, 'w') as fd:
#     #     writer = csv.writer(fd, delimiter=",", lineterminator='\n')
#     #     writer.writerow(['baseline', str(wlen[0]) + 'micron', str(wlen[1]) + 'micron'])
#     #     writer.writerow([0, [1], [1]])
#     #     for i in range(5, 205, 5):
#     #         visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([i]), wlen, data, map_rad)
#     #         print(i, visibility)
#     #         writer.writerow([i, visibility[0], visibility[1]])
#
#
#     cmn.plot_visibility(filename, i_wlen, wlen, star_name + '_2D_' + str(y) + 'AU')
# del data
