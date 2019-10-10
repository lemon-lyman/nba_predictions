import numpy as np


class Model:
    def __init__(self, prediction_history, dates, label):
        self.prediction_history = prediction_history
        self.dates = dates
        self.label = label

    def ongoing_average(self):
        return [np.mean(self.prediction_history[:ii + 1]) for ii in range(len(self.prediction_history))]

    def moving_average(self, prediction_history, window=10):
        pass