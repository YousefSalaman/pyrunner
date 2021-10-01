from ..systems import BaseSubsystem
from .. import base_comp
from .gain import Gain
from .gain_proto import NewGain
from .integrator import Integrator
from .derivative import Derivative
from .sum import Sum
from ..sources.constant import Constant


class PID(BaseSubsystem):

    default_name = base_comp.generate_default_name("pid")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    prop_info = base_comp.generate_prop_info(
        {

            "inputs": ({"setpoint", "measurement"}, {"setpoint", "measurement"}),
            "outputs": ({"pid"}, {"pid"}),
            "parameters": ({}, {"proportional_gain": 0, "integral_gain": 0,
                                "derivative_gain": 0, "init_cond": 0, "sample_time": 1})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(PID, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def _create_components(self):

        self.error_sum = Sum(self, comp_signs=["+", "-"], name="error")

        comp_count = 3 - [self.parameters["proportional_gain"], self.parameters["integral_gain"],
                          self.parameters["derivative_gain"]].count(0)

        self.pid_sum = Sum(self, comp_signs=comp_count*["+"], name="pid_sum")
        self.pid_sum.code_str["Set Up"] = "{} = 0".format(self.pid_sum.name)

        if self.parameters["proportional_gain"]:
            self.proportional = NewGain(self, gain=self.parameters["proportional_gain"], name="proportional")
            # self.proportional = Gain(self, upper_limit=500, name="proportional")
            # self.prop_gain = Constant(self, value=self.parameters["proportional_gain"], name="proportional_gain")
            self.proportional.inputs.update({"value": self.error_sum})
            # self.proportional.inputs.update({"gain": self.prop_gain})
            self.pid_sum.inputs.add(self.proportional)

        if self.parameters["integral_gain"]:
            self.integral = Integrator(self, init_cond=self.parameters["init_cond"],
                                       sample_time=self.parameters["sample_time"], name="integral")
            self.integral.inputs.update({"value": self.error_sum})
            self.pid_sum.inputs.add(self.integral)

        if self.parameters["derivative_gain"] and self.parameters["proportional_gain"]:
            self.derivative = Derivative(self, init_cond=self.parameters["init_cond"],
                                         sample_time=self.parameters["sample_time"], name="derivative")
            self.derivative.inputs.update({"value": self.error_sum})
            self.pid_sum.inputs.add(self.derivative)

        self.outputs.update({"pid": self.pid_sum})

    def verify_properties(self):
        self.error_sum.inputs.add(self.inputs["setpoint"])
        self.error_sum.inputs.add(self.inputs["measurement"])
        super().verify_properties()
