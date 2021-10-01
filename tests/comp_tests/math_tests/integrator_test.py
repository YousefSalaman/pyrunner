import pytest
from pyrunner.components import *

MAIN_SYS = systems.BlockDiagram("main_sys", "seq")


def integrator_test():
    const = sources.Constant(MAIN_SYS, value="np.array([1, 5, 6])")
    integral = math_op.Integrator(MAIN_SYS, init_cond=1, sample_time=0.4)
    integral.inputs.update({"value": const})
    MAIN_SYS.outputs.add(integral)
    MAIN_SYS.build(file_path=r"C:\Users\kevin\PycharmProjects\pyrunner\tests\comp_tests\math_tests\integrator_run.py")
    MAIN_SYS.remove_components(integral)