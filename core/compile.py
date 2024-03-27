import os
import sys
import subprocess
import logging
from pathlib import Path
from main.config import *

# LOGGING LEVEL
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Make sure we're running in the file dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

FILES = {
    "poly": (
        poly := [
            os.path.basename(f) for f in os.listdir(POLY_DIR) if not "utilities" in f
        ]
    ),
    "aoc": (
        aoc := [Path(file).stem for file in os.listdir(AOC_DIR) if file.endswith(".c")]
    ),
    "all": (aoc + poly),
}


def generate_llvm(test: str) -> None:
    out_file = f"{CACHE_DIR}{test}.ll"

    if os.path.exists(out_file):
        logging.debug(f"Already cached: {test}.ll")
        return
    
    try:
        if test in list(FILES["poly"]):
            args = ["./gen_llvm.sh", UTIL_DIR, POLY_DIR, test, out_file]

            logging.debug(f"Running {' '.join(args)}")
            process = subprocess.run(
                args,
                check=True,
                capture_output=True,
                text=True,
            )
            output = process.stdout
            logging.debug(f"gen_llvm.sh output:\n{output}")
        else:
            input_file = f"{AOC_DIR}/{test}.c"
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


def do_or_cache(test: str, test_type: str, args: str) -> None:
    generate_llvm(test)
    out_file = f"{CACHE_DIR}{test}-{test_type}.bc"
    
    if os.path.exists(out_file):
        logging.debug(f"Cached: {test}-{test_type}.bc")
        logging.info(f"{test}~{test_type}: {os.stat(out_file).st_size}")
        return

    try:
        args = ["./gen_bc.sh", args, f"{CACHE_DIR}{test}.ll", out_file]
        logging.debug(f"running: {' '.join(args)}")
        
        process = subprocess.run(
            args,
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


def bad_usage() -> None:
    print("bad usage, see examples:")
    print("python3 compile.py <clean>")
    print("clean: clean, clean-bc")
    print("python3 compile.py <target> <passes>")
    print("target: all, poly, aoc, <test>")
    print("passes: llvm, size, none, <pass binary>")
    print("pass binary length: ", len(POTENTIAL_PASSES))
    sys.exit(0)


def get_args(test_type: str) -> str:
    if test_type == "size":
        return "default<Os>"
    if test_type == "none":
        return ""

    options = []
    for i, c in enumerate(test_type):
        if int(c):
            options.append(POTENTIAL_PASSES[i])
    args = ",".join(options)
    return args


def clean(files_to_clean: list[str]) -> None:
    for file in files_to_clean:
        os.remove(f"{CACHE_DIR}{file}")
    sys.exit(0)


def main(argv: list[str]) -> None:
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if len(argv) < 2:
        bad_usage()
    elif len(argv) < 3:
        if argv[1] == "clean":
            clean(os.listdir(CACHE_DIR))
        if argv[1] == "clean-bc":
            clean([f for f in os.listdir(CACHE_DIR) if ".bc" in f])
        bad_usage()

    test_target = argv[1]
    test_type = argv[2]

    if (test_target not in ["all", "poly", "aoc"] + FILES["all"]) or (
        test_type not in ["llvm", "size", "none"]
        and (len(test_type) != len(POTENTIAL_PASSES) or not test_type.isnumeric())
    ):
        bad_usage()

    if test_type == "llvm":
        if test_target in FILES:
            for test in FILES[test_target]:
                generate_llvm(test)
        else:
            generate_llvm(test_target)
        sys.exit(0)

    args = get_args(test_type)
    if test_target in FILES:
        for test in FILES[test_target]:
            do_or_cache(test, test_type, args)
    else:
        do_or_cache(test_target, test_type, args)


if __name__ == "__main__":
    main(sys.argv)
