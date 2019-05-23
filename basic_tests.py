import numpy as np
from pyquil import Program
from pyquil.gates import MEASURE, I, CNOT, X, H, Z
import stabilizer_code
import stabilizer_check_matrices

from pyquil.api import QVMConnection

def test_general(code: stabilizer_code.StabilizerCode, initial_state_prep: Program, error_prog: Program, num_trials = 100):
    qvm = QVMConnection()
    # find inverse of initial state prep to be applied at end before measurement
    inverse_initial_state_prep = Program()
    for instruction in reversed(initial_state_prep):
        # inverse gate
        new_instruction_name = 'DAGGER ' + instruction.name
        # apply to shifted qubits since decoder writes output to n...n+k-1
        new_instruction_qubits = [str(code.n + q) for q in instruction.qubits]
        inverse_initial_state_prep += Program(' '.join([new_instruction_name]+new_instruction_qubits))
    prog = initial_state_prep + code.encoding_program + error_prog + code.decoding_program + invert_initial_state_prep
    prog.measure_all()
    measured_bits = qvm.run(prog, trials=num_trials)
    decoded_msg_bits = measured_bits[:,code.n:code.n+code.k]
    # part which contains decoded qubits
    num_errors = np.count_nonzero(np.sum(decoded_msg_bits,axis=0))
    print('num_trials', num_trials)
    print('num_errors', num_errors)

def generate_initial_state_prep_for_testing(k):
    # returns list of programs generating initial states for testing the
    # encoding decoding.
    if k == 1:
        # for k = 1, we return |0>, |1>, |+> and |->
        return [
            Program(),
            Program('X 0'),
            Program('H 0'),
            Program('X 0') + Program('H 0'),
        ]
    elif k == 2:
        # for k = 2, return |00>, |01>, |10>, |11>, 1/sqrt(2)(|00>+|11>)
        return [
            Program(),
            Program('X 0'),
            Program('X 1'),
            Program('X 0') + Program('X 1'),
            Program('H 0') + Program('CNOT 0 1'),
        ]
    else:
        raise NotImplementedError

def test_no_error(code: stabilizer_code.StabilizerCode):
    print('No error case')
    initial_state_list = generate_initial_state_prep_for_testing(code.k)
    for init_program in initial_state_list:
        print('Initial state')
        print(program)
        test_general(code, init_program, Program())

def test_single_bit_flip(code: stabilizer_code.StabilizerCode):
    print('Single bit flip case')
    initial_state_list = generate_initial_state_prep_for_testing(code.k)
    for init_program in initial_state_list:
        print('Initial state')
        print(init_program)
        for i in range(code.n):
            print('Error in qubit',i)
            test_general(code, init_program, Program('X '+str(i)))


def test_single_phase_flip(code: stabilizer_code.StabilizerCode):
    print('Single phase flip case')
    initial_state_list = generate_initial_state_prep_for_testing(code.k)
    for init_program in initial_state_list:
        print('Initial state')
        print(init_program)
        for i in range(code.n):
            print('Error in qubit',i)
            test_general(code, init_program, Program('Z '+str(i)))


def test_single_Y_noise(code: stabilizer_code.StabilizerCode):
    print('Single Y error case')
    initial_state_list = generate_initial_state_prep_for_testing(code.k)
    for init_program in initial_state_list:
        print('Initial state')
        print(init_program)
        for i in range(code.n):
            print('Error in qubit',i)
            test_general(code, init_program, Program('Y '+str(i)))


def test_oneX_oneZ(code: stabilizer_code.StabilizerCode):
    print('One X and one Z error on different qubits case')
    initial_state_list = generate_initial_state_prep_for_testing(code.k)
    for init_program in initial_state_list:
        print('Initial state')
        print(init_program)
        for i in range(code.n):
            for j in range(code.n):
                if i == j:
                    continue
                print('X error in qubit',i)
                print('Z error in qubit',j)
                test_general(code, init_program, Program('X '+str(i))+Program('Z '+str(j)))

code_name_list = ['bit_flip_code', 'phase_flip_code', 'shor_code', 'steane_code', 'five_qubit_code','table_3_5_code_4_2_2']
for code_name in code_name_list:
    print('Code:',code_name)
    code = stabilizer_code.StabilizerCode(stabilizer_check_matrices.mat_dict[code_name])
    test_no_error(code)
    test_single_bit_flip(code)
    test_single_phase_flip(code)
    test_single_Y_noise(code)
    test_oneX_oneZ(code)
