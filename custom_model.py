import os
os.environ["KERAS_BACKEND"] = "torch"
import torch
import numpy as np
from keras import Model

class CustomModel(Model):
    def train_step(self, data):
        # Unpack the data. Its structure depends on your model and
        # on what you pass to `fit()`.
        x, y = data

        # Call torch.nn.Module.zero_grad() to clear the leftover gradients
        # for the weights from the previous train step.
        self.zero_grad()

        # Compute loss
        y_pred = self(x, training=True)  # Forward pass
        print(x)
        print(y_pred)
        #TODO y_pred are the determined optimisations in our case, and we should call clang with them.
        #This is for all the x passed in, so if we use 10 application,
        #then x is an array with 10 elements each of which is an array containing all the features in the input layer,
        #y is an array with 10 elements each of which contains the output for each of the values in the nodes in the output layer.
        loss = self.compute_loss(y=y, y_pred=y_pred)
        

        # Call torch.Tensor.backward() on the loss to compute gradients
        # for the weights.
        loss.backward()

        trainable_weights = [v for v in self.trainable_weights]
        gradients = [v.value.grad for v in trainable_weights]

        # Update weights
        with torch.no_grad():
            self.optimizer.apply(gradients, trainable_weights)

        # Update metrics (includes the metric that tracks the loss)
        for metric in self.metrics:
            if metric.name == "loss":
                metric.update_state(loss)
            else:
                metric.update_state(y, y_pred)

        # Return a dict mapping metric names to current value
        # Note that it will include the loss (tracked in self.metrics).
        return {m.name: m.result() for m in self.metrics}