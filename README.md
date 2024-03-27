# ML-2023-56

Overleaf link: https://www.overleaf.com/8326198222kgpttwgvnzqc#7175f7

## Overview

All the development is done in the `core/` directory, which is organized into
 subdirectories.

## Setup

For consistent results, a docker container is provided, which can be built using
 the `setup.sh` script. By default the container gets built and started if not
 existant, otherwise it exits. To run, make sure `docker` and `docker-compose`
 are installed.

When editing the `.cpp` files in `llvm-passes`, please use for vscode the
 `Clang_format_fallback Style`
 `{ BasedOnStyle: LLVM, IndentWidth: 4, ColumnLimit: 100 }` formatting settings.

## Running
Then, to run the project, use `run.sh` from the root directory. You can use the
 `-e` flag to do the evolution, `-d` to disable the compilation & friends, and
 `-s {tests}` to select which files to use as tests.
