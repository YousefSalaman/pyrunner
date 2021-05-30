import pyrunner.runners.seq_runner as seq_runner
import numpy as np


def main_sys():
	const = 3.1415
	const_1 = np.array([1,2,3])
	const_2 = 1
	yield 
	while True:
		add_1 = const-const_1-const_2
		add_2 = -np.sum(const_1)
		add = -add_1+add_2
		yield {"add": add, "add_1": add_1}


main_sys_exec = seq_runner.Executor("main_sys", main_sys(), [])