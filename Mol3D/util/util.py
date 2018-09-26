import sys
import re
import fileinput
import time
import os


def replace(input_file, name, value):
    for line in fileinput.input(input_file, inplace=1):
        if name in line:
            line = re.sub(r'{.*}', '{' + str(value) + '}', line)
        sys.stdout.write(line)
    fileinput.close()


def extract(input_file, name):
    value = None
    for line in fileinput.input(input_file, inplace=1):
        if name in line:
            value = re.search(r'{.*}',line).group(1)
            break
    fileinput.close()

    return value


def make_date_dir(root_dir):
    directory = root_dir + time.strftime("%Y-%m-%d") + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def get_date_dir(root_dir, date=None):
    if date:
        return root_dir + time.strptime(date, "%Y-%m-%d")
    else:
        return root_dir + time.strftime("%Y-%m-%d") + '/'
