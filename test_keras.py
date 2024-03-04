import os
os.environ["KERAS_BACKEND"] = "torch"
from keras import Input, layers
from custom_model import CustomModel
import numpy as np

# https://keras.io/api/layers/
# https://keras.io/api/layers/core_layers/
inputs = Input(shape=(32,))
x = layers.Dense(64, activation="relu")(inputs)
x = layers.Dense(64, activation="relu")(x)
outputs = layers.Dense(10)(x)

model = CustomModel(inputs=inputs, outputs=outputs, name="dummy")
#https://keras.io/api/optimizers/
#https://keras.io/api/losses/
model.compile(optimizer="adam", loss="mse")

x = np.random.random((10, 32))
y = np.random.random((10, 10))
model.fit(x, y, epochs=3)