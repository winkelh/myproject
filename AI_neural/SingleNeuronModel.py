# the SingleNeuronModel class   
import numpy as np

class SingleNeuronModel:
    def __init__(self, weight_1: float, weight_2: float, bias: float):
        self.weight_1 = weight_1
        self.weight_2 = weight_2
        self.bias     = bias
        
    def forward(self, train_data: np.ndarray) -> np.ndarray:
        self.predictions = (train_data[:, 0] * self.weight_1) + (train_data[:, 1] * self.weight_2) + self.bias
        return self.predictions
        
    def get_predictions(self) -> np.ndarray:
        return self.predictions
        
    def calculate_loss(self, predictions: np.ndarray, answers: np.ndarray) -> float:
        mean_sq_loss = np.mean(np.square(predictions - answers))
        return mean_sq_loss