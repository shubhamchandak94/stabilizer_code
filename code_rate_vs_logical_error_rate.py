import numpy as np
from pyquil import Program
from pyquil.gates import MEASURE, I, CNOT, X, H, Z, RZ, RY

import sys
from pyquil.api import QVMConnection
from pyquil.quil import DefGate

import basic_tests
import stabilizer_code
import stabilizer_check_matrices
import noise_models_kraus

import matplotlib.pyplot as plt

import logical_vs_physical_error_rates


def PlotCodeRateVsErrRate(init_state_mode,num_trials_tot,code_name_list,noise_model_kraus):
	code_rate_vec = []
	logical_err_rate_vec = []


	for code_name in code_name_list:
		code = stabilizer_code.StabilizerCode(stabilizer_check_matrices.mat_dict[code_name])
		code_rate_vec.append(code.k/code.n)
		logical_err_rate_vec.append(logical_vs_physical_error_rates.GiveLogicalErrRate(code_name,noise_model_kraus,num_trials_tot,code,init_state_mode))


	fig = plt.figure()
	plt.scatter(code_rate_vec,logical_err_rate_vec)

	for i, txt in enumerate(code_name_list):
		plt.annotate(txt, (code_rate_vec[i],logical_err_rate_vec[i]))
		
	plt.ylabel('Logical Error Rate')
	plt.xlabel('Code rate = num of logical qubits / num of physical qubits')
	plt.title('Logical Error Rates vs code rate various codes with depolarizing noise (0.4)')
	plt.savefig('code_rate.png',dpi=fig.dpi)


# An example code_name_list
# To see what codes are already implemented supported, check stabilizer_check_matrices.py
code_name_list = ["bit_flip_code","phase_flip_code","steane_code","five_qubit_code"]

num_trials_tot = 5

# If init_state_mode  = 0, initial state for the test is randomly |0> or |1> uniformly
# If init_state_mode  = 1, initial state for the test is uniformly random on Bloch sphere
init_state_mode = 1

# p is the noise parameter
p = 0.4

# To see what noise models are already implemented, check noise_models_kraus.py
noise_model_kraus = noise_models_kraus.depolarizing_channel(p)

# It is also possible to write your own code or noise model, by following the formats in the two files above.

PlotCodeRateVsErrRate(init_state_mode,num_trials_tot,code_name_list,noise_model_kraus)


