import AdditionDataGenerator
import numpy as np
train_data: np.ndarray
answers: np.ndarray

adg = AdditionDataGenerator.AdditionDataGenerator(2000, 100.00)

train_data, answers = adg.generate_traindata()

print(f"train_data: {train_data}, answers: {answers}")