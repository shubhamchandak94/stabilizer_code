import numpy as np
import itertools
from pyquil import Program
from pyquil.gates import MEASURE

# all references are to chapter 4 of Gottesman's thesis, chapter 4
# https://arxiv.org/pdf/quant-ph/9705052.pdf

tuple2pauli = {(0,0):'I', (0,1): 'Z', (1,0): 'X', (1,1): 'Y'}

class StabilizerCode:
    def __init__(self, check_matrix):
        self.check_matrix = check_matrix[0]
        assert np.shape(self.check_matrix)[1]%2 == 0
        self.n = np.shape(self.check_matrix)[1]//2
        self.k = self.n - np.shape(self.check_matrix)[0]
        print('n:',self.n)
        print('k:',self.k)
        print('Check matrix stabilizers:')
        print_check_matrix(self.check_matrix)
        (self.r, self.std_check_matrix, self.X_bar, self.Z_bar) = \
                    convert_to_std_form(self.check_matrix)
        print('Standard form check matrix stabilizers:')
        print_check_matrix(self.std_check_matrix)
        print('Standard form X_bar operators:')
        print_check_matrix(self.X_bar)
        print('Standard form Z_bar operators:')
        print_check_matrix(self.Z_bar)
        self.syndrome2correction = self.__generate_syndrome_map(check_matrix[1])
        # map each syndrome to a program that corrects for that

        self.encoding_program = self.__encode()
        # message qubits 0 to k-1, ancilla 0 qubits k to n-1
        # encoded codeword qubits in 0 to n-1
        print(self.encoding_program)
        self.decoding_program = self.__decode()
        # noisy encoded codeword 0 to n-1, ancilla 0 qubits n to n+k-1
        # decoded message qubits in n to n+k-1
        print(self.decoding_program)

    def __generate_syndrome_map(self, allowed_errors):
        syndrome2correction = {}
        # for each allowed error pattern, find the syndrome (basically the
        # generators that anti-commute)
        for error in allowed_errors:
            if allowed_errors[error] > 1:
                raise NotImplementedError
            elif allowed_errors[error] == 1:
                if error in ['X', 'Y', 'Z']:
                    for pos in range(self.n):
                        error_str = 'I'*pos + error + 'I'*(self.n-1-pos)
                        syndrome_list = [commutator_n_qubits(check_matrix_row2str(row),error_str) \
                                            for row in self.std_check_matrix]
                        syndrome_tuple = tuple(syndrome_list)
                        if syndrome_tuple in syndrome2correction:
                            print('Syndrome collision - might be fine for degenerate codes.')
                        else:
                            syndrome2correction[syndrome_tuple] = Program(error + ' ' +str(pos))
                elif error == 'XZ':
                    for posX in range(self.n):
                        for posZ in range(self.n):
                            if posX == posZ:
                                continue
                            error_list = ['I' for _ in range(self.n)]
                            error_list[posX] = 'X'
                            error_list[posZ] = 'Z'
                            error_str = ''.join(error_list)
                            syndrome_list = [commutator_n_qubits(check_matrix_row2str(row),error_str) \
                                                for row in self.std_check_matrix]
                            syndrome_tuple = tuple(syndrome_list)
                            if syndrome_tuple in syndrome2correction:
                                print('Syndrome collision - might be fine for degenerate codes.')
                            else:
                                syndrome2correction[syndrome_tuple] = \
                                    Program('X ' +str(posX))+Program('Z ' +str(posZ))
        return syndrome2correction

    def __encode(self) -> Program:
        # DO NOT CALL DIRECTLY, INSTEAD USE StabilizerCode.encoding_program
        # Returns program for encoding under the assumption that
        # qubits 0 through k-1 contain the state to be encoded
        # and rest of the n-k qubits start at 0. The encoded codeword
        # is put in qubits 0 through n-1
        p = Program()
        # first swap and put the first k qubits to n-k...n-1 to match section 4.2 notation
        for i in range(self.k):
            p += Program('SWAP '+str(i)+' '+str(self.n-self.k+i))

        # do the X_bar operators
        for i,row in enumerate(self.X_bar):
            for j in range(self.r,self.n-self.k):
                if row[j] == 1:
                    p += Program('CNOT '+str(self.n-self.k+i)+' '+str(j))

        # now apply Hadamards
        for i in range(self.r):
            p += Program('H '+str(i))

        # now apply Z to the qubits when M_i has a factor of Z_i
        for i in range(self.r):
            if self.std_check_matrix[i,self.n+i] == 1:
                p += Program('Z '+str(i))

        # finally apply the M_i generators conditioned on qubit i
        for i in range(self.r):
            for j in range(self.n):
                if j == i:
                    continue # already considered before
                pauli = tuple2pauli[(self.std_check_matrix[i,j],self.std_check_matrix[i,self.n+j])]
                if pauli != 'I':
                    p += Program('CONTROLLED '+pauli+' '+str(i)+' '+str(j))

        return p

    def __decode(self) -> Program:
        # DO NOT CALL DIRECTLY, INSTEAD USE StabilizerCode.decoding_program
        # returns program for decoding under the assumption that
        # qubits 0 through n-1 contain the noisy codeword.
        # The decoded message qubits are finally put in qubits n through n+k-1.

        p = Program()
        # Step 1: measure all the syndromes (this part is based on Nielsen & Chuang
        # 10th anniversary edition section 10.5.8, fig. 10.16. Also see
        # Quantum Error Correction for Beginners, VIII.B)
        syndrome_ro = p.declare('syndrome_ro', 'BIT', self.n-self.k)
        # apply Hadamards to ancilla and then conditioned on that
        # apply the stabilizer generators and then apply Hadamard again
        for i in range(self.n-self.k):
            p += Program('H '+str(self.n+i))
            for j in range(self.n):
                pauli = tuple2pauli[(self.std_check_matrix[i,j],self.std_check_matrix[i,self.n+j])]
                if pauli != 'I':
                    p += Program('CONTROLLED '+pauli+' '+str(self.n+i)+' '+str(j))
            p += Program('H '+str(self.n+i))

        for i in range(self.n-self.k):
            p += MEASURE(self.n+i, syndrome_ro[i])

        # Step 2: apply corrections based on syndromes and then reset ancilla
        # we use recursive technique to define the code, starting at depth n
        prog = {} # dictionary mapping tuples to programs
        # start from the leaves and go towards root
        for len_tuple in range(self.n-self.k,0,-1):
            for syndrome_list in itertools.product(range(2),repeat=len_tuple):
                syndrome_tuple = tuple(syndrome_list)
                if len_tuple == self.n-self.k:
                    if syndrome_tuple in self.syndrome2correction:
                        prog[syndrome_tuple] = self.syndrome2correction[syndrome_tuple]
                    else:
                        prog[syndrome_tuple] = Program()
                else:
                    prog[syndrome_tuple] = Program().if_then(syndrome_ro[len_tuple],
                                    prog[syndrome_tuple+tuple([1])],prog[syndrome_tuple+tuple([0])])

        p.if_then(syndrome_ro[0],prog[tuple([1])],prog[tuple([0])])

        # set back ancilla to 0
        for i in range(self.n-self.k):
            p += Program('RESET '+str(self.n+i))

        # Step 3: decode to get back the k message qubits (section 4.3)
        for i in range(self.k):
            for j in range(self.n):
                if self.Z_bar[i,self.n+j] == 1:
                    p += Program('CNOT '+str(j)+' '+str(self.n+i))
            for j in range(self.n):
                pauli = tuple2pauli[(self.X_bar[i,j],self.X_bar[i,self.n+j])]
                if pauli != 'I':
                    p += Program('CONTROLLED '+pauli+' '+str(self.n+i)+' '+str(j))

        return p

def commutator_1_qubit(op1, op2):
    # for op1, op2 in I, X, Y, Z, return 0 if they commute, else return 1
    assert op1 in ['I','X','Y','Z']
    assert op2 in ['I','X','Y','Z']
    if op1 == 'I' or op2 == 'I' or op1 == op2:
        return 0
    else:
        return 1

def commutator_n_qubits(op1, op2):
    assert len(op1) == len(op2)
    return sum([commutator_1_qubit(op1[i],op2[i]) for i in range(len(op1))])%2

def check_matrix_row2str(row):
    # convert to 'IIXXI' type representation
    assert len(row)%2 == 0
    n = len(row)//2
    return ''.join([tuple2pauli[(row[i], row[n+i])] for i in range(n)])

def print_check_matrix(check_matrix):
    assert np.shape(check_matrix)[1]%2 == 0
    n = np.shape(check_matrix)[1]//2
    for row in check_matrix:
        print(check_matrix_row2str(row))
    return

def convert_to_std_form(check_matrix):
    assert np.shape(check_matrix)[1]%2 == 0
    n = np.shape(check_matrix)[1]//2
    k = n - np.shape(check_matrix)[0]
    # first we perform Gaussian elimination on the check matrix
    # as in equation 4.1 of thesis (want RREF form)
    std_check_matrix = np.copy(check_matrix)
    (r, operations) = gaussian_elimination(std_check_matrix[:,:n])
    print('r:',r)
    for op in operations:
        if op[0] == 'SWAPROW':
            std_check_matrix[[op[1],op[2]],:] = std_check_matrix[[op[2],op[1]],:]
        elif op[0] == 'ADDROW':
            std_check_matrix[op[1],:] = np.mod(std_check_matrix[op[1],:]+std_check_matrix[op[2],:],2)
        elif op[0] == 'SWAPCOL':
            std_check_matrix[:,[op[1],op[2]]] = std_check_matrix[:,[op[2],op[1]]]
            std_check_matrix[:,[n+op[1],n+op[2]]] = std_check_matrix[:,[n+op[2],n+op[1]]]

    # now go to the form in eq 4.3
    (rank_E, operations) = gaussian_elimination(std_check_matrix[r:,-(n-r):])
    assert rank_E == n-k-r
    for op in operations:
        if op[0] == 'SWAPROW':
            std_check_matrix[[r+op[1],r+op[2]],:] = std_check_matrix[[r+op[2],r+op[1]],:]
        elif op[0] == 'ADDROW':
            std_check_matrix[r+op[1],:] = np.mod(std_check_matrix[r+op[1],:]+std_check_matrix[r+op[2],:],2)
        elif op[0] == 'SWAPCOL':
            std_check_matrix[:,[-(n-r)+op[1],-(n-r)+op[2]]] = std_check_matrix[:,[-(n-r)+op[2],-(n-r)+op[1]]]
            std_check_matrix[:,[-n-(n-r)++op[1],-n-(n-r)++op[2]]] = std_check_matrix[:,[-n-(n-r)+op[2],-n-(n-r)+op[1]]]

    # now write the submatrices of interest
    E = std_check_matrix[r:,-k:] # size n-k-r * k
    C_1 = std_check_matrix[:r,-(n-r):-k] # size r * n-k-r
    C_2 = std_check_matrix[:r,-k:] # size r * k
    A_2 = std_check_matrix[:r,-n-k:-n] # size r * k

    # use formulae derived towards the end of section 4.1 to compute logical X and Z operators
    X_bar = np.concatenate([np.zeros((k,r),dtype=np.uint), E.T, np.identity(k,dtype=np.uint), np.mod(np.dot(E.T,C_1.T)+C_2.T,2), np.zeros((k,n-r),dtype=np.uint)],axis=1)
    Z_bar = np.concatenate([np.zeros((k,n),dtype=np.uint), A_2.T, np.zeros((k,n-k-r),dtype=np.uint),np.identity(k,dtype=np.uint)],axis=1)
    return (r,std_check_matrix,X_bar,Z_bar)


def gaussian_elimination(original_matrix):
    # performs Gaussian elimination on an matrix to obtain the RREF form.
    # Instead of returning RREF matrix, return sequence of operations to get
    # there. This helps with doing same sequence of ops on multiple submatrices.
    # also returns rank
    matrix = np.copy(original_matrix)
    nrow = matrix.shape[0]
    ncol = matrix.shape[1]
    operations = []
    # follow steps from https://www.math.purdue.edu/~shao92/documents/Algorithm%20REF.pdf
    # we first convert to REF form
    if np.count_nonzero(matrix) == 0:
        # all zeros matrix, trivial
        return (0,operations)
    pivot_row = 0
    pivot_col = 0
    while True:
        # determine first non-zero column in submatrix below pivot position
        # and swap columns to bring it to current_column
        if np.count_nonzero(matrix[pivot_row:,pivot_col]) == 0:
            for j in range(pivot_col+1,ncol):
                if np.count_nonzero(matrix[pivot_row:,j]) > 0:
                    matrix[:,[pivot_col,j]] = matrix[:,[j,pivot_col]]
                    operations.append(('SWAPCOL',pivot_col,j))

        # first put a 1 at matrix[pivot_pos,j] if not already
        if matrix[pivot_row,pivot_col] != 1:
            for i in range(pivot_row+1,nrow):
                if matrix[i,pivot_col] == 1:
                    matrix[[pivot_row,i],:] = matrix[[i,pivot_row],:]
                    operations.append(('SWAPROW',pivot_row,i))

        # now put zeros at each matrix[i,j] for i > pivot_pos
        for i in range(pivot_row+1,nrow):
            if matrix[i,pivot_col] == 1:
                matrix[i,:] = np.mod(matrix[i,:]+matrix[pivot_row,:],2)
                operations.append(('ADDROW',i,pivot_row))

        pivot_row += 1
        pivot_col += 1
        # if no more non-zero rows below pivot, break
        non_zero_found = False
        for i in range(pivot_row, nrow):
            if np.count_nonzero(matrix[i,:]) > 0:
                non_zero_found = True
        if not non_zero_found:
            break

    rank = pivot_row

    # now convert to RREF form (make top left rank x rank = identity)
    for j in range(rank):
         for i in range(j):
             if matrix[i,j] == 1:
                 matrix[i,:] = np.mod(matrix[i,:]+matrix[j,:],2)
                 operations.append(('ADDROW',i,j))

    return (rank, operations)
