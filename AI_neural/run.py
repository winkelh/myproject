import AdditionDataGenerator
import numpy as np
import SingleNeuronModel
train_data: np.ndarray
answers: np.ndarray

adg = AdditionDataGenerator.AdditionDataGenerator(2000, 100.00)

train_data, answers = adg.generate_traindata()

print(f"train_data: {train_data}, answers: {answers}")

a = np.array([[3, 7], [8, 11], [24, 3]])
b1 = 0.7
b2 = 1.2
c = a[:, 0] * b1
d = a[:, 1] * b2
print(f"Result 1: {c}")
print(f"Result 2: {d}")

snm = SingleNeuronModel.SingleNeuronModel(2000, 100.00, 0.7, 1.2, 3)
e = snm.forward()
print(e)