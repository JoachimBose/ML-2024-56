# https://llvm.org/docs/Passes.html#codegenprepare-optimize-for-code-generation
potential_passes = [
    "sroa,mem2reg",
    "instcombine",
    "instsimplify",
    "reassociate",
    "early-cse",

    "loop-mssa(licm)",
    # "loop-mssa(loop-instsimplify)",
    # "loop-unroll",
    # "loop-deletion",
    # "loop-vectorize",
    "loop-simplify,loop-rotate",
    "loop-sink",

    "adce",
    "dse",
    "constraint-elimination",
    "gvn",
    "sccp",
]