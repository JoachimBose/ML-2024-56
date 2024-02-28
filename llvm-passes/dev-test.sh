#!/bin/bash
# Purpose:  Script to setup, if needed, and run the test
# Usage:    ./dev-test.sh
# ---------------------------------------

# Setup build dir if not present
if [ ! -d build ];
then
    mkdir build
    cd build
    cmake -DLT_LLVM_INSTALL_DIR=$LLVM_DIR ..
    make
    cd ..
fi

# Make and run test
cd ./build
make
cd ..
opt-17 -load-pass-plugin ./build/lib/libFeatExtr.so -passes=feat-extr ./2mm.ll \
    -S -disable-output
