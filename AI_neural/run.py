# the caller script

import AdditionDataGenerator
import SingleNeuronModel
import numpy as np
train_data: np.ndarray
answers: np.ndarray

adg = AdditionDataGenerator.AdditionDataGenerator()
train_data, answers = adg.generate_traindata(sample_size = 2000, max_number = 100.00)
snm = SingleNeuronModel.SingleNeuronModel(weight_1 = 0.7, weight_2 = 1.2, bias = 1)
predictions = snm.forward(train_data = train_data)
total_loss = snm.calculate_loss(predictions = predictions, answers = answers)
print(f"Predictions: {predictions}")
print(f"Answers: {answers}")
print(f"Mean squared loss: {total_loss}")

