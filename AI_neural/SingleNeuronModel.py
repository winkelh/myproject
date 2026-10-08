import AdditionDataGenerator
import numpy as np

class SingleNeuronModel:
    def __init__(self, sample_size: int, max_number: float, weight_1: float, weight_2: float, bias: float):
        self.sample_size = sample_size
        self.max_number  = max_number
        self.weight_1    = weight_1
        self.weight_2    = weight_2
        self.bias        = bias
        
    def forward(self) -> []:
        adg = AdditionDataGenerator.AdditionDataGenerator(self.sample_size, self.max_number)
        self.train_data, self.answers = adg.generate_traindata()
        self.predictions = (self.train_data[:, 0] * self.weight_1) + (self.train_data[:, 1] * self.weight_2) + self.bias
        return self.predictions