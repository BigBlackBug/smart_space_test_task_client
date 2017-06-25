import random
import sys
from argparse import ArgumentParser

import client


def _make_matrix(rows, cols, generator=lambda: random.randint(1, 10)):
    return [[generator() for i in range(cols)] for j in
            range(rows)]


def _generate_matrices(max_size):
    print("Generating matrices")
    rows_1 = random.randint(0, max_size)
    cols_1 = random.randint(0, max_size)
    rows_2 = cols_1
    cols_2 = random.randint(0, max_size)

    d_1 = (rows_1, cols_1)
    d_2 = (rows_2, cols_2)
    print("Submitting matrix multiplication {}x{} to {}x{}".format(*d_1, *d_2))
    return _make_matrix(*d_1), _make_matrix(*d_2)


if __name__ == '__main__':
    parser = ArgumentParser(description='Multiply matrices')
    parser.add_argument("-n", type=int, default=5,
                        help="The number of pairs of matrices to multiply")
    parser.add_argument("-s", "--size", type=int, default=50,
                        help="Maximum matrix size")
    args = parser.parse_args()
    if args.n < 1:
        print("N must be greater than 0")
        sys.exit(0)
    if args.size < 1:
        print("Size must be greater than 0")
        sys.exit(0)
    for i in range(args.n):
        first, second = _generate_matrices(args.size)
        job_id = client.multiply(first, second)
        print("Job ID: {}\n".format(job_id))
        client.poll(job_id, sleep_time=1)
        print("-------------------------------------")
