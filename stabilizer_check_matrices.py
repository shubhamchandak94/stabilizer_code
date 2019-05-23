import numpy as np

mat_dict = {}

# dtype = np.uint8 instead of bool so that addition works correctly

mat_dict['bit_flip_code'] = np.array([
    [0, 0, 0,   1, 1, 0],
    [0, 0, 0,   1, 0, 1],
], dtype = np.uint8)

mat_dict['phase_flip_code'] = np.array([
    [1, 1, 0,   0, 0, 0],
    [1, 0, 1,   0, 0, 0],
], dtype = np.uint8)

mat_dict['shor_code'] = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 1,  0, 0, 0, 0, 0, 0, 0, 0, 0],
], dtype = np.uint8)

mat_dict['steane_code'] = np.array([
    [1, 1, 1, 1, 0, 0, 0,   0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0,   0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1,   0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0,   1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0,   1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0,   1, 0, 1, 0, 1, 0, 1],
], dtype = np.uint8)

mat_dict['five_qubit_code'] = np.array([
    [1, 0, 0, 1, 0,     0, 1, 1, 0, 0],
    [0, 1, 0, 0, 1,     0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0,     0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0,     1, 0, 1, 0, 0],
], dtype = np.uint8)

mat_dict['table_3_5_code_4_2_2'] = np.array([
    [1, 0, 0, 1,     0, 1, 1, 0],
    [1, 1, 1, 1,     1, 0, 0, 1],
], dtype = np.uint8)