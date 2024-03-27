"""Evolution model parameters"""
SOL_PER_POP = 4 # Hyperparameters have been assigned defaulty
NUM_GENERATIONS = 10 # Number of generations.
NUM_PARENTS_MATING = 2 # Number of solutions to be selected as parents in the mating pool.

"""Directory Constants"""
POLY_DIR = "./test/PolyBenchC/"
UTIL_DIR = "./test/PolyBenchC/utilities/"
AOC_DIR = "./test/AoC/"
CACHE_DIR = "./test/Cache/"
OUTPUT_DIR = "./output/"

"""Features extracted"""
FEATURES = [
    "nBasicBlocks",
    "nConditionalJMPs",
    "nInsts",
    "nFPInsts",
    "nIntInsts",
    "nLoads",
    "nStores",
    "ratioFloatIntInsts",
    "intrinsicFunctions",
    "functions",
]

"""Passes for the EA to pick"""
# https://llvm.org/docs/Passes.html#codegenprepare-optimize-for-code-generation
POTENTIAL_PASSES = [
    "adce",
    "aggressive-instcombine",
    "bdce",
    "constraint-elimination",
    "correlated-propagation",
    "div-rem-pairs",
    "dse",
    "early-cse",
    "function(early-cse)",
    "function(instcombine)",
    "function(lower-expect)",
    "function(simplifycfg)",
    "function(sroa)",
    "gvn",
    # "inferattrs",
    "inject-tli-mappings",
    # "inline",
    "instcombine",
    "instsimplify",
    # "ipsccp",
    "jump-threading",
    "indvars",
    "loop-deletion",
    "loop-idiom",
    "loop-unroll-full",
    "loop-distribute",
    "loop-load-elim",
    "loop-mssa(licm)",
    "loop-instsimplify",
    "loop-rotate",
    "loop-simplifycfg",
    "simple-loop-unswitch",
    "loop-sink",
    "loop-unroll",
    "loop-vectorize",
    "lower-constant-intrinsics",
    "memcpyopt",
    "mldst-motion",
    "move-auto-init",
    # "openmp-opt",
    "reassociate",
    # "recompute-globalsaa",
    # "rel-lookup-table-converter",
    # "rpo-function-attrs",
    "sccp",
    "simplifycfg",
    "slp-vectorizer",
    "speculative-execution",
    "sroa",
    "tailcallelim",
    "transform-warning",
    "vector-combine",
    "verify",
]