import numpy as np
import pandas as pd
import pygad as pg
import pygad.kerasga as pgkGA
import keras as keras
import subprocess
import matplotlib as mpl
import evolutionShapes as es


def main():
    
    #hyperparameters have been assigned defaulty
    sol_per_pop = 4

    keras_ga = pgkGA.KerasGA(es.model, sol_per_pop)

    # Prepare the PyGAD parameters. Check the documentation for more information: https://pygad.readthedocs.io/en/latest/pygad.html#pygad-ga-class
    num_generations = 2 # Number of generations.
    num_parents_mating = 2 # Number of solutions to be selected as parents in the mating pool.
    initial_population = keras_ga.population_weights # Initial population of network weights

    ga_instance = pg.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        initial_population=initial_population,
                        fitness_func=es.fitness_function,
                        on_generation=es.on_generation)

    ga_instance.run()

    # After the generations complete, some plots are showed that summarize how the outputs/fitness values evolve over generations.
    ga_instance.plot_fitness(title="PyGAD & Keras - Iteration vs. Fitness", linewidth=4)
    ga_instance.save("ga_instance.evol")

    mpl.pyplot.plot(ga_instance.best_solutions_fitness)
    mpl.pyplot.savefig("PyGAD_figure.jpg")

    """
    breakdown of bestsolution() because python documentation is bad:
    best_solution() returns a tuple:
     - numpy tensor of the model weights for best solution
     - numpy tensor of the fitness of the best solution
     - index of best solution from population
    """
    np.savetxt('best_solution_model_weights.csv', ga_instance.best_solution()[0],delimiter=",")

if(__name__ == "__main__"):
    main()