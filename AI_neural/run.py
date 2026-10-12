# the caller script

import AdditionDataGenerator
import SingleNeuronModel
import numpy as np
train_data: np.ndarray
answers: np.ndarray
NO_OF_EPOCHS: int = 1000
PRINT_INTERVAL: int = 10

adg = AdditionDataGenerator.AdditionDataGenerator()
train_data, answers = adg.generate_traindata(sample_size = 2000, max_number = 1.0)
snm = SingleNeuronModel.SingleNeuronModel(weight_1 = 0.5, weight_2 = 1.5, bias = 2.0)
for i in range(NO_OF_EPOCHS):
    predictions = snm.forward(train_data = train_data)
    mean_sq_loss = snm.calculate_loss(predictions = predictions, answers = answers)
    snm.backward(train_data = train_data, predictions = predictions, answers = answers, learning_rate = 0.1)
    if (i+1) % PRINT_INTERVAL == 0:
        print(f"Epoch #: {i+1}; Mean squared loss: {mean_sq_loss}")

print(f"\nResult after {NO_OF_EPOCHS} epochs:")
print(f"Weight 1: {snm.get_weight_1():.4f} (Expected: ~1.0)")
print(f"Weight 2: {snm.get_weight_2():.4f} (Expected: ~1.0)")
print(f"Bias:     {snm.get_bias():.4f} (Expected: ~0.0)")

test_data, answers = adg.generate_traindata(sample_size = 10, max_number = 1.0)
predictions = snm.forward(train_data = test_data)