#include <llvm/IR/LegacyPassManager.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>
#include <llvm/Support/raw_ostream.h>
#include <iostream>

using namespace llvm;

/**
Features (Printed in order):
  - N-Basic blocks
  - N-Branches
  - N-Total Insts
  - N-FP Insts
  - N-Int Insts
  - N-Loads
  - N-Stores
  - Ratio of FP Insts to Int Insts
  - N-Builtin math functions
  - N-functions

TODO:


Look-into:
  - Average MLP per basic block
  - Average ILP per basic block


Skipped (Too Multithreading related):
  - N-Barriers
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
    virtual ~FunctionFeature() {}
};

class ModuleFeature {
  public:
    virtual void runOnModule(Module &module) {}
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

    void printResult() { std::cerr << nBasicBlocks << ","; }
};

class FunctionCounter : public ModuleFeature {
  private:
    int nIntrinsicFunctions = 0;
    int nFunction = 0;

  public:
    void runOnModule(Module &module) {
        for (Function &function : module) {
            nIntrinsicFunctions += (int)function.isIntrinsic();
            nFunction++;
        }
    }
    void printResult() { std::cerr << nIntrinsicFunctions << "," << nFunction; }
};

class InstructionCounter : public FunctionFeature {
    int nInsts = 0;
    int nFPInsts = 0;
    int nIntInsts = 0;
    int nLoads = 0;
    int nStores = 0;
    double ratioFloatIntInsts = 0.0;

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
        ratioFloatIntInsts = ((double)nFPInsts) / nIntInsts;
    }

    void printResult() {
        std::cerr << std::fixed;
        std::cerr.precision(3);
        std::cerr << nInsts << "," << nFPInsts << "," << nIntInsts << ",";
        std::cerr << nLoads << "," << nStores << "," << ratioFloatIntInsts << ",";
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

    void printResult() { std::cerr << nConditionalJMP << ","; }
};

/*Gregs voice is ghosting through my head :'(
    , AND IT IS NOT EVEN A REAL FACTORY! >:'(
*/
class FeatureFactory {
  public:
    SmallVector<FunctionFeature *> functionFeatures;
    SmallVector<ModuleFeature *> moduleFeatures;

    FeatureFactory() {
        functionFeatures.push_back(new BasicBlockCounter());
        functionFeatures.push_back(new ConditionalJMPCounter());
        functionFeatures.push_back(new InstructionCounter());

        moduleFeatures.push_back(new FunctionCounter());
    }

    ~FeatureFactory() {
        for (size_t i = 0; i < functionFeatures.size(); i++)
            delete functionFeatures[i];

        for (size_t i = 0; i < moduleFeatures.size(); i++)
            delete moduleFeatures[i];
    }
};

FeatureFactory features = FeatureFactory();

// New PM implementation
struct HelloWorld : PassInfoMixin<HelloWorld> {
    // Main entry point, takes IR unit to run the pass on (&F) and the
    // corresponding pass manager (to be queried if need be)

    void runOnModule(Module &module) {
        for (size_t i = 0; i < features.moduleFeatures.size(); i++) {
            features.moduleFeatures[i]->runOnModule(module);
        }
    }

    void runOnFunction(Function &function) {
        for (size_t i = 0; i < features.functionFeatures.size(); i++)
            features.functionFeatures[i]->runOnFunction(function);
    }

    void exportResults() {
        for (size_t i = 0; i < features.functionFeatures.size(); i++)
            features.functionFeatures[i]->printResult();
        for (size_t i = 0; i < features.moduleFeatures.size(); i++) {
            features.moduleFeatures[i]->printResult();
        }
    }

    // void getAnalysisUsage(AnalysisUsage &analysisUsage){
    //     analysisUsage.addPreserved<LoopVec>();
    //     getLoopAnalysisUsage(analysisUsage);
    // }

    PreservedAnalyses run(Module &module, ModuleAnalysisManager &AM) {
        // LoopAnalysis::Result analysis = AM.getResult<LoopAnalysis>(module);
        runOnModule(module);
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