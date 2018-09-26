from util.constants import *
import util.common as cmn
import matplotlib.pyplot as plt
import numpy as np
import math as m
import csv


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
r_in_range = [0.1, 0.2, 0.5, 1, 2, 5, 10]

filename = 'luminosity_r_in' + star_name + '.csv';
with open(filename, 'w') as fd:
    writer = csv.writer(fd, delimiter=",", lineterminator='\n')
    writer.writerow(['Luminosity', 'R_in', 'T_max', 'T_max < 1500 K'])
    for luminosity in luminosity_range:
        for r_in in r_in_range:
            simulation_name = star_name + 'L_' + str(luminosity) + '_Rin_' + str(r_in)
            cmn.run_simulation(
                star_name,
                star_temperature,
                star_radius,
                star_distance,
                simulation_name,
                run_temperature=True,
                run_mono=False,
                run_raytrace=False,
                run_visibility=False,
                i_wlen=i_wlen_s,
                wlen=wlen_s,
                params={'r_in': r_in, 'no_photon': 10**6}
            )
            t_max = cmn.get_t_max(simulation_name + '_temp_n')
            writer.writerow([luminosity, r_in, t_max, t_max < 1500])
