import numpy as np
import pygad as pg
import pygad.kerasga as pgkGA
import keras as keras
import matplotlib as mpl
import os
import core.evolution.evolution_shapes as es
from core.main.config import SOL_PER_POP, NUM_GENERATIONS, NUM_PARENTS_MATING, OUTPUT_DIR

# Make sure we're running in the file dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main() -> None:
    keras_ga = pgkGA.KerasGA(es.model, SOL_PER_POP)

    # Prepare the PyGAD parameters. Check the documentation for more information: 
    # https://pygad.readthedocs.io/en/latest/pygad.html#pygad-ga-class
    # Initial population of network weights
    initial_population = keras_ga.population_weights 

    ga_instance = pg.GA(num_generations=NUM_GENERATIONS,
                        num_parents_mating=NUM_PARENTS_MATING,
                        initial_population=initial_population,
                        fitness_func=es.fitness_function,
                        on_generation=es.on_generation)

    ga_instance.run()

    # After the generations complete, some plots are showed that summarize how the outputs/fitness values evolve over generations.
    ga_instance.plot_fitness(title="PyGAD & Keras - Iteration vs. Fitness", linewidth=4)
    ga_instance.save("../" + OUTPUT_DIR + "ga_instance.evol")

    mpl.pyplot.plot(ga_instance.best_solutions_fitness)
    mpl.pyplot.savefig("../" + OUTPUT_DIR + "PyGAD_figure.jpg")

    """
    breakdown of bestsolution() because python documentation is bad:
    best_solution() returns a tuple:
     - numpy tensor of the model weights for best solution
     - numpy tensor of the fitness of the best solution
     - index of best solution from population
    """
    np.savetxt("../" + OUTPUT_DIR + "best_solution_model_weights.csv", ga_instance.best_solution()[0],delimiter=",")

if(__name__ == "__main__"):
    main()