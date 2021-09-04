from ..systems import BaseSubsystem
from .. import base_comp
from .derivative import Derivative
from .sum import Sum


class PID(BaseSubsystem):

    default_name = base_comp.generate_default_name("pid")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    prop_info = base_comp.generate_prop_info(
        {

            "inputs": ({"value"}, {"value"}),
            "outputs": ({"pid"}, {"pid"}),
            "parameters": ({}, {"proportional_gain": 1, "integral_gain": 0,
                                "derivative_gain": 0, "init_cond": 0, "sample_time": 1})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(PID, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def _create_components(self):

        self.error_sum = Sum(self, comp_signs=["+", "-"])
        self.error_sum.inputs.add(self.inputs, self.pid_sum)

        comp_count = 3 - [self.parameters["proportional_gain"], self.parameters["integral_gain"],
                          self.parameters["derivative_gain"]].count(0)

        self.pid_sum = Sum(self, comp_signs=comp_count*"+")

        if self.parameters["proportional_gain"] != 0:
            self.proportional = Gain(self, gain=self.parameters["proportional_gain"])
            self.proportional.inputs.update({"value": self.error_sum})
            self.pid_sum.inputs.add(self.proportional)

        if self.parameters["integral_gain"] != 0:
            self.integral = Integral(self, init_cond=self.parameters["init_cond"],
                                     sample_time=self.parameters["sample_time"])
            self.integral.inputs.update({"value": self.error_sum})
            self.pid_sum.inputs.add(self.integral)

        if self.parameters["derivative_gain"] != 0:
            self.derivative = Derivative(self, init_cond=self.parameters["init_cond"],
                                         sample_time=self.parameters["sample_time"])
            self.derivative.inputs.update({"value": self.error_sum})
            self.pid_sum.inputs.add(self.derivative)

        self.outputs.update({"pid": self.pid_sum})

