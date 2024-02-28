#!/bin/bash
# Purpose:  Script to setup the docker container and/or enter it
# Usage:    ./setup.sh (flags)
# Default:  Checks if docker exists and is running, if not creates/starts it
# ---------------------------------------

force_build=false
enter=false

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo " -b   Force a rebuild of the docker"
    echo " -d   Disable detached start"
    echo " -h   Display this help message"
}

enter_container() {
    echo "[--] Entering container..."
    docker exec -it machine-learning /bin/bash
    exit 0
}

while getopts ":beh" flag; do
    case $flag in
        b) # Force a rebuild
            force_build=true
        ;;
        e) # Enter the docker
            enter=true
        ;;
        h) # Display usage
            usage
            exit 0
        ;;
    esac
done

# Sanity check; is docker & co installed?
if ! command -v docker &> /dev/null | command -v docker-compose &> /dev/null; 
then
    echo "[:(] docker and/or docker-compose is not installed."
    exit 1
fi

if [ "$force_build" == false ] && \
    docker-compose ps --filter State=Up | grep "machine-learning" &> /dev/null;
then
    [ "$enter" == true ] && enter_container
    echo "[:(] Container is already running, did you mean to run with -e?"
    exit 0
fi

# Build and start the docker container
echo "[--] Building container, may take a while..."
docker-compose build &> /dev/null
echo "[:)] Docker container built!"
echo "[--] Starting container..."
docker-compose up -d &> /dev/null
echo "[:)] Docker container up & running!"

[ "$enter" == true ] && enter_container

# ---------------------------------------
# bare-metal install, left in for now
# ---------------------------------------

# sudo cp /etc/apt/sources.list /etc/apt/sources.backup
# echo deb http://apt.llvm.org/jammy/ llvm-toolchain-jammy-17 main \
#     | sudo tee -a /etc/apt/sources.list
# echo deb-src http://apt.llvm.org/focal/ llvm-toolchain-focal-17 main \
#     | sudo tee -a /etc/apt/sources.list

# # wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
# # sudo apt update && sudo apt upgrade
# sudo apt-get install libllvm17 llvm-17 llvm-17-dev llvm-17-doc \
#     llvm-17-examples llvm-17-runtime libedit-dev libzstd-dev \
#     libcurl4-gnutls-dev libstdc++-12-dev clang-17 
