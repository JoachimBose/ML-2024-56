import numpy as np
import pandas as pd
import pygad as pg
import pygad.kerasga as pgkGA
import keras as keras
import subprocess

potential_passes = [
    "loop-unroll",
    "sroa,mem2reg",
    "loop-simplify,loop-rotate",
    "instcombine",
    "instsimplify",
    "loop-vectorize",
    "adce",
    "reassociate",
    "licm",
]

feature_cols = ["nBasicBlocks","nConditionalJMPs","nInsts"
                                ,"nFPInsts","nIntInsts","nLoads","nStores",
                                "ratioFloatIntInsts","intrinsicFunctions",
                                "functions"]

input_dataset = pd.read_csv("/usr/src/app/dataset.csv")

# Help me datascientists
features_frame = input_dataset[feature_cols]
test_col = input_dataset["test"].to_numpy()

def getPasses(t):
    output_layer_rnd = list(map(lambda x : "1" if x > 0.5 else "0", t))
    # print(output_layer_rnd)
    return "".join(output_layer_rnd)

def find_codesize_for_sol(output_layers):
    true_y_pred = []
    for index, output_layer in enumerate(output_layers):
        test_name = test_col[index]

        # print(f"    outp{output_layer}")
        cmd =  ["python3", "./compile.py", test_name, getPasses(output_layer)]
        # print(cmd)
        opt_process = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        text = opt_process.stderr
        size = int(text.split(": ")[1])
        true_y_pred.append(size)
    return true_y_pred

def fitness_function(ga_instance, solution, solution_idx):
    predictions = pgkGA.predict(model=model,
                                        solution=solution,
                                        data=features_frame.to_numpy())
    # print("predictions:")
    # print(predictions)
    size = find_codesize_for_sol(predictions)
    # input() 

    for i in range(0,len(size)):
        size[i] = 1 / (size[i] + 0.0001)
    return size # avoid sticky situations

def constructNN():
    input_layer = keras.Input(shape=(len(feature_cols),))
    dense_layer1 = keras.layers.Dense(16, activation="relu")
    output_layer = keras.layers.Dense(len(potential_passes), activation="sigmoid")

    constructedModel = keras.Sequential()
    constructedModel.add(input_layer)
    constructedModel.add(dense_layer1)
    constructedModel.add(output_layer)
    return constructedModel


model = constructNN()

def on_generation(ga_instance):
    print(f"Generation = {ga_instance.generations_completed}")
    print(f"Fitness    = {ga_instance.best_solution()[1]}")
    ga_instance.plot_fitness(title="PyGAD & Keras - Iteration vs. Fitness", linewidth=4)
    return


def main():
    #hyperparameters have been assigned defaulty
    num_parents_mating = 4

    sol_per_pop = 8

    keras_ga = pgkGA.KerasGA(model, sol_per_pop)

    # Prepare the PyGAD parameters. Check the documentation for more information: https://pygad.readthedocs.io/en/latest/pygad.html#pygad-ga-class
    num_generations = 16 # Number of generations.
    num_parents_mating = 5 # Number of solutions to be selected as parents in the mating pool.
    initial_population = keras_ga.population_weights # Initial population of network weights

    ga_instance = pg.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        initial_population=initial_population,
                        fitness_func=fitness_function,
                        on_generation=on_generation)

    ga_instance.run()

    # After the generations complete, some plots are showed that summarize how the outputs/fitness values evolve over generations.
    ga_instance.plot_fitness(title="PyGAD & Keras - Iteration vs. Fitness", linewidth=4)

if(__name__ == "__main__"):
    main()