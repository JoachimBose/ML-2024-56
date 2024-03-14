import os
import sys
import subprocess
import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

# Making implicit assumption that the Cache Directory exists and contains the relevant ll files already
# generated by "python3 compile.py all llvm" and "python3 compile.py all size"

version = "poly"  # "poly" or "aoc" or "all"

cache_dir = "../core/test/Cache/"
tests_dir = "../core/test/PolyBenchC/"
aoc_dir = "../core/test/AoC/"
test_names = []
if version == "poly" or version == "all":
    test_names += [os.path.basename(f) for f in os.listdir(tests_dir)]
    test_names.remove("utilities")
if version == "aoc" or version == "all":
    test_names += [Path(f).stem for f in os.listdir(aoc_dir) if f.endswith(".c")]

features = [
    "nBasicBlocks",
    "nConditionalJMPs",
    "nInsts",
    "nFPInsts",
    "nIntInsts",
    "nLoads",
    "nStores",
    "ratioFloatIntInsts",
    "intrinsicFunctions",
    "functions",
]
columns = ["test"] + features + ["target-size"]

if __name__ == "__main__":
    dataset_path = "../dataset.csv"
    extracted_features = pd.DataFrame(columns=columns)

    for test in test_names:
        test_file_raw = f"{cache_dir}{test}.ll"
        test_file_size = f"{cache_dir}{test}-size.bc"
        process = subprocess.run(
            ["./dev-test.sh", test_file_raw],
            check=True,
            capture_output=True,
            text=True,
        )
        output = process.stderr
        logging.debug(f"dev-test.sh output:\n{output}")
        output_vals = [float(val) for val in output.split(",")]
        if len(output_vals) != len(features):
            logging.error(
                f"Error extracting features for {test} - length of features mismatch.\nExpected: {len(features)}, Got: {len(output_vals)}\n"
            )
            continue
        logging.info(f"Extracted features for {test}: {output_vals}")
        target_size = os.stat(test_file_size).st_size
        row = [test] + output_vals + [target_size]

        extracted_features = extracted_features._append(
            pd.Series(row, index=columns), ignore_index=True
        )

    extracted_features.to_csv(dataset_path, encoding="utf-8", index=False)
    logging.info(f"Data written to {dataset_path}")
