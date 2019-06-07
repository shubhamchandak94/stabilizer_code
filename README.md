# Stabilizer codes
Implementation of stabilizer codes in pyQuil

CS269Q Spring 2018-19 course project

Authors: Shubham Chandak, Jay Mardia, Meltem Tolunay

Instructor: Will Zeng


## Installation
Follow instructions to install qvm and quilc from http://docs.rigetti.com/en/stable/.
Then just run
```
git clone https://github.com/shubhamchandak94/stabilizer_code
```
to download the code.

## Defining a stabilizer code
The stabilizer codes are defined here in terms of the stabilizer generator matrix and the error correction capabilities of the code. The error correction capability is defined in terms of a dictionary mapping the error type to the number of such errors the code can correct. Currently supported error types are X, Y, Z on single qubits and a combination of X and Z on different qubits. Some examples of stabilizer codes along with the parameters are provided in `stabilizer_check_matrices.py`.

## Generating programs for encoding and decoding a stabilizer code
Given a stabilizer code representation `my_stabilizer_code` in the format as described above, run the following
```python
import stabilizer_code
code = stabilizer_code.StabilizerCode(my_stabilizer_code)
```

Then `code.encoding_program` and `code.decoding_program` are the encoding and decoding programs, respectively.

## Running basic tests
First run `qvm -S` and `quilc -S` before running any tests.

Several standard stabilizer matrices are defined in `stabilizer_check_matrices.py`

To run basic tests (bit flip, phase flip etc. with different initial states) for
all codes in above file, run
`
python3 basic_tests.py
`

To run basic tests for a specific code, run with the name of the code, e.g.,
`
python3 basic_tests.py bit_flip_code
`
