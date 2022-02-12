from pyrunner.components import *

MAIN_SYS = systems.BlockDiagram("main_sys", "seq")


def pid_test():
    const = sources.Constant(MAIN_SYS, value=8)
    pid = math_op.PID(MAIN_SYS, proportional_gain=3, integral_gain=7, derivative_gain=2,
                      integral_init_cond=8, derivative_init_cond=8, sample_time=0.2)
    gain = math_op.Gain(MAIN_SYS, gain=1)
    gain.inputs.update({"value": pid.outputs["pid"]})
    pid.inputs.update({"setpoint": const})
    pid.inputs.update({"measurement": gain})
    MAIN_SYS.outputs.add(gain)
    MAIN_SYS.comps += pid.comps
    MAIN_SYS.build(create_code=False)
    MAIN_SYS.remove_components(pid)


def pi_test():
    const = sources.Constant(MAIN_SYS, value=8)
    pid = math_op.PID(MAIN_SYS, proportional_gain=3, integral_gain=7, integral_init_cond=8, sample_time=0.2)
    pid.inputs.update({"setpoint": const})
    pid.inputs.update({"measurement": pid.outputs["pid"]})
    MAIN_SYS.outputs.add(pid.outputs["pid"])
    MAIN_SYS.comps += pid.comps
    MAIN_SYS.build(create_code=False)
    MAIN_SYS.remove_components(pid)


def derivative_only_error():
    const = sources.Constant(MAIN_SYS, value=8)
    pid = math_op.PID(MAIN_SYS, derivative_gain=5)
    pid.inputs.update({"setpoint": const})
    pid.inputs.update({"measurement": pid.outputs["pid"]})
    MAIN_SYS.outputs.add(pid.pid_sum)
    MAIN_SYS.build(create_code=False)
    MAIN_SYS.remove_components(pid)


def all_gains_zero_error():
    const = sources.Constant(MAIN_SYS, value=8)
    pid = math_op.PID(MAIN_SYS)
    pid.inputs.update({"setpoint": const})
    pid.inputs.update({"measurement": pid.outputs["pid"]})
    MAIN_SYS.outputs.add(pid.pid_sum)
    MAIN_SYS.build(create_code=False)
    MAIN_SYS.remove_components(pid)


def integral_derivative_error():
    const = sources.Constant(MAIN_SYS, value=8)
    pid = math_op.PID(MAIN_SYS, integral_gain=7, derivative_gain=2, sample_time=0.2)
    print(pid.parameters)
    pid.inputs.update({"setpoint": const})
    pid.inputs.update({"measurement": pid.outputs["pid"]})
    MAIN_SYS.outputs.add(pid.pid_sum)
    MAIN_SYS.build(create_code=False)
    MAIN_SYS.remove_components(pid)
