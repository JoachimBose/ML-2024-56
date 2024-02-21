sudo cp /etc/apt/sources.list /etc/apt/sources.backup
echo deb http://apt.llvm.org/jammy/ llvm-toolchain-jammy-17 main | sudo tee -a /etc/apt/sources.list
echo deb-src http://apt.llvm.org/focal/ llvm-toolchain-focal-17 main | sudo tee -a /etc/apt/sources.list

wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
sudo apt update && sudo apt upgrade
sudo apt-get install libllvm17 llvm-17 llvm-17-dev llvm-17-doc llvm-17-examples\
    llvm-17-runtime libedit-dev libzstd-dev libcurl4-gnutls-dev libstdc++-12-dev