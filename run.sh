#!/bin/bash
# Purpose:  Script to run the project code
# Usage:    ./run.sh (flags)
# Default:  Compiles and sets up the dataset, and/or does the evolution
# ---------------------------------------

compile=true
evolution=false
tests="all"

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo " -d   Disable the compilation & friends"
    echo " -e   Start evolving"
    echo " -s   Set which tests to use"
    echo " -h   Display this help message"
}

while getopts "s:deh" flag; do
    case $flag in
        s)
            tests="${OPTARG}"
        ;;
        d) # Disable compile
            compile=false
        ;;
        e) # Enable evolution
            evolution=true
        ;;
        h) # Display usage
            usage
            exit 0
        ;;
    esac
done

if [ "$compile" == true ];
then
    python3 core/compile.py clean
    python3 core/compile.py $tests size &> /dev/null
    python3 -m core.llvm_passes.create_dataset $tests
    python3 core/pca.py $tests
fi

if [ "$evolution" = true ];
then
    python3 -m core.evolution.evolution_master
    python3 -m core.evolution.evolution_shapes
    python3 -m core.evolution.plotmaker
fi
