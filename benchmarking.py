#!/usr/bin/env python3
import argparse
import subprocess
import importlib
import cProfile
import pstats
import resource


def run_program(program):
    subprocess.run(program)


def get_usage():
    return resource.getrusage(resource.RUSAGE_CHILDREN)


def get_run_time(usage):
    res = "Run-time: " + str(usage.ru_utime) + 's'
    return res


def get_memory(usage):
    res = "Memory usage: " + str(usage.ru_maxrss // 1024) + "KB"
    return res


def get_num_funcs(program):
   src = program[0]
   compile_target_file = compile(open(src,"rb").read(), src, 'exec')
   pr = cProfile.Profile()
   pr.enable()
   pr.run(compile_target_file)
   pr.disable()
   ps = pstats.Stats(pr)
   ps.print_stats(src[2:])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", action='store_true', help='outputs\
                outputs the memory allocation of the target program')
    parser.add_argument("-t", action='store_true', help='outputs\
                the execution time (run-time) of the target program', default=True)
    parser.add_argument("-n", action='store_true', help='outputs\
                outputs the number of function calls of the target program')
    parser.add_argument('program', nargs='+', type=str)
    arg = parser.parse_args()
    if arg.m:
        run_program(arg.program)
        usage = get_usage()
        print(get_memory(usage))
    elif arg.n:
        get_num_funcs(arg.program)
    elif arg.t:
        run_program(arg.program)
        usage = get_usage()
        print(get_run_time(usage))


if __name__ == "__main__":
    main()
