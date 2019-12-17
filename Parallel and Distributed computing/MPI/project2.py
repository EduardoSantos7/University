"""
@Author: Eduardo Luis Santos Delgado
@Description: Parallel MPI Sparse Matrix Compression

This script read a matrix from a file and
use multiple processes to create a list with
the non zero values and its position.

Input:

2 7 0
3 0 1

Output (value, pos_x, pos_y):

(2, 0, 0)
(7, 0, 1)
(3, 1, 0)
(1, 1, 2)
"""

import numpy as np

from mpi4py import MPI


comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
procesess = comm.Get_size()

# Master process
MASTER = 0


def read_data():
    data = []
    with open('input.txt', 'r') as opened_file:
        for line in opened_file:
            # Casting each number in the row
            row = np.array([int(n) for n in line.split()])
            # Save the row as part of the general data
            data.append(row)

    return np.array(data)


def formated_out(out):
    for row in out:
        for val_ref in row:
            print(f'({val_ref[0]}, {val_ref[1]}, {val_ref[2]})')


if my_rank == MASTER:

    data = read_data()
    rows = len(data)
    min_chunk_size = rows // (procesess - 1)
    result = []

    for i in range(1, procesess):
        start = (i-1)*min_chunk_size
        pre_offset = start + min_chunk_size
        offset = start + min_chunk_size if pre_offset + min_chunk_size < rows else rows
        # subset contains a subset of the original list
        subset = data[start: offset]

        comm.send(start, dest=i, tag=i)
        comm.send(subset, dest=i, tag=i)

    for source in range(1, procesess):
        # TThe order is not really important, but I'll keep it.
        subset = comm.recv(source=source)
        result.extend(subset)

    result = np.array(result)

    formated_out(result)

if my_rank != MASTER:
    start = comm.recv(source=MASTER, tag=my_rank)
    subset = comm.recv(source=MASTER, tag=my_rank)

    new_subset = []
    for row in subset:

        new_row = []

        # Attach the position structure: [value, x, y]
        for j, element in enumerate(row):
            new_elem = np.array([row[j], start, j])
            new_row.append(new_elem)

        new_row = np.array(new_row)

        start += 1

        # Delete the elements which the value is 0
        new_row = new_row[new_row[:, 0] != 0]
        new_subset.append(new_row)

    new_subset = np.array(new_subset)

    # Return the new subset to MASTER
    comm.send(new_subset, dest=MASTER, tag=my_rank)

MPI.Finalize()
