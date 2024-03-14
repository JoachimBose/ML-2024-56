import os
import sys
import subprocess
import logging
from config import potential_passes
from pathlib import Path

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

test_dir = "./test/PolyBenchC/"
util_dir = "./test/PolyBenchC/utilities/"
aoc_dir = "./test/AoC"
cache_dir = "./test/Cache/"
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

poly_files = [os.path.basename(f) for f in os.listdir(test_dir)]
poly_files.remove("utilities")
aoc_files = [Path(file).stem for file in os.listdir(aoc_dir) if file.endswith(".c")]
all_files = poly_files + aoc_files

def get_passes():
    return potential_passes


def generate_llvm(test):
    out_file = f"{cache_dir}{test}.ll"
    if os.path.exists(out_file):
        logging.debug(f"Already cached: {test}.ll")
        return
    try:
        if test in list(poly_files):
            logging.debug(f"""Running {' '.join([ 
                "./gen_llvm.sh",
                util_dir,
                test_dir,
                test,
                out_file,
            ])}""")
            process = subprocess.run(
                [
                    "./gen_llvm.sh",
                    util_dir,
                    test_dir,
                    test,
                    out_file,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            output = process.stdout
            logging.debug(f"gen_llvm.sh output:\n{output}")
        else:
            input_file = f"{aoc_dir}/{test}.c"
            process = subprocess.run(
                [
                    "clang-17",
                    "-S",
                    "-emit-llvm",
                    "-O",
                    "-Xclang",
                    "-disable-llvm-passes",
                    input_file,
                    "-o",
                    out_file,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            output = process.stdout
            logging.debug(f"AoC clang-17 output:\n{output}")
    except subprocess.CalledProcessError as e:
        logging.debug(f"Error occurred: {e}")
    logging.debug(f"Generated: {test}.ll")


def do_or_cache(test, test_type, args):
    generate_llvm(test)
    out_file = f"{cache_dir}{test}-{test_type}.bc"
    if os.path.exists(out_file):
        logging.debug(f"Cached: {test}-{test_type}.bc")
        logging.info(f"{test}~{test_type}: {os.stat(out_file).st_size}")
        return
    try:
        logging.debug(f"""running: {' '.join(["./gen_bc.sh",
                                            args, f"{cache_dir}{test}.ll",
                                            out_file])}""")
        process = subprocess.run(
            ["./gen_bc.sh", args, f"{cache_dir}{test}.ll", out_file],
            check=True,
            capture_output=True,
            text=True,
        )
        output = process.stdout
        logging.debug(f"gen_bc.sh output:\n{output}")
    except subprocess.CalledProcessError as e:
        logging.debug(f"ERROR OCCURRED: {e}")
        logging.debug("==================== STDERR:")
        logging.debug(process.stderr)

    logging.debug(f"Compiled: {test}-{test_type}.bc")
    logging.info(f"{test}-{test_type}: {os.stat(out_file).st_size}")


def bad_usage():
    print("bad usage, see examples:")
    print("python3 compile.py <clean>")
    print("clean: clean, clean-bc")
    print("python3 compile.py <target> <passes>")
    print("target: all, poly, aoc, <test>")
    print("passes: llvm, size, none, <pass binary>")
    print("pass binary length: ", len(potential_passes))
    exit(0)

def get_args(test_type):
    options = []
    for i, c in enumerate(test_type):
        if int(c):
            options.append(potential_passes[i])
    args = ",".join(options)
    return args

if __name__ == "__main__":

    if sys.argv.__len__() < 2:
        bad_usage()

    if sys.argv[1] == "clean":
        for file in os.listdir(cache_dir):
            os.remove(f"{cache_dir}{file}")
        exit(0)
    if sys.argv[1] == "clean-bc":
        for file in os.listdir(cache_dir):
            if file.endswith(".bc"):
                os.remove(f"{cache_dir}{file}")
        exit(0)

    if sys.argv.__len__() < 3:
        bad_usage()

    test_target = sys.argv[1]
    test_type = sys.argv[2]

    if test_target not in ["all", "poly", "aoc"] + all_files:
        bad_usage()
    if test_type not in ["llvm", "size", "none"] and (
        len(test_type) != len(potential_passes) or not test_type.isnumeric()
    ):
        bad_usage()

    if test_type == "llvm":
        if test_target == "all":
            for test in all_files:
                generate_llvm(test)
        elif test_target == "poly":
            for test in poly_files:
                generate_llvm(test)
        elif test_target == "aoc":
            for test in aoc_files:
                generate_llvm(test)
        else:
            generate_llvm(test_target)
        exit(0)

    if test_type == "size":
        args = "default<Os>"
    elif test_type == "none":
        args = ""
    else:
        args = get_args(test_type)

    if test_target == "all":
        for test in all_files:
            do_or_cache(test, test_type, args)
    elif test_target == "poly":
        for test in poly_files:
            do_or_cache(test, test_type, args)
    elif test_target == "aoc":
        for test in aoc_files:
            do_or_cache(test, test_type, args)
    else:
        do_or_cache(test_target, test_type, args)
