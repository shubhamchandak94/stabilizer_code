import numpy as np
from pyquil import Program
from pyquil.gates import MEASURE, I, CNOT, X, H, Z
import stabilizer_code
import stabilizer_check_matrices
import sys
from pyquil.api import QVMConnection

import basic_tests


# The goal of this program is to create a function that takes as input 
# 1. A stabilizer code (described via its stabilizers)
# 2. A parametrized noise model (the parameter corresponds to the physical error rate)
# and output a plot of the logical vs physical error rates achieved






























