import pandas as pd
import pygad.kerasga as pgkGA
import keras as keras
import subprocess
import os
import time as time
from core.main.config import POTENTIAL_PASSES, FEATURES, OUTPUT_DIR

# Make sure we're running in the file dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

input_dataset = pd.read_csv("../" + OUTPUT_DIR + "dataset.csv")
features_frame = input_dataset[FEATURES]
test_col = input_dataset["test"].to_numpy()
sizes_found = []


def getPasses(t):
    output_layer_rnd = list(map(lambda x: "1" if x > 0.5 else "0", t))
    return "".join(output_layer_rnd)


def find_codesize_for_sol(output_layers):
    sizes = []

    compiling_procs = []
    for index, output_layer in enumerate(output_layers):
        test_name = test_col[index]
        cmd = ["python3","../compile.py",test_name,getPasses(output_layer)]
        
        compiling_procs.append(subprocess.Popen(" ".join(cmd), 
            stderr = subprocess.PIPE,
            stdin = subprocess.PIPE,
            shell=True))
    for index, output_layer in enumerate(output_layers):
        compiling_procs[index].wait()
        # print("done waiting!")
        # print(dir(compiling_procs[index].stderr))
        text = compiling_procs[index].stderr.readline().decode(encoding='utf-8')
        # print(f"text is of type {type(text)} and is: {text}")
        try:
            size = int(text.split(": ")[1])
        except:
            print(text)
        sizes.append(size)

    # for index, output_layer in enumerate(output_layers):
    #     test_name = test_col[index]

    #     cmd = ["python3", "../compile.py", test_name, getPasses(output_layer)]
    #     opt_process = subprocess.run(cmd, check=True, capture_output=True, text=True)
    #     text = opt_process.stderr
    #     try:
    #         size = int(text.split(": ")[1])
    #         sizes.append(size)
    #     except:
    #         print(text)
    #         sizes.append(100000000000000)
    #         exit(0)
    return sizes


def fitness_function(ga_instance, solution, solution_idx):
    start = time.time()
    predictions = pgkGA.predict(
        model=model, solution=solution, data=features_frame.to_numpy()
    )
    size = find_codesize_for_sol(predictions)

    for i in range(0, len(size)):
        size[i] = -(size[i])
    end = time.time()
    print(f"size: {sum(size)} fitness took {end - start} ")
    return size  # avoid sticky situations


def constructNN() -> keras.Sequential:
    input_layer = keras.Input(shape=(len(FEATURES),))
    dense_layer1 = keras.layers.Dense(len(FEATURES), activation="relu")
    dense_layer2 = keras.layers.Dense(len(FEATURES), activation="relu")
    dense_layer3 = keras.layers.Dense(len(FEATURES), activation="relu")

    output_layer = keras.layers.Dense(len(POTENTIAL_PASSES), activation="sigmoid")

    constructedModel = keras.Sequential()
    constructedModel.add(input_layer)
    constructedModel.add(dense_layer1)
    constructedModel.add(dense_layer2)
    constructedModel.add(dense_layer3)
    constructedModel.add(output_layer)
    return constructedModel


def on_generation(ga_instance):
    print(f"Generation = {ga_instance.generations_completed}")
    print(f"Fitness    = {sum(ga_instance.best_solution()[1])}")
    ga_instance.save("../" + OUTPUT_DIR + "ga_instance.evol")
    return


model = constructNN()
