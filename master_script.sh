#!/bin/bash

cd core
python3 compile.py clean
python3 compile.py all size &> /dev/null

cd ../llvm-passes
python3 create_dataset.py

cd ..
python3 pca.py