import numpy as np


def bit_flip_channel(prob: float):
    noisy_I = np.sqrt(1-prob) * np.asarray([[1, 0], [0, 1]])
    noisy_X = np.sqrt(prob) * np.asarray([[0, 1], [1, 0]])
    return [noisy_I, noisy_X]


def phase_flip_channel(prob: float):
    noisy_I = np.sqrt(1-prob) * np.asarray([[1, 0], [0, 1]])
    noisy_Z = np.sqrt(prob) * np.asarray([[1, 0], [0, -1]])
    return [noisy_I, noisy_Z]


def depolarizing_channel(prob: float):
    noisy_I = np.sqrt(1-prob) * np.asarray([[1, 0], [0, 1]])
    noisy_X = np.sqrt(prob/3.0) * np.asarray([[0, 1], [1, 0]])    
    noisy_Y = 1j	* np.sqrt(prob/3.0) * np.asarray([[0, -1], [1, 0]])
    noisy_Z = np.sqrt(prob/3.0) * np.asarray([[1, 0], [0, -1]])
    return [noisy_I, noisy_X,noisy_Y, noisy_Z]
