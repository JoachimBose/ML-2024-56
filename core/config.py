potential_passes = [
    "loop-unroll",
    "sroa,mem2reg",
    "loop-simplify,loop-rotate",
    "instcombine",
    "instsimplify",
    "loop-vectorize",
    "adce",
    "reassociate",
    "loop-mssa(licm<no-allowspeculation>)",
]