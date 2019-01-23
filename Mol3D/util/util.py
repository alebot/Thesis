import sys
import re
import fileinput
import time
import os

from util.constants import *
import numpy as np
import csv
import shutil as sh
import os


def replace(input_file, name, value):
    for line in fileinput.input(input_file, inplace=1):
        if name in line:
            line = re.sub(r'{.*}', '{' + str(value) + '}', line)
        sys.stdout.write(line)
    fileinput.close()


def extract(input_file, name):
    value = None
    pattern = re.compile(r'{.*}')
    with open(input_file, 'rt') as in_file:
        for line in in_file:
            if name in line:
                value = pattern.search(line).group()
                value = re.sub('{', '', value)
                value = re.sub('}', '', value)

    return float(value)


def make_date_dir(root_dir):
    directory = root_dir + time.strftime("%Y-%m-%d") + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory

def make_dir(root_dir, dir):
    directory = root_dir + dir + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory

def get_date_dir(root_dir, date=None):
    if date:
        return root_dir + date + "/"
    else:
        return root_dir + time.strftime("%Y-%m-%d") + '/'

def clean_filename(s):
    clean_basename = slugify(os.path.splitext(s)[0])
    clean_extension = slugify(os.path.splitext(s)[1][1:])
    if clean_extension:
        clean_filename = '{}.{}'.format(clean_basename, clean_extension)
    elif clean_basename:
        clean_filename = clean_basename
    else:
        clean_filename = 'none'  # only unclean characters

    return clean_filename

def get_factor(simulation_name):
    input_file = results_dir + simulation_name + '_mono_input_file.dat'
    pixel = extract(input_file, 'n_bin_map')
    distance = extract(input_file, 'distance')
    range = extract(input_file, 'r_ou')/extract(input_file, 'zoom_map')

    return (pixel*2+1)**2 * (distance)**2 / (range*2)**2

def get_param(simlation_name, param):
    input_file = results_dir + simulation_name + '_mono_input_file.dat'

    return extract(input_file, param)

def transform_visibility(simulation_names, star_name):
    for simulation_name in simulation_names:
        vis_dir = make_dir(visibility_dir, star_name)
        filename = vis_dir + 'visibilities_' + simulation_name + star_name + '.csv';
        filename_old = vis_dir + 'visibilities_' + simulation_name + star_name + '_old.csv';
        sh.copyfile(filename, filename_old)
        os.system('rm ' + filename)
        data = np.empty(0)
        with open(filename_old, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=",", lineterminator='\n')
            with open(filename, 'w') as fd:
                writer = csv.writer(fd, delimiter=",", lineterminator='\n')
                for row in reader:
                    string = str.replace(row[1][2:-2], "]", ",")
                    string = str.replace(string, "\n", "")
                    string = str.replace(string, "[", "")
                    array = np.fromstring(string, sep=",", dtype=float)
                    if row[0] == '0':
                        writer.writerow(np.concatenate([[0], [1] * size]))
                    else:
                        writer.writerow(np.concatenate([[row[0]], array]))
                    size = array.size




