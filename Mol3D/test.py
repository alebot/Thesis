import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from util.constants import *
import util.common as cmn

plt.style.use("classic")
plt.rcParams.update(pgf_with_latex)

files = [
    "input/DRTau/Visibility_2004-12-31_cal.dat",
    "input/DRTau/Visibility_2013-10-20_cal.dat"
]
epochs = [
    "31-12-2004",
    "20-10-2013"
]

plt.figure()

star_name = "CTau"
baseline = 60
# simulation_names = np.empty(0)
# labels =np.empty(0)
# for star_name in ["CTau"]:
#     for r_in in [0.1]:
#         for star_luminosity in [1,20]:
#             for star_temperature in [3900, 4500, 5000, 6000, 7000, 8000, 9000]:
#                 simulation_name = star_name + ('Rin=%sL=%sT=%s' % (str(r_in), str(star_luminosity), str(star_temperature)))
#                 simulation_names = np.append(simulation_names, simulation_name)
#                 labels = np.append(labels, '$%s R_{\\rm{in}}=%s,\, L=%s \\rm{L_{\odot}}, \, T=%s \\rm{K}$' % ( star_name, str(r_in), str(star_luminosity), str(star_temperature)))
#     cmn.plot_visibility_for_baseline(simulation_names, labels, star_name, 60)

cmn.plot_visibility_for_baseline(["DTauRin=0.07L=1T=4050"],
    ["Simulation for $R_{\\rm{in}} = 0.07 \\rm{AU}, \, T = 4050 \\rm{K}, L= 1L_{\odot}$"],
    "DTau",
     60)
# simulation_names = np.empty(0)
# labels =np.empty(0)
# for star_name in ["ATau",]:
#     for star_radius in [0.07, 0.1]:
#         simulation_name = star_name + ('R=%sAU' % str(star_radius))
#         simulation_names = np.append(simulation_names, simulation_name)
#         labels = np.append(labels, '$%s R_{\\rm{in}}=%s$' % (star_name, str(star_radius)))
# cmn.plot_visibility_for_baseline(simulation_names, labels, star_name, 60)

# 0 - wavelength in micrometers
# 2 - visibility
# 3 - uncertainty in visibility
for i in range(len(files)):
    file = files[i]
    data = np.loadtxt(root_dir + file, dtype=float)
    x = data[:, 0]
    y = data[:, 2]
    y_error = data[:,3]
    plt.errorbar(x, y, yerr=y_error, label=epochs[i])

plt.xlabel("$\mu m$")
plt.ylabel("Visibility")
plt.grid(b=True, which='major', color='#666666', linestyle='-')

plt.title("DR Tau visibility in MIR at baseline 60 m")
plt.show()
plt.savefig("DRTau.png")
