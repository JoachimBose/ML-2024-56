add_library(LLVMfeat-extr MODULE feat-extr.cpp)

# this is very important, to link with the passes library
target_link_libraries(LLVMfeat-extr ${llvm_libs})