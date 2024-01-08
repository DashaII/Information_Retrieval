import argparse
import parse_data
import run_0
import run_1
from configs import *

# EXAMPLE: python main.py --run=run-1 --full=1
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='run-1', type=str, help='run-0 or run-1')
    parser.add_argument('--full', default=0, type=int, help='0 for reduced list of docs (default), 1 for full list of docs')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parser()
    if args.run == 'run-1' and args.full == 0:
        parse_data.parse_reduced_data_run_1()
        run_1.run(EN, TRAIN)
        run_1.run(EN, TEST)
        run_1.run(CZ, TRAIN)
        run_1.run(CZ, TEST)
    elif args.run == 'run-0' and args.full == 0:
        parse_data.parse_reduced_data_run_0()
        run_0.run(EN, TRAIN)
        run_0.run(EN, TEST)
        run_0.run(CZ, TRAIN)
        run_0.run(CZ, TEST)
    elif args.run == 'run-1' and args.full == 1:
        parse_data.parse_full_data_run_1()
        run_1.run(EN, TRAIN)
        run_1.run(EN, TEST)
        run_1.run(CZ, TRAIN)
        run_1.run(CZ, TEST)
    elif args.run == 'run-0' and args.full == 1:
        parse_data.parse_full_data_run_0()
        run_0.run(EN, TRAIN)
        run_0.run(EN, TEST)
        run_0.run(CZ, TRAIN)
        run_0.run(CZ, TEST)
    else:
        print("incorrect arguments format:\n'--run', default='run-1', type=str, help='run-0 or run-1'\n'--full', default=0, type=int, help='0 by default (reduced list of docs), 1 for full list of docs'")