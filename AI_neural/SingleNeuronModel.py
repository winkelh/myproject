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
        
    def backward(self, train_data: np.ndarray, predictions: np.ndarray, answers: np.ndarray, learning_rate: float = 0.0001) -> None:
        error_array = predictions - answers

        # Calculate gradients
        weight_1_gradient = np.mean(error_array * train_data[:, 0]) * 2
        weight_2_gradient = np.mean(error_array * train_data[:, 1]) * 2
        bias_gradient = np.mean(error_array) * 2

        # Update internal states
        self.weight_1 -= learning_rate * weight_1_gradient
        self.weight_2 -= learning_rate * weight_2_gradient
        self.bias -= learning_rate * bias_gradient

    def get_weight_1(self) -> float:
        return self.weight_1

    def get_weight_2(self) -> float:
        return self.weight_2

    def get_bias(self) -> float:
        return self.bias
                        