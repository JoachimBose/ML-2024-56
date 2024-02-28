#!/bin/bash

util_dir="$1"
test_dir="$2"
test="$3"
compile_args="$4"
out_file="$5"

# Generate LLVM IR for all relevant files
echo "clang-17 -S -O0 -emit-llvm -I\"$util_dir\" \"$test_dir$test/$test.c\" ${compile_args} \"${util_dir}polybench.c\""
clang-17 -S -O0 -emit-llvm -I"$util_dir" "$test_dir$test/$test.c" "${compile_args}" "${util_dir}polybench.c"

# Link all generated LLVM IR files into a single file
echo "llvm-link-17 -S -v -o \"$out_file\" *.ll"
llvm-link-17 -S -v -o "$out_file" *.ll

# Remove all generated LLVM IR files
echo "rm *.ll"
rm *.ll
