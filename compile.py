import os
import sys
import subprocess

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

potential_passes = ["-mem2reg -sccp", "-mem2reg -licm", "-adce"]


def do_or_cache(test, test_type, args):
    out_file = f"{cache_dir}{test}-{test_type}.out"
    if os.path.exists(out_file):
        print("Cached: ", test, os.stat(out_file).st_size)
        return
    subprocess.call(
        ["clang-17"]
        + args
        + [
            f"-I{util_dir}",
            f"{test_dir}{test}/{test}.c",
            compile_args[test],
            f"{util_dir}polybench.c",
            "-o",
            f"{out_file}",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("Compiled: ", test, os.stat(out_file).st_size)


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

    # Constructing the arguments
    if test_type == "size":
        args = ["-Os"]
    elif test_type == "none":
        args = []
    elif len(test_type) == len(potential_passes):
        args = []
        for i, c in enumerate(test_type):
            if int(c):
                args.append(potential_passes[i])
    else:
        print("invalid passes")
        exit(1)

    if sys.argv[1] == "all":
        for test in compile_args:
            do_or_cache(test, test_type, args)
    elif sys.argv[1] in compile_args:
        test = sys.argv[1]
        do_or_cache(test, test_type,args )

    else:
        print("invalid test")
        exit(1)
