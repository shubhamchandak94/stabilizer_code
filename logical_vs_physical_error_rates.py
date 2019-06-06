import numpy as np
from pyquil import Program
from pyquil.gates import MEASURE, I, CNOT, X, H, Z, RZ, RY

import sys
from pyquil.api import QVMConnection
from pyquil.quil import DefGate

import basic_tests
import stabilizer_code
import stabilizer_check_matrices
import noise_models

# The goal of this program is to create a function that takes as input 
# 1. A stabilizer code (described via its stabilizers)
# 2. A parametrized noise model (the parameter corresponds to the physical error rate)
# and output a plot of the logical vs physical error rates achieved



code_name = "bit_flip_code"
noise_model = noise_models.bit_flip_channel(0.4)
num_trials_tot = 200

def GiveLogicalErrRate(code_name,noise_model,num_trials_tot):
	logical_err_rate = 0.0
	code = stabilizer_code.StabilizerCode(stabilizer_check_matrices.mat_dict[code_name])
	#print(code.encoding_program)		
	#print(code.decoding_program)		

	for trial_id in range(num_trials_tot):
		initial_state_prep = Program()
		for qubit_id in range(code.k):
			#z_angle = (2*np.pi*np.random.rand(1))
			#y_angle = (1*np.pi*np.random.rand(1))
			#initial_state_prep += RZ(z_angle[0],qubit_id)
			#initial_state_prep += RY(y_angle[0],qubit_id)
			bit = np.random.randint(2)
			if bit==1:
				initial_state_prep += X(qubit_id)

		
		error_prog = Program()
		for qubit_id in range(code.n):
			#error_prog.define_noisy_gate("I", [qubit_id], noise_model)
			#error_prog += I(qubit_id)
			num_kraus_ops = len(noise_model)				
					
			prob_vec = np.zeros(num_kraus_ops)
			for i in range(num_kraus_ops):
				prob_vec[i] = (noise_model[i])[1]

			kraus_op_to_apply = (np.random.choice(num_kraus_ops, 1, p=prob_vec))[0]
			
			MY_NOISE = (noise_model[kraus_op_to_apply])[0]
			error_prog += Program(MY_NOISE+' '+str(qubit_id))
		
		
		
		num_errors = basic_tests.test_general(code, initial_state_prep, error_prog, 1)		
		logical_err_rate += num_errors

	logical_err_rate = logical_err_rate/num_trials_tot
	print(code_name,logical_err_rate)
	return logical_err_rate



GiveLogicalErrRate(code_name,noise_model,num_trials_tot)



















