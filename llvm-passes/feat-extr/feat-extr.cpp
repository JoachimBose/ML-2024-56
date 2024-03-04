#include <llvm/IR/LegacyPassManager.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>
#include <llvm/Support/raw_ostream.h>

using namespace llvm;


/**
Features:
 - N-basic blocks
 - Average instructions per basic block
 - N-Conditional jumps
 - N-loops
 -
*/
namespace
{
    class FunctionFeature
    {
        public:
        virtual void runOnFunction(Function &function){}
        virtual int getResult() { errs() << " baseclass "; return -1; }
    };

    // class LoopFeature{
    //     private:
    //     public:
    //     virtual void runOnLoop(Loop& loop){}
    //     virtual int getResult() { errs() << " baseloop "; return -1; }
    // };

    // class LoopCounter : public LoopFeature
    // {
    // private:
    //     int nLoops;
    // public:
    //     LoopCounter()
    //     {
    //         nLoops = 0;
    //     }
    //     void runOnLoop(Loop& loop){
    //         nLoops ++;
    //     }
    //     int getResult(){
    //         return nLoops;
    //     }
    // };

    class BasicBlockCounter : public FunctionFeature
    {
    private:
        int nBasicBlocks;

    public:
        void runOnFunction(Function &function)
        {
            for (BasicBlock &basicBlock : function)
            {
                nBasicBlocks++;
            }
        }
        BasicBlockCounter()
        {
            nBasicBlocks = 0;
        }
        int getResult() { errs() << " bbcount "; return nBasicBlocks; }
    };

    class InstructionCounter : public FunctionFeature
    {
    private:
        int nInstructions = 0;

    public:
        void runOnFunction(Function &function)
        {
            for (BasicBlock &basicBlock : function)
            {
                for (Instruction &instruction : basicBlock)
                {
                    nInstructions ++;
                }
            }
        }
        InstructionCounter()
        {
            nInstructions = 0;
        }
        int getResult() { return nInstructions; }
    };

    class ConditionalJMPCounter : public FunctionFeature
    {
    private:
        int nConditionalJMP;
    public:
        ConditionalJMPCounter(){
            nConditionalJMP = 0;
        }
        void runOnFunction(Function &function){
            for (BasicBlock& basicBlock : function)
            {
                for (Instruction& instruction : basicBlock)
                {
                    if (auto branchInst = dyn_cast<BranchInst>(&instruction))
                    {
                        nConditionalJMP += branchInst->isConditional()? 1 : 0;
                    }
                }
            }
        }
        int getResult() { return nConditionalJMP; }
    };

    /*Gregs voice is ghosting through my head :'(
        , AND IT IS NOT EVEN A REAL FACTORY! >:'(
    */
    class FeatureFactory
    {
    public:
        SmallVector<FunctionFeature*> functionFeatures;
        // SmallVector<LoopFeature*> loopFeatures;

        FeatureFactory()
        {
            functionFeatures.push_back(new ConditionalJMPCounter());
            functionFeatures.push_back(new InstructionCounter());
            functionFeatures.push_back(new BasicBlockCounter());

            // loopFeatures.push_back(new LoopCounter());
        }
        ~FeatureFactory(){
            
            for (size_t i = 0; i < functionFeatures.size(); i++)
            {
                delete functionFeatures[i];
            }
            // for (size_t i = 0; i < loopFeatures.size(); i++)
            // {
            //     delete loopFeatures[i];
            // }
        }
    };
    
    
    FeatureFactory features = FeatureFactory();

    // New PM implementation
    struct HelloWorld : PassInfoMixin<HelloWorld>
    {
        // Main entry point, takes IR unit to run the pass on (&F) and the
        // corresponding pass manager (to be queried if need be)

        void runOnFunction(Function& function)
        {
            for (size_t i = 0; i < features.functionFeatures.size(); i++)
            {
                features.functionFeatures[i]->runOnFunction(function);
            }
        }
        void exportResults(){
            for (size_t i = 0; i < features.functionFeatures.size(); i++)
            {
                errs() << "funcFeat " << i << " " << features.functionFeatures[i]->getResult() << "\n";
            }
            // for (size_t i = 0; i < features.loopFeatures.size(); i++)
            // {
            //     errs() << "loopFeat " << i << " " << features.functionFeatures[i]->getResult() << "\n";
            // }
        }

        // PreservedAnalyses run(Loop &L, LoopAnalysisManager &AM,
        //     LoopStandardAnalysisResults &AR,
        //     LPMUpdater &) {
        //     for (size_t i = 0; i < features.loopFeatures.size(); i++)
        //     {
        //         features.loopFeatures[i]->runOnLoop(L);
        //     }
        //     errs() << "loop pass finished\n";
        //     return PreservedAnalyses::all();
        // }

        // void getAnalysisUsage(AnalysisUsage &analysisUsage){
        //     analysisUsage.addPreserved<LoopAnalysis>();
        //     getLoopAnalysisUsage(analysisUsage);
        // }

        PreservedAnalyses run (Module &module, ModuleAnalysisManager &AM){
            // LoopAnalysis::Result analysis = AM.getResult<LoopAnalysis>(module);
            for (Function &function : module)
            {
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
llvm::PassPluginLibraryInfo getHelloWorldPluginInfo()
{
    return {LLVM_PLUGIN_API_VERSION, "feat-extr", LLVM_VERSION_STRING,
            [](PassBuilder &PB)
            {
                PB.registerPipelineParsingCallback(
                    [](StringRef Name, ModulePassManager &FPM,
                       ArrayRef<PassBuilder::PipelineElement>)
                    {
                        if (Name == "feat-extr")
                        {
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
extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo()
{
    return getHelloWorldPluginInfo();
}