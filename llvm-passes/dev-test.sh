cd ./build
make
cd ..
opt-17 -load-pass-plugin ./build/libFeatExtr.so -passes=feat-extr ./2mm.ll -S -disable-output