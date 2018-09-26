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


def run_simulation(
    star_name,
    star_temperature,
    star_radius,
    star_distance,
    simulation_name,
    run_temperature=True,
    run_mono=True,
    run_raytrace=True,
    run_visibility=True,
    i_wlen=wavelengths_index,
    wlen=wavelengths,
    params={}
):

    star_input = root_dir + 'input/input_' + simulation_name + '.dat'
    shutil.copyfile(input_file, star_input)
    project_name = simulation_name + '_temp_n'

    if run_temperature:
        # Temperature simulation
        u.replace(star_input, 'proname', project_name)
        u.replace(star_input, 'T_star', star_temperature)
        u.replace(star_input, 'R_star', star_radius)
        u.replace(star_input, 'distance', star_distance)
        u.replace(star_input, 'no_photon', 10**7)
        for key, value in params.items():
            u.replace(star_input, key, value)
        os.system(root_dir + "mol3d " + star_input)

    if run_raytrace:
        # Raytrace simulation
        u.replace(star_input, 'proname', simulation_name + '_raytrace')
        u.replace(star_input, 'old_model', 'T')
        u.replace(star_input, 'old_proname', project_name)
        u.replace(star_input, 'do_MC_temperature', 'F')
        u.replace(star_input, 'do_continuum_raytrace', 'T')
        u.replace(star_input, 'no_photon', 10**6)
        os.system(root_dir + "mol3d " + star_input)

    if run_mono:
        # Continuum simulation
        u.replace(star_input, 'proname', simulation_name + '_mono')
        u.replace(star_input, 'old_model', 'T')
        u.replace(star_input, 'old_proname', project_name)
        u.replace(star_input, 'do_continuum_mono', 'T')
        u.replace(star_input, 'do_continuum_raytrace', 'F')
        os.system(root_dir + "mol3d " + star_input)

    if run_visibility:
        # Calculate visibility
        r_ou = u.extract(star_input, 'r_ou')
        map_rad = np.arctan((r_ou * m.pi)/(star_distance * 648000))
        calculate_visibility(simulation_name, i_wlen, wlen, star_name, map_rad)

    os.system('rm ' + star_input)


def calculate_visibility(simulation_name, i_wlen, wlen, star_name, map_rad):
    # Visibility calculation
    mono_file = fits.open(results_dir + simulation_name + '_mono_continuum_map_mono.fits.gz')
    raytrace_file = fits.open(results_dir + simulation_name + '_raytrace_continuum_map_raytrace.fits.gz')
    data_mono = mono_file[0].data[0][i_wlen]
    data_raytrace = raytrace_file[0].data[0][i_wlen]
    mono_file.close()
    raytrace_file.close()

    data = data_raytrace + data_mono
    del data_raytrace
    del data_mono

    visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([200]), wlen, data, map_rad)
    kband = np.array([])
    nband = np.array([])
    x = np.array([])

    date_dir = u.make_date_dir(visibility_dir)

    filename = date_dir + 'visibilities_' + simulation_name + '.csv';
    with open(filename, 'w') as fd:
        writer = csv.writer(fd, delimiter=",", lineterminator='\n')
        writer.writerow(['baseline', str(wlen[0]) + 'micron', str(wlen[1]) + 'micron'])
        writer.writerow([0, [1], [1]])
        for i in range(5, 205, 5):
            visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([i]), wlen, data, map_rad)
            print(i, visibility)
            writer.writerow([i, visibility[0], visibility[1]])

    del data
    plot_visibility(filename, i_wlen, wlen, star_name)


def plot_visibility(filename, i_wlen, wlen, star_name):
    date_dir = u.make_date_dir(figures_dir);

    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=",", lineterminator='\n')
        next(reader)
        for row in reader:
            x = np.append(x, [float(row[0])])
            kband = np.append(kband, [float(row[1][1:-1])])
            nband = np.append(nband, [float(row[2][1:-1])])
    print(x, kband, nband)

    plt.plot(x, kband, label=str(wlen[0]) + ' $\mu$m')
    plt.plot(x, nband, label=str(wlen[1]) + ' $\mu$m')
    plt.xlabel('Baseline ($m$)')
    plt.ylabel('Visibility')
    plt.legend()
    plt.title('Visibilities variation with baseline for %s' % star_name)
    plt.savefig(date_dir + "visibility%s.png" % star_name)


def plot_visibility_multi(simulation_names, labels, star_name, date=None):
    date_dir = u.get_date_dir(visibility_dir, date)
    fig_dir = u.make_date_dir(figures_dir);

    for key, simulation_name in simulation_names:
        kband = np.array([])
        nband = np.array([])
        x = np.array([])
        with open(date_dir + 'visibilities_' + simulation_name + '.csv', 'rt') as csvfile:
            reader = csv.reader(csvfile,delimiter=",", lineterminator='\n')
            next(reader)
            for row in reader:
                x = np.append(x, [float(row[0])])
                kband = np.append(kband, [float(row[1][1:-1])])
                nband = np.append(nband, [float(row[2][1:-1])])
        print(x, kband, nband)
        plt.figure(1)
        plt.plot(x, kband, label=labels[key])
        plt.figure(2)
        plt.plot(x, kband, label=labels[key])

    plt.figure(1)
    plt.xlabel('Baseline ($m$)')
    plt.ylabel('Visibility')
    plt.title('Visibilities variation with baseline for %s band (%s) %s' % ('K', str(wavelengths[0]) + ' $\mu$m', star_name))
    plt.legend()
    plt.savefig(fig_dir + "visibility%s.png" % (star_name + 'Kband'))

    plt.figure(2)
    plt.xlabel('Baseline ($m$)')
    plt.ylabel('Visibility')
    plt.title('Visibilities variation with baseline for %s band (%s) %s' % ('N', str(wlen_s[0]) + ' $\mu$m', star_name))
    plt.legend()
    plt.savefig(fig_dir + "visibility%s.png" % (star_name + 'Nband'))
    print(star_name + " done!")


def get_t_max(simulation_name):
    data = np.genfromtxt(results_dir + simulation_name + '_cut_x.dat')
    n_dust = int((data.shape[1] - 9) / 2)
    init = data.shape[0] // 2 + 1

    return np.amax(data[init:, 5 + n_dust])