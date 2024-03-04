#include <llvm/IR/LegacyPassManager.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>
#include <llvm/Support/raw_ostream.h>

using namespace llvm;

/**
Features (Printed in order):
  - N-Basic blocks
  - N-Branches
  - N-Total Insts
  - N-FP Insts
  - N-Int Insts
  - Ratio of FP Insts to Int Insts
  - N-Loads
  - N-Stores

TODO:
  - N-Builtin math functions

Look-into:
  - Average MLP per basic block
  - Average ILP per basic block
  - N-Barriers

Skipped (Too Multithreading related):
  - Div-stuff (Where threads diverge; not relevant)
  - N-Divergent Insts
  - N-Insts in divergent regions
  - Ratio of Insts in divergent regions to total Insts
*/

namespace {
class FunctionFeature {
  public:
    virtual void runOnFunction(Function &function) {}
    virtual void printResult() {}
};

class BasicBlockCounter : public FunctionFeature {
    int nBasicBlocks = 0;

  public:
    BasicBlockCounter() {}

    void runOnFunction(Function &function) {
        for (BasicBlock &basicBlock : function) {
            (void)basicBlock;
            nBasicBlocks++;
        }
    }

    void printResult() { errs() << nBasicBlocks << ","; }
};

class InstructionCounter : public FunctionFeature {
    int nInsts = 0;
    int nFPInsts = 0;
    int nIntInsts = 0;
    int rFPtoInt = 0; // float?
    int nLoads = 0;
    int nStores = 0;

  public:
    InstructionCounter() {}

    void runOnFunction(Function &function) {
        for (BasicBlock &basicBlock : function) {
            for (Instruction &instruction : basicBlock) {
                nInsts++;

                nFPInsts += (int)isa<FPMathOperator>(instruction);
                nIntInsts += (int)isa<BinaryOperator>(instruction);
                nLoads += (int)isa<LoadInst>(instruction);
                nStores += (int)isa<StoreInst>(instruction);
            }
        }

        // calculate ratio's here
    }

    void printResult() {
        errs() << nInsts << "," << nFPInsts << "," << nIntInsts << "," << rFPtoInt << ",";
        errs() << nLoads << "," << nStores;
    }
};

class ConditionalJMPCounter : public FunctionFeature {
    int nConditionalJMP = 0;

  public:
    ConditionalJMPCounter() {}

    void runOnFunction(Function &function) {
        for (BasicBlock &basicBlock : function) {
            for (Instruction &instruction : basicBlock) {
                if (auto branchInst = dyn_cast<BranchInst>(&instruction)) {
                    nConditionalJMP += branchInst->isConditional() ? 1 : 0;
                }
            }
        }
    }

    void printResult() { errs() << nConditionalJMP << ","; }
};

/*Gregs voice is ghosting through my head :'(
    , AND IT IS NOT EVEN A REAL FACTORY! >:'(
*/
class FeatureFactory {
  public:
    SmallVector<FunctionFeature *> functionFeatures;

    FeatureFactory() {
        functionFeatures.push_back(new BasicBlockCounter());
        functionFeatures.push_back(new ConditionalJMPCounter());
        functionFeatures.push_back(new InstructionCounter());
    }

    ~FeatureFactory() {
        for (size_t i = 0; i < functionFeatures.size(); i++)
            delete functionFeatures[i];
    }
};

FeatureFactory features = FeatureFactory();

// New PM implementation
struct HelloWorld : PassInfoMixin<HelloWorld> {
    // Main entry point, takes IR unit to run the pass on (&F) and the
    // corresponding pass manager (to be queried if need be)

    void runOnFunction(Function &function) {
        for (size_t i = 0; i < features.functionFeatures.size(); i++)
            features.functionFeatures[i]->runOnFunction(function);
    }

    void exportResults() {
        for (size_t i = 0; i < features.functionFeatures.size(); i++)
            features.functionFeatures[i]->printResult();
        errs() << "\n";
    }

    // void getAnalysisUsage(AnalysisUsage &analysisUsage){
    //     analysisUsage.addPreserved<LoopVec>();
    //     getLoopAnalysisUsage(analysisUsage);
    // }

    PreservedAnalyses run(Module &module, ModuleAnalysisManager &AM) {
        // LoopAnalysis::Result analysis = AM.getResult<LoopAnalysis>(module);
        for (Function &function : module) {
            runOnFunction(function);
        }
        exportResults();
        return PreservedAnalyses::all();
    }

    // Without isRequired returning true, this pass will be skipped for functions
    // decorated with the optnone LLVM attribute. Note that clang -O0 decorates
    // all functions with optnone.
    static bool isRequired() { return true; }
};
} // namespace

//-----------------------------------------------------------------------------
// New PM Registration
//-----------------------------------------------------------------------------
llvm::PassPluginLibraryInfo getHelloWorldPluginInfo() {
    return {LLVM_PLUGIN_API_VERSION, "feat-extr", LLVM_VERSION_STRING, [](PassBuilder &PB) {
                PB.registerPipelineParsingCallback([](StringRef Name, ModulePassManager &FPM,
                                                      ArrayRef<PassBuilder::PipelineElement>) {
                    if (Name == "feat-extr") {
                        FPM.addPass(HelloWorld());
                        return true;
                    }
                    return false;
                });
            }};
}

// This is the core interface for pass plugins. It guarantees that 'opt' will
// be able to recognize HelloWorld when added to the pass pipeline on the
// command line, i.e. via '-passes=hello-world'
extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo llvmGetPassPluginInfo() {
    return getHelloWorldPluginInfo();
}