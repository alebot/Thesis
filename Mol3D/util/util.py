import sys
import re
import fileinput


def replace(input_file, name, value):
    for line in fileinput.input(input_file, inplace=1):
        if name in line:
            line = re.sub(r'{.*}', '{' + str(value) + '}', line)
        sys.stdout.write(line)
    fileinput.close()