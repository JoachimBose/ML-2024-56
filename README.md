# ML-2023-56

Overleaf link: https://www.overleaf.com/8326198222kgpttwgvnzqc#7175f7

## Overview

The development of the llvm pass is done in the `llvm-pass/` directory, whereas
 the other development is done in the `core/` directory.

## Setup

For consistent results, a docker container is provided, which can be built using
 the `setup.sh` script. By default the container gets built and started if not
 existant, otherwise it exits. To run, make sure `docker` and `docker-compose`
 are installed.
