import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from util.constants import *
import util.common as cmn
import util.util as u

plt.style.use("classic")
plt.rcParams.update(pgf_with_latex)
files = [
    "input/DRTau/Visibility_2004-12-31_cal.dat",
    "input/DRTau/Visibility_2013-10-20_cal.dat"
]
wlen=8.257153
wlen_array = [8.257153, 11.12258, 13.75993]

suptitle = "Visbility per baseline"
title = "$\lambda =%s \, $" % wlen

plot_type_1 = False
plot_type_2 = True

if (plot_type_1):
    star_name = "CTau"
    baseline = 60
    simulation_names = np.empty(0)
    labels =np.empty(0)
    for r_in in [1, 3]:
        for star_luminosity in [5]:
            for star_temperature in [3900, 9000]:
                simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
                simulation_names = np.append(simulation_names, simulation_name)
                labels = np.append(labels, '$R_{\\rm{in}}=%s, \, T=%s \\rm{K}$' % (str(r_in), str(star_temperature)))



    # 0 - wavelength in micrometers
    # 2 - visibility
    # 3 - uncertainty in visibility
    plt.figure(1)
    for file in files:
        data = np.loadtxt(root_dir + file, dtype=float)
        x = data[:, 0]
        y = data[:, 2]
        y_error = data[:,3]
        #plt.errorbar(x, y, yerr=y_error)
    cmn.plot_visibility_for_wavelength(simulation_names, labels, star_name, wlen)
    plt.xlabel("baseline [m]")
    plt.ylabel("Visibility")
    plt.title("Visibility per baseline $ \lambda =%s \\rm{\\mu m} \, , L = 5 \, \\rm{L_{\odot}} $" % str(wlen))
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.legend(loc='best')


    plt.show()
    plt.savefig(u.clean_filename("baseline.png"))

    plt.figure(2)
    cmn.plot_visibility_for_baseline(simulation_names, labels, star_name, baseline)

    plt.xlabel("wavelength $\\rm{[ \mu m]}$")
    plt.ylabel("Visibility")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.legend(loc='best')
    plt.title("Visibilty per wavelength $ baseline = %s \\rm{m} \, , L = 5 \, \\rm{L_{\odot}} $" % baseline)
    plt.show()
    plt.savefig(u.clean_filename("wavelength.png"))

if (plot_type_2):

    star_name = "CTau"
    baseline = 60
    simulation_names = np.empty(0)
    labels =np.empty(0)
    r_in = 3
    star_temperature = 4500
    star_luminosity = 1
    plt.figure(1)
    simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
    simulation_names = np.append(simulation_names, simulation_name)
    for lam in wlen_array:
        labels = ['$\lambda =%s \\rm{[\mu m]}$' % str(lam)]
        cmn.plot_visibility_for_wavelength(simulation_names, labels, star_name, lam)

    plt.xlabel("baseline [m]")
    plt.ylabel("Visibility")
    plt.title("Visibility per baseline $ R_{\\rm{in}}=%s \\rm{AU} \, , L = %s \, \\rm{L_{\odot}}  \, , T = %s \, \\rm{K} $" % (str(r_in), str(star_luminosity), str(star_temperature)))
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.legend(loc='best')


    plt.show()
    plt.savefig(u.clean_filename("baseline.png"))

    plt.figure(2)
    cmn.plot_visibility_for_baseline(simulation_names, labels, star_name, baseline, wlen_array)

    plt.xlabel("wavelength $\\rm{[ \mu m]}$")
    plt.ylabel("Visibility")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.title("Visibilty per wavelength baseline = $ %s \\rm{m} \, R_{\\rm{in}}=%s \\rm{AU} \, , L = %s \, \\rm{L_{\odot}}  \, , T = %s \, \\rm{K} $" % (str(baseline), str(r_in), str(star_luminosity), str(star_temperature)))
    plt.show()
    plt.savefig(u.clean_filename("wavelength.png"))
