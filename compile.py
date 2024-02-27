import os
import sys
import subprocess
import time
import logging

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

test_dir = "./test/PolyBenchC/"
util_dir = "./test/PolyBenchC/utilities/"
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

potential_passes = [
    "loop-unroll",
    "sroa,mem2reg",
    "licm",
    "loop-simplify,loop-rotate",
    "early-cse,sink",
    "instcombine",
    "instsimplify",
    "loop-vectorize",
    "adce",
    "reassociate",
]


def generate_llvm(test):
    out_file = f"{cache_dir}{test}.ll"
    if os.path.exists(out_file):
        logging.debug(f"Already cached: {test}.ll")
        return
    try:
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
    except subprocess.CalledProcessError as e:
        logging.debug(f"Error occurred: {e}")
    logging.debug(f"Generated: {test}.ll")


def do_or_cache(test, test_type, args):
    generate_llvm(test)
    out_file = f"{cache_dir}{test}-{test_type}.bc"
    if os.path.exists(out_file):
        logging.debug(f"Cached: {test}-{test_type}.bc")
        print(f"{test}: {os.stat(out_file).st_size}")
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
    print(f"{test}: {os.stat(out_file).st_size}")


if __name__ == "__main__":

    # Getting the test
    if sys.argv.__len__() < 2:
        print("missing target (all or specific test)")
        exit(1)

    # Getting the passes
    if sys.argv.__len__() >= 3:
        test_type = sys.argv[2]
    else:
        test_type = "size"

    gen_llvm = False

    # Constructing the arguments
    if test_type == "llvm":
        gen_llvm = True
    elif test_type == "size":
        args = "default<Os>"
    elif test_type == "none":
        args = ""
    elif len(test_type) == len(potential_passes):
        options = []
        for i, c in enumerate(test_type):
            if int(c):
                options.append(potential_passes[i])
        args = ",".join(options)
    else:
        print("invalid passes")
        exit(1)

    if sys.argv[1] == "all":
        for test in compile_args:
            if gen_llvm:
                generate_llvm(test)
            else:
                do_or_cache(test, test_type, args)
    elif sys.argv[1] in compile_args:
        test = sys.argv[1]
        if gen_llvm:
            generate_llvm(test)
        else:
            do_or_cache(test, test_type, args)
    elif sys.argv[1] == "clean":
        for file in os.listdir(cache_dir):
            if file.endswith(".bc") or file.endswith(".ll"):
                os.remove(f"{cache_dir}{file}")
    else:
        print("invalid test")
        exit(1)
