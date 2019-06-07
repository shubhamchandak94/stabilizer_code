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

# The goal of this program is to create a function that takes as input 
# 1. A stabilizer code (described via its stabilizers)
# 2. A parametrized noise model (the parameter corresponds to the physical error rate)
# and output a plot of the logical vs physical error rates achieved



def GiveLogicalErrRate(code_name,noise_model_kraus,num_trials_tot,code):
	logical_err_rate = 0.0
	
	#print(code.encoding_program)		
	#print(code.decoding_program)		

	for trial_id in range(num_trials_tot):
		initial_state_prep = Program()
		inverse_initial_state_prep = Program()
		for qubit_id in range(code.k):
			z_angle = (2*np.pi*np.random.rand(1))
			y_angle = (1*np.pi*np.random.rand(1))
			initial_state_prep += RZ(z_angle[0],qubit_id)
			initial_state_prep += RY(y_angle[0],qubit_id)
			inverse_initial_state_prep += RY(-y_angle[0],qubit_id)
			inverse_initial_state_prep += RZ(-z_angle[0],qubit_id)
			#bit = np.random.randint(2)
			#if bit==1:
			#	initial_state_prep += X(qubit_id)
			#	inverse_initial_state_prep += X(qubit_id)

		# Don't use I gate anywher else in program
		error_prog = Program()
		for qubit_id in range(code.n):
			error_prog += Program(I(qubit_id))

		kraus_ops = noise_model_kraus
		error_defn = Program()
		for qubit_id in range(code.n):
			error_defn.define_noisy_gate('I', [qubit_id], kraus_ops)
		error_prog = error_defn + error_prog

		num_errors = basic_tests.test_general(code, initial_state_prep, error_prog, 1, inverse_initial_state_prep)		
		logical_err_rate += num_errors

	logical_err_rate = logical_err_rate/num_trials_tot
	print(code_name,logical_err_rate)
	return logical_err_rate

#code_name_list = ["bit_flip_code","phase_flip_code","steane_code","five_qubit_code", "shor_code"]
code_name_list = ["bit_flip_code","phase_flip_code","steane_code","five_qubit_code"]
#code_name_list = ["steane_code"]
noise_model_list = [["amplitude damping",noise_models_kraus.damping_kraus_map],
["dephasing",noise_models_kraus.dephasing_kraus_map],
["bit flip",noise_models_kraus.bit_flip_channel],
["phase flip",noise_models_kraus.phase_flip_channel],
["depolarizing",noise_models_kraus.depolarizing_channel]]

#noise_model_list = [["depolarizing",noise_models_kraus.depolarizing_channel]]

num_trials_tot = 500

for j in range(len(noise_model_list)):
	fig = plt.figure()

	for code_name in code_name_list:
		code = stabilizer_code.StabilizerCode(stabilizer_check_matrices.mat_dict[code_name])
		channel_param_vec = np.linspace(0,1,11)
		logical_err_rate_vec = np.zeros(len(channel_param_vec))
		for i in range(len(channel_param_vec)):
			noise_model_kraus = ((noise_model_list[j])[1])(channel_param_vec[i])
			logical_err_rate_vec[i] = GiveLogicalErrRate(code_name,noise_model_kraus,num_trials_tot,code)
		plt.plot(channel_param_vec,logical_err_rate_vec,label=code_name)
		

	plt.ylabel('Logical Error Rate')
	plt.xlabel((noise_model_list[j])[0]+' probability')
	plt.title('Logical Error Rates for various codes with '+(noise_model_list[j])[0]+' noise')
	plt.legend(loc='upper left')
	plt.savefig((noise_model_list[j])[0]+'.png',dpi=fig.dpi)
	#plt.show()


















