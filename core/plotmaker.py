import evolutionShapes as es
import matplotlib as mpl
import numpy as np
import pygad as pg
import pygad.kerasga as pgkGA
import pandas as pd
import compile as comp

def main():
    best_model_weights = np.loadtxt("best_solution_model_weights.csv", delimiter=",")
    ga_instance = pg.load("ga_instance.evol")
    predictions = pgkGA.predict(model=es.model, solution=best_model_weights, data=es.features_frame)
    choices = map(es.getPasses, predictions) 
    passes =  map(comp.get_args, predictions)

    labeled_predictions = {'test' : es.input_dataset['test'],
                           'choices' : choices,
                           'args' : passes}

    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print(pd.DataFrame(labeled_predictions))
if(__name__ == "__main__"):
    main()
