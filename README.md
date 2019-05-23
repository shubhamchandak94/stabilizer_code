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
