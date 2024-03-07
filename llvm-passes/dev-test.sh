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

if [ $? -eq 0 ] 
then
    cd ..
    # set up nice stacktrace
    export LLVM_SYMBOLIZER_PATH="/usr/bin/llvm-symbolizer-17"
    
    target_file="$1"

    #load and run
    opt-17 -load-pass-plugin ./build/lib/libFeatExtr.so -passes=feat-extr \
    $target_file -S -disable-output
else
    echo "make returned error, not continueing"
fi


