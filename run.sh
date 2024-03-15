#!/bin/bash

cd core/
python3 compile.py clean
python3 compile.py all size &> /dev/null
python3 llvm-passes/create_dataset.py
python3 pca.py all
