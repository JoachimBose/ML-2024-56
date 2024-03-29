import numpy as np
import pygad.kerasga as pgkGA
import pandas as pd
import os
import core.evolution.evolution_shapes as es
from core.main.config import MODEL_DIR, OUTPUT_DIR, PERF_DIR
import sys
import subprocess
import matplotlib.pyplot as plt


# Make sure we're running in the file dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main() -> None:
    validation_data = pd.read_csv(f"../{OUTPUT_DIR}validation_pca.csv") 
    validation_frame = validation_data.iloc[:, :4]     
    
    for file in os.listdir("../" + MODEL_DIR):
        if not file.endswith(".csv"):
            continue
        model_file = file
        
        output_file = f"../{PERF_DIR}{model_file}"
        if os.path.exists(output_file):
            print(f"ERROR: Performance already evaluated {model_file[:-4]}")
            continue
                
        best_model_weights = np.loadtxt("../" + MODEL_DIR + model_file, delimiter=",")
        predictions = pgkGA.predict(model=es.model, solution=best_model_weights, data=validation_frame)
        choices = list(map(es.getPasses, predictions)) 
        
        sizes = []
        for index, test in enumerate(validation_data['test']):
            cmd = ["python3", "../compile.py", test, choices[index]]

            
            process = subprocess.Popen(
                " ".join(cmd), stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True
            )
            process.wait()
            text = process.stderr.readline().decode(encoding="utf-8")
            try:
                size = int(text.split(": ")[1])
            except:
                print(text)
            sizes.append(size)

        
        labeled_predictions = {'test' : validation_data['test'],
                            'choices' : choices,
                            'target-size' : validation_data['target-size'],
                            'actual-size' : sizes}
        data = pd.DataFrame(labeled_predictions)
        data.to_csv(output_file)    

    # plt.scatter(sizes, validation_data['target-size'])
    # plt.axline((0, 0), slope=1, color='red')
    # plt.xlabel('Actual Size')
    # plt.ylabel('Target Size')
    # plt.title('Validation Data: Target Size vs Actual Size')
    # plt.savefig("../../temp.png")


if __name__ == "__main__":
    
    main()
