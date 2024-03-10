import os
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

test_dir = "./test/PolyBenchC/"
util_dir = "./test/PolyBenchC/utilities/"
aoc_dir = "./test/AoC"
aocpp_dir = "./test/AoCpp"
cache_dir = "./test/Cache/"
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

compile_args = {
    "2mm": "",
    "3mm": "",
    "adi": "",
    "atax": "",
    "bicg": "",
    "cholesky": "-lm",
    "correlation": "-lm",
    "covariance": "-lm",
    "deriche": "-lm",
    "doitgen": "",
    "durbin": "",
    "fdtd-2d": "",
    "floyd-warshall": "",
    "gemm": "",
    "gemver": "",
    "gesummv": "",
    "gramschmidt": "-lm",
    "heat-3d": "-lm",
    "jacobi-1d": "",
    "jacobi-2d": "",
    "lu": "",
    "ludcmp": "",
    "mvt": "",
    "nussinov": "",
    "seidel-2d": "",
    "symm": "",
    "syr2k": "",
    "syrk": "",
    "trisolv": "",
    "trmm": "",
}

aoc_files = [Path(file).stem for file in os.listdir(aoc_dir) if file.endswith(".c")]
aocpp_files = [
    Path(file).stem for file in os.listdir(aocpp_dir) if file.endswith(".cpp")
]


potential_passes = [
    "loop-unroll",
    "sroa,mem2reg",
    "loop-simplify,loop-rotate",
    "instcombine",
    "instsimplify",
    "loop-vectorize",
    "adce",
    "reassociate",
    "licm",
]


def generate_llvm(test, is_cpp=False):
    out_file = f"{cache_dir}{test}.ll"
    if os.path.exists(out_file):
        logging.debug(f"Already cached: {test}.ll")
        return
    try:
        if test in list(compile_args.keys()):
            process = subprocess.run(
                [
                    "./gen_llvm.sh",
                    util_dir,
                    test_dir,
                    test,
                    compile_args[test],
                    out_file,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            output = process.stdout
            logging.debug(f"gen_llvm.sh output:\n{output}")
        else:
            if is_cpp:
                input_file = f"{aocpp_dir}/{test}.cpp"
            else:
                input_file = f"{aoc_dir}/{test}.c"
            process = subprocess.run(
                [
                    "clang-17",
                    "-S",
                    "-O0",
                    "-emit-llvm",
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


def do_or_cache(test, test_type, args, is_cpp=False):
    generate_llvm(test, is_cpp)
    out_file = f"{cache_dir}{test}-{test_type}.bc"
    if os.path.exists(out_file):
        logging.debug(f"Cached: {test}-{test_type}.bc")
        logging.info(f"{test}~{test_type}: {os.stat(out_file).st_size}")
        return
    try:
        process = subprocess.run(
            ["./gen_bc.sh", args, f"{cache_dir}{test}.ll", out_file],
            check=True,
            capture_output=True,
            text=True,
        )
        output = process.stdout
        logging.debug(f"gen_bc.sh output:\n{output}")
    except subprocess.CalledProcessError as e:

        logging.debug(f"Error occurred: {e}")

    logging.debug(f"Compiled: {test}-{test_type}.bc")
    logging.info(f"{test}-{test_type}: {os.stat(out_file).st_size}")


def bad_usage():
    print("bad usage, see examples:")
    print("python3 compile.py <clean>")
    print("clean: clean, clean-bc")
    print("python3 compile.py <target> <passes>")
    print("target: all, <test>")
    print("passes: llvm, size, none, <pass binary>")
    print("pass binary length: ", len(potential_passes))
    exit(0)


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

    if (
        test_target not in ["all"] + list(compile_args.keys())
        and test_target not in aoc_files
    ):
        bad_usage()
    if test_type not in ["llvm", "size", "none"] and (
        len(test_type) != len(potential_passes) or not test_type.isnumeric()
    ):
        bad_usage()

    if test_type == "llvm":
        if test_target == "all":
            for test in compile_args:
                generate_llvm(test)
            for test in aoc_files:
                generate_llvm(test)
            for test in aocpp_files:
                generate_llvm(test, True)
        else:
            if test_target in aocpp_files:
                generate_llvm(test_target, True)
            else:
                generate_llvm(test_target)
        exit(0)

    if test_type == "size":
        args = "default<Os>"
    elif test_type == "none":
        args = ""
    else:
        options = []
        for i, c in enumerate(test_type):
            if int(c):
                options.append(potential_passes[i])
        args = ",".join(options)

    if test_target == "all":
        for test in compile_args:
            do_or_cache(test, test_type, args)
        for test in aoc_files:
            do_or_cache(test, test_type, args)
        for test in aocpp_files:
            do_or_cache(test, test_type, args, True)
    else:
        if test_target in aocpp_files:
            do_or_cache(test_target, test_type, args, True)
        else:
            do_or_cache(test_target, test_type, args)
