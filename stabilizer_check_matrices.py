import numpy as np

mat_dict = {}

# dtype = np.uint instead of bool so that addition works correctly
# the second element of list stores a dict showing the types of errors the
# code can correct and number of those errors: 'X', 'Y', 'Z' are the standard
# stuff. The min of these three is the number of arbitrary qubit errors the
# code can handle. Other than that we also mention 'XZ' which means one X and
# one Z occuring on different qubits (Shor and Steane codes can correct this).

mat_dict['bit_flip_code'] = [np.array([
    [0, 0, 0,   1, 1, 0],
    [0, 0, 0,   1, 0, 1],
], dtype = np.uint), {
    'X': 1,
    'Z': 0,
    'Y': 0,
    'XZ': 0,
}]



mat_dict['phase_flip_code'] = [np.array([
    [1, 1, 0,   0, 0, 0],
    [1, 0, 1,   0, 0, 0],
], dtype = np.uint), {
    'X': 0,
    'Z': 1,
    'Y': 0,
    'XZ': 0,
}]

mat_dict['shor_code'] = [np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 1,  0, 0, 0, 0, 0, 0, 0, 0, 0],
], dtype = np.uint), {
    'X': 1,
    'Z': 1,
    'Y': 1,
    'XZ': 1,
}]

mat_dict['steane_code'] = [np.array([
    [1, 1, 1, 1, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0,   0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1,   0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0,   1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0,   1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0,   1, 0, 1, 0, 1, 0, 1],
], dtype = np.uint), {
    'X': 1,
    'Z': 1,
    'Y': 1,
    'XZ': 1,
}]

mat_dict['five_qubit_code'] = [np.array([
    [1, 0, 0, 1, 0,     0, 1, 1, 0, 0],
    [0, 1, 0, 0, 1,     0, 0, 1, 1, 0],
    [1, 0, 1, 0, 0,     0, 0, 0, 1, 1],
    [0, 1, 0, 1, 0,     1, 0, 0, 0, 1],
], dtype = np.uint), {
    'X': 1,
    'Z': 1,
    'Y': 1,
    'XZ': 0,
}]
