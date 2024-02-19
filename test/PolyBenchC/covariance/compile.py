import os
import sys
import subprocess

if sys.argv.__len__() < 2:
    print("missing argument")
    exit(1)

args = sys.argv[2:]

subprocess.call(
    ["clang-17"] + args + ["-I../utilities", "-lm", "correlation.c", "correlation.h", "../utilities/polybench.c", "../utilities/polybench.h"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

if sys.argv[1] == "time":
    result = subprocess.run(
        ["/usr/bin/time", "./a.out"],
        capture_output=True,
        text=True
    )

    print(float(result.stderr.splitlines()[0].split("user")[0]))
elif sys.argv[1] == "size":
    print(os.stat("./a.out").st_size)
else:
    print("invalid test type")