# AdditionDataGenerator class
import numpy as np
import random

class AdditionDataGenerator:
    def __init__(self) -> None:
        pass
        
    def generate_traindata(self, sample_size: int, max_number: float = 100) -> tuple[np.ndarray, np.ndarray]:        
        self.sample_size = sample_size
        self.max_number  = max_number
        self.train_data = np.random.uniform(0, self.max_number, size=(self.sample_size, 2))
        self.answers = np.sum(self.train_data, axis=1)
        return self.train_data, self.answers      
            
    def get_traindata(self) -> np.ndarray:
        return self.train_data
        
    def get_answers(self) -> np.ndarray:
        return self.answers
        
        