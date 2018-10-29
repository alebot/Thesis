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

plt.rcParams.update(pgf_with_latex)
stars = np.genfromtxt(star_data, skip_header=1, dtype=None)
# #Do one simulation for test
#stars = [stars[0]]
i_wlen = [36, 51, 92]
wlen = [2.118170, 10.54976, 849.4667]
i_wlen_s = [36, 51]
wlen_s = [2.118170, 10.54976]

# for star in stars:
#     star_name = star[0].decode('UTF-8') + 'v2'
#     star_type = star[1]
#     star_distance = star[2]
#     star_temperature = star[3]
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

star_name = 'TTest'
star_distance = 150
star_temperature = 6300
star_luminosity = 15
star_radius = m.sqrt(star_luminosity*(sun_temperature/star_temperature)**4)
star_luminosity_min = 9
star_luminosity_max = 23
luminosity_range = [star_luminosity_min,
                    np.average([star_luminosity_min, star_luminosity]),
                    star_luminosity,
                    np.average([star_luminosity, star_luminosity_max]),
                    star_luminosity_max]
r_in_range = [1]
simulations_names = np.array([])
labels = np.array([])
filename = 'luminosity_r_in' + star_name + '.csv';
with open(filename, 'w') as fd:
    writer = csv.writer(fd, delimiter=",", lineterminator='\n')
    writer.writerow(['Luminosity', 'R_in', 'T_max', 'T_max < 1500 K'])
    for luminosity in luminosity_range:
        for r_in in r_in_range:
            simulation_name = star_name + 'L_' + str(luminosity) + '_Rin_' + str(r_in)
            np.append(simulations_names, [simulation_name])
            np.append(labels,['L=%s' %str(luminosity)])
            cmn.run_simulation(
                star_name,
                star_temperature,
                star_radius,
                star_distance,
                simulation_name,
                run_temperature=True,
                run_mono=True,
                run_raytrace=True,
                run_visibility=True,
                i_wlen=i_wlen_s,
                wlen=wlen_s,
                params={'r_in': r_in}
            )
            t_max = cmn.get_t_max(simulation_name + '_temp_n')
            writer.writerow([luminosity, r_in, t_max, t_max < 1500])

cmn.plot_visibility_multi(simulations_names, labels, star_name)

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

simulations_names= ['']