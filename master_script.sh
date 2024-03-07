#!/bin/bash

cd core
python3 compile.py clean
python3 compile.py all llvm 
python3 compile.py all size &> /dev/null

cd ../llvm-passes
python3 create_dataset.py