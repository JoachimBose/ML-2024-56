import os
import sys
import subprocess
import logging
from config import potential_passes

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
    "loop-simplify,loop-rotate",
    "instcombine",
    "instsimplify",
    "loop-vectorize",
    "adce",
    "reassociate",
    "loop-instsimplify",
]

def get_passes():
    return potential_passes


def generate_llvm(test):
    out_file = f"{cache_dir}{test}.ll"
    if os.path.exists(out_file):
        logging.debug(f"Already cached: {test}.ll")
        return
    try:
        logging.debug(f"""Running {' '.join([ 
                "./gen_llvm.sh",
                util_dir,
                test_dir,
                test,
                compile_args[test],
                out_file,
            ])}""")
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
    print(
        "bad usage, see examples:\npython3 compile.py clean\npython3 compile.py <target> <passes>"
    )
    print("target: all, <test>")
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

    if sys.argv.__len__() < 3:
        bad_usage()

    test_target = sys.argv[1]
    test_type = sys.argv[2]

    if test_target not in ["all"] + list(compile_args.keys()):
        bad_usage()
    if test_type not in ["llvm", "size", "none"] and (
        len(test_type) != len(potential_passes) or not test_type.isnumeric()
    ):
        bad_usage()

    if test_type == "llvm":
        if test_target == "all":
            for test in compile_args:
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
        for test in compile_args:
            do_or_cache(test, test_type, args)
    else:
        do_or_cache(test_target, test_type, args)
