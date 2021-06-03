import numpy as np
import pyrunner.runners.seq_runner as seq_runner


def simple_adder():
	const = 3.1415
	const_1 = np.array([1,2,3])
	const_2 = 1
	yield 
	while True:
		add_2 = -np.sum(const_1)
		add_1 = const-const_1-const_2
		add = -add_1+add_2
		yield {"add": add}


simple_adder_exec = seq_runner.Executor("simple_adder", simple_adder(), [])

