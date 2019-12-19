"""
@Author: Eduardo Luis Santos Delgado
@Description: Random Matrix Generator

This script can receive the next parameters:

rows: Indicate the number of rows in the matrix.
cols: Indicate the number of columns in the matrix.
start: Indicate the minimum random number.
end: Indicate the maximum random number.
name: Indicate the output file name.

Input:

Without args:
    python3 random_matrix_generator.py
With args example:
    python3 random_matrix_generator.py -n in.txt -r 10 -c 10 -s 1 -e 200

Output: Create a file with the matrix.

"""

import argparse

from numpy.random import seed
from numpy.random import randint
from numpy import savetxt
from numpy import array


parser = argparse.ArgumentParser()

parser.add_argument('-r', '--rows', default=10, type=int)
parser.add_argument('-c', '--cols', default=10, type=int)
parser.add_argument('-s', '--start', default=0, type=int)
parser.add_argument('-e', '--end', default=10, type=int)
parser.add_argument('-n', '--name', default="input.txt")

args = parser.parse_args()

# seed random number generator
seed(1)

matrix = []

for _ in range(args.rows):
    # generate integers
    values = (randint(args.start, args.end, args.cols))
    matrix.append(values)

savetxt(args.name, array(matrix).astype(int), fmt='%i', delimiter=" ")
