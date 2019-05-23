import numpy as np

from pyquil import Program
from pyquil.gates import MEASURE, I, CNOT, X, H, Z

# all references are to chapter 4 of Gottesman's thesis, chapter 4
# https://arxiv.org/pdf/quant-ph/9705052.pdf

class StabilizerCode:
    def __init__(self, check_matrix):
        self.check_matrix = check_matrix
        assert np.shape(self.check_matrix)[1]%2 == 0
        self.n = np.shape(self.check_matrix)[1]//2
        self.k = self.n - np.shape(self.check_matrix)[0]
        print('Check matrix stabilizers:')
        print_check_matrix(self.check_matrix)
        (self.r, self.std_check_matrix, self.X_bar, self.Z_bar) = \
                    convert_to_std_form(check_matrix)
        print('Standard form check matrix stabilizers:')
        print_check_matrix(self.std_check_matrix)
        print('Standard form X_bar operators:')
        print_check_matrix(self.X_bar)
        print('Standard form Z_bar operators:')
        print_check_matrix(self.Z_bar)
        self.encoding_program = self.__encode()
        # message qubits 0 to k-1, ancilla 0 qubits k to n-1
        # encoded codeword qubits in 0 to n-1
        self.decoding_program = self.__decode()
        # noisy encoded codeword 0 to n-1, ancilla 0 qubits n to n+k-1
        # decoded message qubits in n to n+k-1

    def __encode(self) -> Program:
        # DO NOT CALL DIRECTLY, INSTEAD USE StabilizerCode.encoding_program
        # Returns program for encoding under the assumption that
        # qubits 0 through k-1 contain the state to be encoded
        # and rest of the n-k qubits start at 0. The encoded codeword
        # is put in qubits 0 through n-1
        pass

    def __decode(self) -> Program:
        # DO NOT CALL DIRECTLY, INSTEAD USE StabilizerCode.decoding_program
        # returns program for decoding under the assumption that
        # qubits 0 through n-1 contain the noisy codeword.
        # The decoded message qubits are finally put in qubits n through n+k-1.
        pass

def print_check_matrix(check_matrix):
    assert np.shape(check_matrix)[1]%2 == 0
    n = np.shape(check_matrix)[1]//2
    tuple2pauli = {(0,0):'I', (0,1): 'Z', (1,0): 'X', (1,1): 'Y'}
    for row in check_matrix:
        print(''.join([tuple2pauli[(row[i], row[n+i])] for i in range(n)]))
    return

def convert_to_std_form(check_matrix):
    assert np.shape(check_matrix)[1]%2 == 0
    n = np.shape(check_matrix)[1]//2
    k = n - np.shape(check_matrix)[0]
    # first we perform Gaussian elimination on the check matrix
    # as in equation 4.1 of thesis
    std_check_matrix = np.copy(check_matrix)
