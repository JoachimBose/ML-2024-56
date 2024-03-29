#!/bin/bash
# Purpose:  Script to run the project code
# Usage:    ./run.sh (flags)
# Default:  Compiles and sets up the dataset, and/or does the evolution
# ---------------------------------------

compile=true
evolution=false
final=false
tests="all"

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo " -d   Disable the compilation & friends"
    echo " -e   Start evolving"
    echo " -s   Set which tests to use"
    echo " -h   Display this help message"
}

while getopts "s:dehpf" flag; do
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
        p) # paramter modeling
            param=true
        ;;
        f) # final modeling
            final=true
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

if [ "$param" = true ];
then
    # Create base files
    python3 core/compile.py all size &> /dev/null

    # Create Training, Validation and Test datasets
    python3 -m core.llvm_passes.create_dataset aoc
    python3 -m core.llvm_passes.create_dataset aocvalid
    python3 -m core.llvm_passes.create_dataset aoctest

    # Create PCA'd datasets
    python3 core/pca.py
    python3 core/pca.py validation
    python3 core/pca.py testing

    # Create all the models
    for gen in 5 10 15
    do
        for sol in 4 8 12 16
        do
            for par in 2 4 6 8 10
            do
                python3 -m core.evolution.evolution_master $sol $gen $par 
            done    
        done    
    done

    # Validate the models
    python3 -m core.evolution.validation_assesser

    # Combine the results
    python3 -m core.evolution.performance_combiner
fi

if [ "$final" = true ];
then
    # Create base files
    python3 core/compile.py all size &> /dev/null

    # Create Training, Validation and Test datasets
    python3 -m core.llvm_passes.create_dataset final
    python3 -m core.llvm_passes.create_dataset aoctest

    # Create PCA'd datasets
    python3 core/pca.py final
    python3 core/pca.py testing

    python3 -m core.evolution.evolution_master 16 10 4

    # Validate the models
    python3 -m core.evolution.final_assesser

fi