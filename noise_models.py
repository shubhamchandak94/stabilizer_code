import numpy as np


def bit_flip_channel(prob: float):
    return [['I',1-prob],['X',prob],['Y',0],['Z',0]]

def phase_flip_channel(prob: float):
    return [['I',1-prob],['X',0],['Y',0],['Z',prob]]

def depolarizing_channel(prob: float):
    return [['I',1-prob],['X',prob/3.0],['Y',prob/3.0],['Z',prob/3.0]]
