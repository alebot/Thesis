from util.constants import *
import util.util as u
import matplotlib.pyplot as plt
import numpy as np
import os
import math as m
import shutil
from astropy.io import fits
import inter_tools as it
import csv

plt.rcParams.update(pgf_with_latex)
stars = np.genfromtxt(star_data, skip_header=1, dtype=None)
# #Do one simulation for test
stars = [stars[0]]
i_wlen = [36, 51, 92]
wlen = [2.118170, 10.54976, 849.4667]
i_wlen_s = [36, 51]
wlen_s = [2.118170, 10.54976]
R_ou = 200

# for star in stars:
#     star_name = star[0].decode('UTF-8') + 'v2'
#     star_type = star[1]
#     star_distance = star[2]
#     star_temperature = star[3]
#     star_luminosity = star[4]
#     map_rad = np.arctan((R_ou * m.pi)/(star_distance * 648000))
#     star_radius = m.sqrt(star_luminosity*(sun_temperature/star_temperature)**4)
#
#     print(star_temperature)
#     print(star_radius)
#     print(star_luminosity)
#     print(star_name)
#
#     star_input = root_dir + 'input/input_' + star_name + '.dat'
#     shutil.copyfile(input_file, star_input)
#
#     #Temperature simulation
#     project_name = star_name + '_temp_n'
#     u.replace(star_input, 'proname', project_name)
#     u.replace(star_input, 'T_star', star_temperature)
#     u.replace(star_input, 'R_star', star_radius)
#     u.replace(star_input, 'distance', star_distance)
#     u.replace(star_input, 'no_photon', 10**7)
#     os.system(root_dir + "mol3d " + star_input)
#
#     #Raytrace simulation
#     u.replace(star_input, 'proname', star_name + '_raytrace')
#     u.replace(star_input, 'old_model', 'T')
#     u.replace(star_input, 'old_proname', project_name)
#     u.replace(star_input, 'do_MC_temperature', 'F')
#     u.replace(star_input, 'do_continuum_raytrace', 'T')
#     u.replace(star_input, 'no_photon', 10**6)
#     os.system(root_dir + "mol3d " + star_input)
#
#     #Continuum simulation
#     u.replace(star_input, 'proname', star_name + '_mono')
#     u.replace(star_input, 'old_model', 'T')
#     u.replace(star_input, 'old_proname', project_name)
#     u.replace(star_input, 'do_continuum_mono', 'T')
#     u.replace(star_input, 'do_continuum_raytrace', 'F')
#
#     os.system(root_dir + "mol3d " + star_input)
#     os.system('rm ' + star_input)
#
#     #Visibility calculation
#     mono_file = fits.open(results_dir + star_name + '_mono_continuum_map_mono.fits.gz')
#     raytrace_file = fits.open(results_dir + star_name + '_raytrace_continuum_map_raytrace.fits.gz')
#     data_mono = mono_file[0].data[0][i_wlen_s]
#     data_raytrace = raytrace_file[0].data[0][i_wlen_s]
#
#     data = data_raytrace + data_mono;
#
#     visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([200]), wlen_s, data, map_rad)
#     kband = np.array([])
#     nband = np.array([])
#     x = np.array([])
#     mono_file.close()
#     raytrace_file.close()
#
#     with open('visibilities2' + star_name + '.csv', 'w') as fd:
#         writer = csv.writer(fd, delimiter=",", lineterminator='\n')
#         writer.writerow(['baseline', str(wlen_s[0]) + 'micron', str(wlen_s[1]) + 'micron'])
#         writer.writerow([0, [1], [1]])
#         for i in range(5, 205, 5):
#             visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([i]), wlen_s, data, map_rad)
#             print(i, visibility)
#             writer.writerow([i, visibility[0], visibility[1]])
#     with open('visibilities2' + star_name + '.csv', 'rt') as csvfile:
#         reader = csv.reader(csvfile, delimiter=",", lineterminator='\n')
#         next(reader)
#         for row in reader:
#             x = np.append(x, [float(row[0])])
#             kband = np.append(kband, [float(row[1][1:-1])])
#             nband = np.append(nband, [float(row[2][1:-1])])
#     print(x, kband, nband)
#
#     plt.plot(x, kband, label=str(wlen_s[0]) + ' $\mu$m')
#     plt.plot(x, nband, label=str(wlen_s[1]) + ' $\mu$m')
#     plt.xlabel('Baseline ($m$)')
#     plt.ylabel('Visibility')
#     plt.legend()
#     plt.title('Visibilities variation with baseline for %s' % star_name)
#     plt.savefig("visibility%s.png" % star_name)
#     print(star_name + " done!")


for star in stars:
    star_name = star[0].decode('UTF-8')
    star_type = star[1]
    star_distance = star[2]
    star_temperature = star[3]
    star_luminosity = star[4]
    star_luminosity_min = star[5]
    star_luminosity_max = star[6]
    map_rad = np.arctan((R_ou * m.pi) / (star_distance * 648000))
    luminosity_range = [star_luminosity_min,
                        np.average([star_luminosity_min, star_luminosity]),
                        star_luminosity,
                        np.average([star_luminosity, star_luminosity_max]),
                        star_luminosity_max]
    # for luminosity in luminosity_range:
    #     star_radius = m.sqrt(luminosity*(sun_temperature/star_temperature)**4)
    #
    #     print(star_temperature)
    #     print(star_radius)
    #     print(luminosity)
    #     print(star_name)
    #     star_input = root_dir + 'input/input_' + star_name + '.dat'
    #     shutil.copyfile(input_file, star_input)
    #
    #     #Temperature simulation
    #     project_name = star_name + '_temp_n_L' + str(luminosity)
    #     u.replace(star_input, 'proname', project_name)
    #     u.replace(star_input, 'T_star', star_temperature)
    #     u.replace(star_input, 'R_star', star_radius)
    #     u.replace(star_input, 'distance', star_distance)
    #     u.replace(star_input, 'no_photon', 10**7)
    #     os.system(root_dir + "mol3d " + star_input)
    #
    #     #Raytrace simulation
    #     u.replace(star_input, 'proname', star_name + '_raytrace_L' + str(luminosity))
    #     u.replace(star_input, 'old_model', 'T')
    #     u.replace(star_input, 'old_proname', project_name)
    #     u.replace(star_input, 'do_MC_temperature', 'F')
    #     u.replace(star_input, 'do_continuum_raytrace', 'T')
    #     u.replace(star_input, 'no_photon', 10**6)
    #     os.system(root_dir + "mol3d " + star_input)
    #
    #     #Continuum simulation
    #     u.replace(star_input, 'proname', star_name + '_mono_L' + str(luminosity))
    #     u.replace(star_input, 'old_model', 'T')
    #     u.replace(star_input, 'old_proname', project_name)
    #     u.replace(star_input, 'do_continuum_mono', 'T')
    #     u.replace(star_input, 'do_con])
    #     with open('visibilities' + star_name + '_L' + str(luminosity) + '.csv', 'rt') as csvfile:
    #         reader = csv.reader(ctinuum_raytrace', 'F')
    #
    #     os.system(root_dir + "mol3d " + star_input)
    #     os.system('rm ' + star_input)
    #
    #     #Visibility calculation
    #     mono_file = fits.open(results_dir + star_name + '_mono_L' + str(luminosity) + '_continuum_map_mono.fits.gz')
    #     raytrace_file = fits.open(results_dir + star_name + '_raytrace_L' + str(luminosity) + '_continuum_map_raytrace.fits.gz')
    #     data_mono = mono_file[0].data[0][i_wlen_s]
    #     data_raytrace = raytrace_file[0].data[0][i_wlen_s]
    #
    #     data = data_raytrace + data_mono;
    #
    #     visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([200]), wlen_s, data, map_rad)
    #     with open('visibilities' + star_name + '_L' + str(luminosity) + '.csv', 'w') as fd:
    #         writer = csv.writer(fd, delimiter=",", lineterminator='\n')
    #         writer.writerow(['baseline', str(wlen_s[0]) + 'micron', str(wlen_s[1]) + 'micron'])
    #         writer.writerow([0, [1], [1]])
    #         for i in range(5, 205, 5):
    #             visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([i]), wlen_s, data, map_rad)
    #             writer.writerow([i, visibility[0], visibility[1]])
    #
    #     mono_file.close()
    #     raytrace_file.close()
    for luminosity in luminosity_range:
        kband = np.array([])
        nband = np.array([])
        x = np.array([])
        with open('visibilities' + star_name + '_L' + str(luminosity) + '.csv', 'rt') as csvfile:
            reader = csv.reader(csvfile,delimiter=",", lineterminator='\n')
            next(reader)
            for row in reader:
                x = np.append(x, [float(row[0])])
                kband = np.append(kband, [float(row[1][1:-1])])
                nband = np.append(nband, [float(row[2][1:-1])])
        print(x, kband, nband)
        plt.figure(1)
        plt.plot(x, kband, label='L=' + str(luminosity) + "$L_{\odot}$")
        plt.figure(2)
        plt.plot(x, kband, label='L=' + str(luminosity) + "$L_{\odot}$")

    plt.figure(1)
    plt.xlabel('Baseline ($m$)')
    plt.ylabel('Visibility')
    plt.title('Visibilities variation with baseline for %s band (%s) %s' % ('K', str(wlen_s[0]) + ' $\mu$m', star_name))
    plt.legend()
    plt.savefig("visibility%s.png" % (star_name + 'Kband'))

    plt.figure(2)
    plt.xlabel('Baseline ($m$)')
    plt.ylabel('Visibility')
    plt.title('Visibilities variation with baseline for %s band (%s) %s' % ('N', str(wlen_s[0]) + ' $\mu$m', star_name))
    plt.legend()
    plt.savefig("visibility%s.png" % (star_name + 'Nband'))
    print(star_name + " done!")