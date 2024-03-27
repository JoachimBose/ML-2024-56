import numpy as np
import pygad as pg
import pygad.kerasga as pgkGA
import pandas as pd
import os
import core.evolution.evolution_shapes as es
import matplotlib as mpl
from core.main.config import OUTPUT_DIR, POTENTIAL_PASSES

# Make sure we're running in the file dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_args(test_type: str) -> str:
    options = []
    for i, c in enumerate(test_type):
        if int(c):
            options.append(POTENTIAL_PASSES[i])
    args = ",".join(options)
    return args

def main() -> None:
    best_model_weights = np.loadtxt("../" + OUTPUT_DIR + "best_solution_model_weights.csv", delimiter=",")
    ga_instance = pg.load("../" + OUTPUT_DIR + "ga_instance.evol")
    predictions = pgkGA.predict(model=es.model, solution=best_model_weights, data=es.features_frame)
    choices = map(es.getPasses, predictions) 
    passes =  map(get_args, predictions)
    one = '\e[34;47Y\e[0m'
    zero = '\e[0;30mN\e[0m'

    labeled_predictions = {'test' : es.input_dataset['test'],
                           'choices' : list(choices),
                           'args' : list(passes)}

    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print(pd.DataFrame(labeled_predictions))
    pd.DataFrame(labeled_predictions).to_csv(f"../{OUTPUT_DIR}/PyGAD_summed_figure.jpg")

    mpl.pyplot.plot(ga_instance.best_solutions_fitness)
    mpl.pyplot.savefig("../" + OUTPUT_DIR + "PyGAD_figure.jpg")

    best_sol_arr = np.array(ga_instance.best_solutions_fitness)
    print(best_sol_arr.shape)
    print("hi wut?")
    v = best_sol_arr.sum(axis=1)
    print(v)
    print(v.shape)

    mpl.pyplot.clf()
    mpl.pyplot.plot(v)
    mpl.pyplot.savefig(f"../{OUTPUT_DIR}/PyGAD_summed_figure.jpg")
    

if __name__ == "__main__":
    main()
