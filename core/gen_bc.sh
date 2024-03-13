#!/bin/bash

args="$1"
test_file="$2"
out_file="$3"

echo "opt-17 -passes=\"$args\" \"$test_file\" -o \"$out_file\""

opt-17 -passes="$args" "$test_file" -o "$out_file"
