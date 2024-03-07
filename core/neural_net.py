import os
os.environ["KERAS_BACKEND"] = "torch"
from keras import Input, layers
from custom_model import CustomModel
from pandas import read_csv

source_location = "../source.csv"
input_count = 10
output_count = 9
target = "target-size"
test = "test"

data = read_csv(source_location)
y_data = data[target].values.astype("int32")
test_names = data[test].values
x_data = data.drop([target, "test"], axis=1).values

# https://keras.io/api/layers/
# https://keras.io/api/layers/core_layers/
inputs = Input(shape=(input_count,))
x = layers.Dense(64, activation="relu")(inputs)
x = layers.Dense(64, activation="relu")(x)
outputs = layers.Dense(output_count, activation="sigmoid")(x)

model = CustomModel(test_names, inputs=inputs, outputs=outputs, name="dummy")
#https://keras.io/api/optimizers/
#https://keras.io/api/losses/
model.compile(optimizer="adam", loss="mse")

model.fit(x_data, y_data, epochs=3)