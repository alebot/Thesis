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
import matplotlib.ticker as ticker
import random
import uuid

def plot_brightness_diff(simulation_name1, simulation_name2):

    if (not os.path.isfile(results_dir + simulation_name1 + '_mono_continuum_map_total.fits.gz')):
        print('not found')
    else:
        data1 = fits.open(results_dir + simulation_name1 + '_mono_continuum_map_total.fits.gz')

    if (not os.path.isfile(results_dir + simulation_name2 + '_mono_continuum_map_total.fits.gz')):
        print('not found')
    else:
        data2 = fits.open(results_dir + simulation_name2 + '_mono_continuum_map_total.fits.gz')

    plt.plot(np.linspace(-20, 20, 40), data1[0].data[0][200][180:220], label="$T_1 = 4060  \mathrm{K}$")
    plt.plot(np.linspace(-20, 20, 40), data2[0].data[0][200][180:220], label="$T_2 = 3917  \mathrm{K}$")
    plt.plot(np.linspace(-20, 20, 40), data1[0].data[0][200][180:220]-data2[0].data[0][200][180:220], label="$\Delta T = T_1 - T_2$")
    plt.xlabel('$\mathrm{AU}$')
    plt.ylabel('Intensity')
    plt.title('Brightness profile at $\lambda = 10.55 \mu m$')
    plt.legend()
    plt.show()
    plt.savefig('brightnessdiff.png')



def calculate_visibility_1Point(simulation_name, wlen, map_rad):
    # Visibility calculation
    data = np.zeros((1, 1001, 1001))
    data[0][487][501] = 1
    data[0][512][501] = 1
    kband = np.array([])
    nband = np.array([])
    x = np.array([])

    date_dir = u.make_date_dir(visibility_dir)

    filename = date_dir + 'visibilities_' + simulation_name + '.csv';
    with open(filename, 'w') as fd:
        writer = csv.writer(fd, delimiter=",", lineterminator='\n')
        writer.writerow(['baseline', str(wlen[0]) + 'micron'])
        writer.writerow([0, [1], [1]])
        for i in range(5, 205, 5):
            j=i/2
            visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([j]), wlen, data, map_rad)
            writer.writerow([j, visibility[0]])

    del data
    plot_visibility_1Point(filename, wlen, simulation_name)

def plot_visibility_1Point(filename, wlen, title):
    date_dir = u.make_date_dir(figures_dir);
    kband = np.array([])
    x = np.array([])

    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=",", lineterminator='\n')
        next(reader)
        for row in reader:
            x = np.append(x, [float(row[0])])
            kband = np.append(kband, [float(row[1][1:-1])])

    print('min: ', x[np.argmin(kband)])

    plt.plot(x, kband, label=str(wlen[0]) + ' $\mu$m')

    plt.xlabel('Baseline ($m$)')
    plt.ylabel('Visibility')
    plt.legend()
    plt.title('Visibilities variation with baseline for %s' % title)
    plt.savefig(date_dir + "visibility%s.png" % title)


def run_simulation(
    star_name,
    star_temperature,
    star_radius,
    star_distance,
    simulation_name,
    run_temperature=True,
    run_rm=True,
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
        for key, value in params.items():
            u.replace(star_input, key, value)
        os.system(root_dir + "mol3d " + star_input)

    if run_rm:
        # Continuum simulation
        u.replace(star_input, 'proname', simulation_name + '_mono')
        u.replace(star_input, 'old_model', 'T')
        u.replace(star_input, 'do_MC_temperature', 'F')
        u.replace(star_input, 'old_proname', project_name)
        u.replace(star_input, 'do_continuum_mono', 'T')
        u.replace(star_input, 'do_continuum_raytrace', 'T')
        os.system(root_dir + "mol3d " + star_input)

    if run_visibility:
        # Calculate visibility
        r_ou = 20 #with zoom =10
        map_rad = np.arctan((r_ou * m.pi)/(star_distance * 648000))
        calculate_visibility(simulation_name, i_wlen, wlen, star_name, map_rad)

    os.system('rm ' + star_input)


def calculate_visibility(simulation_name, i_wlen, wlen, star_name, map_rad):
    # Visibility calculation
    mono_file = fits.open(results_dir + simulation_name + '_mono_continuum_map_mono.fits.gz')
    raytrace_file = fits.open(results_dir + simulation_name + '_mono_continuum_map_raytrace.fits.gz')
    data_mono = mono_file[0].data[0][i_wlen]
    data_raytrace = raytrace_file[0].data[0][i_wlen]
    mono_file.close()
    raytrace_file.close()

    data = data_mono + data_raytrace
    if (not os.path.isfile(results_dir + simulation_name + '_mono_continuum_map_total.fits.gz')):
        hdu = fits.PrimaryHDU(data)
        hdul = fits.HDUList([hdu])
        hdul.writeto(results_dir + simulation_name + '_mono_continuum_map_total.fits.gz')

    del data_raytrace
    del data_mono

    dir = u.make_dir(visibility_dir, star_name)

    filename = dir + 'visibilities_' + simulation_name + star_name + '.csv';
    with open(filename, 'w') as fd:
        writer = csv.writer(fd, delimiter=",", lineterminator='\n')
        writer.writerow(np.concatenate([['baseline'], wlen]))
        writer.writerow(np.concatenate([[0], [1] * len(wlen)]))
        for i in range(5, 205, 5):
            visibility, phases, maps = it.get_visibility_2D(np.array([0]), np.array([i]), wlen, data, map_rad)
            writer.writerow(np.concatenate([[i], visibility[:, 0]]))

    del data
    # plot_visibility(filename, wlen, star_name)


def plot_visibility(simulation_names, labels, i_wlen, wlen, star_name, title="Visibilities for different wavelenghts"):
    vis_dir = u.make_dir(visibility_dir, star_name)
    fig_dir = u.make_dir(figures_dir, star_name)



    for k in range(len(simulation_names)):
        simulation_name = simulation_names[k]
        label = labels[k]
        bands = [[]] * (len(i_wlen))
        x = np.empty(0)
        filename = vis_dir + 'visibilities_' + simulation_name + star_name + '.csv';
        with open(filename, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=",", lineterminator='\n')
            next(reader)
            for row in reader:
                x = np.append(x, [float(row[0])])
                for i in range(len(i_wlen)):
                    bands[i] = np.append(bands[i], [float(row[i_wlen[i]+1])])

        for j in range(len(i_wlen)):
            plt.plot(x, bands[j], label=label)

    plt.grid(b=True, which='major', color='b', linestyle='--', alpha=0.2)
    plt.xticks(np.arange(0, 200, step=20))
    plt.xlabel('Baseline ($m$)')
    plt.xlim([0, 200])
    plt.ylabel('Visibility')
    plt.ylim([0, 1])
    plt.legend()
    plt.savefig(fig_dir + u.clean_filename(title) + ".png")

    plt.title(title)
    plt.savefig(u.make_dir(fig_dir, 'title') + u.clean_filename(title) + ".png")

def plot_visibility_for_baseline(simulation_names, labels, star_name, baseline, wlen=[]):
    vis_dir = u.make_dir(visibility_dir, star_name)

    for k in range(len(simulation_names)):
        simulation_name = simulation_names[k]
        label = labels[k]
        ln = np.empty(0)
        filename = vis_dir + 'visibilities_' + simulation_name + star_name + '.csv';
        if os.path.isfile(filename):
            data = np.genfromtxt(filename, delimiter=",")
            index = np.where(data[:, 0]==baseline)
            x = data[0, 1:]
            for l in wlen:
                index2 = np.where(data[0, :]==l)
                ln = np.append(ln, data[index, index2])
            y = data[index, 1:][0][0]
            plt.plot(x, y, label = label)
            plt.plot(wlen, ln, '--')
        else:
            print("Warning! File not found: " + filename)

def plot_visibility_for_wavelength(simulation_names, labels, star_name, wlen):
    vis_dir = u.make_dir(visibility_dir, star_name)

    for k in range(len(simulation_names)):
        simulation_name = simulation_names[k]
        label = labels[k]

        filename = vis_dir + 'visibilities_' + simulation_name + star_name + '.csv';
        if os.path.isfile(filename):
            data = np.genfromtxt(filename, delimiter=",")
            index = np.where(data[0, :]==wlen)
            x = data[1:, 0]
            y = data[1:, index[0][0]]
            print(x, y)
            plt.plot(x, y, label = label)
    else:
        print("Warning! File not found: " + filename)

def plot_brightness(simulation_names, labels, i_wlen, title="Monochromatic flux"):
    fig = plt.figure()
    xi = np.linspace(-5, 5, 100)
    date_dir = u.make_dir(figures_dir, 'brightness')

    for i in range(len(simulation_names)):
        simulation_name = simulation_names[i]
        mono_file = fits.open(results_dir + simulation_name + '_mono_continuum_map_mono.fits.gz')
        raytrace_file = fits.open(results_dir + simulation_name + '_mono_continuum_map_raytrace.fits.gz')
        data_mono = mono_file[0].data[0][i_wlen]
        data_raytrace = raytrace_file[0].data[0][i_wlen]
        mono_file.close()
        raytrace_file.close()
        data = data_mono + data_raytrace

        del data_raytrace
        del data_mono
        data = data * u.get_factor(simulation_name)
        plt.semilogy(xi, data[200][150:250], '-o', label=labels[i])
        plt.axhline(1e-2 * np.max(data), color="black")
        plt.text(-5, 1e-2 * np.max(data), "1:100 " + labels[i], color="black", weight="bold", ha="left", va="bottom", fontsize=12)
        del data

    plt.ylim(bottom=1)
    plt.xlim([-5, 5])
    plt.xlabel('$\\rm{x [AU]}$')
    plt.ylabel('$\\rm{S [Jy/arcsec^{2}]}$')
    plt.xticks(np.linspace(-5, 5, 11))
    plt.legend()

    num = uuid.uuid4()
    plt.savefig(date_dir + u.clean_filename(title) + num + ".png")
    plt.title(title)

    plt.savefig(u.make_dir(date_dir, 'title') + u.clean_filename(title) + num + ".png")


def plot_brightness_2D(
        simulation_names,
        labels,
        i_wlen,
        title="Monochromatic flux for two different star luminosities at $\\rm{\lambda =%s \mu m}$",
        bins=100
    ):

    n = len(simulation_names)//2
    fig, axs = plt.subplots(ncols=2, nrows=n, sharex=True, sharey=True, subplot_kw={'aspect':'equal', 'autoscale_on' : True})
    xi = np.linspace(-5, 5, 100)
    dir = u.make_dir(figures_dir, 'brightness_2D')

    for i in range(len(simulation_names)):
        simulation_name = simulation_names[i]
        mono_file = fits.open(results_dir + simulation_name + '_mono_continuum_map_mono.fits.gz')
        raytrace_file = fits.open(results_dir + simulation_name + '_mono_continuum_map_raytrace.fits.gz')
        data_mono = mono_file[0].data[0][i_wlen]
        data_raytrace = raytrace_file[0].data[0][i_wlen]
        mono_file.close()
        raytrace_file.close()
        data = data_mono + data_raytrace

        del data_raytrace
        del data_mono
        data = data * u.get_factor(simulation_names[i])
        im = axs[i//2, i % 2].contourf(xi, xi, data[150:250, 150:250], locator=ticker.MaxNLocator(bins))
        axs[i//2, i % 2].set_title(labels[i])
        axs[i // 2, i % 2].set_ylabel('$y [\\rm{AU}]$')
        axs[i // 2, i % 2].set_ylabel('$x [\\rm{AU}]$')
        del data

    # COLORBAR
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    clb_ax.set_title('$\\rm{S [Jy/arcsec^{2}]}$')

    num = str(uuid.uuid4())
    fig.savefig(dir + u.clean_filename(title) + num + ".png")
    fig.suptitle(title)
    fig.savefig(u.make_dir(dir, 'title') + u.clean_filename(title) + num + ".png")

def plot_temperatures(simulation_names, labels, title="Temperature profiles"):
    dir = u.make_dir(figures_dir, 'temperatures')
    plt.figure()
    xi = np.linspace(0, 200, 100)
    for i in range(len(simulation_names)):
        simulation_name = simulation_names[i]
        plt.semilogy(xi, get_t_profile(simulation_name), label=labels[i])


    plt.xlabel('$x [\\rm{AU}]$')
    plt.ylabel('$T [\\rm{K}]$')
    plt.legend()
    num = str(uuid.uuid4())
    plt.savefig(dir + u.clean_filename(title) + num + ".png")
    plt.suptitle(title)
    plt.savefig(u.make_dir(dir, 'title') + u.clean_filename(title) + num + ".png")



def get_t_profile(simulation_name):
    data = np.genfromtxt(results_dir + simulation_name + '_temp_n_cut_x.dat')
    n_dust = int((data.shape[1] - 9) / 2)
    init = data.shape[0] // 2 + 1

    return data[init:, 5 + n_dust]

