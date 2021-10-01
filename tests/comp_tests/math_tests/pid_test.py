from pyrunner.components import *

MAIN_SYS = systems.BlockDiagram("main_sys", "seq")


def pid_test():
    const = sources.Constant(MAIN_SYS, value=8)
    pid = math_op.PID(MAIN_SYS, proportional_gain=3, integral_gain=7, derivative_gain=2, init_cond=8, sample_time=0.2)
    pid.inputs.update({"setpoint": const})
    pid.inputs.update({"measurement": pid})
    MAIN_SYS.outputs.add(pid)
    MAIN_SYS.build(create_code=False)
    MAIN_SYS.remove_components(pid)
