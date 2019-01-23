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

# plt.rcParams.update(pgf_with_latex)
i_wlen = np.arange(121, 134)
wlen = [8.257153, 8.616133, 8.990722, 9.381597, 9.789465, 10.21506, 10.65917, 11.12258, 11.60613, 12.11072, 12.63723, 13.18664, 13.75993]

star_name = 'MTau'
star_distance = 140
map_rad = (20 * m.pi)/(140 * 648000)

cmn.calculate_visibility('MTauRin=1L=50T=3900',i_wlen, wlen, star_name, map_rad)