from ..systems import BaseSubsystem
from .. import base_comp
from .gain import Gain
from .integrator import Integrator
from .derivative import Derivative
from .sum import Sum


class PID(BaseSubsystem):
    """This component can implement controllers of the types: PID, PI,
    PD, P or I.

    Parameters
    ----------

    - proportional_gain: int
        Gain value for the proportional part of the controller. By default
        this value is zero (0).

    - integral_gain: int
        Gain value for the integral part of the controller. By default this
        value is zero (0).

    - derivative_gain: int
        Gain value for the derivative part of the controller. By default this
        value is zero (0).

    -  integral_init_cond: int
        This represents the area under the input signal up until the point
        previous to the current point being evaluated. By default this value
        is zero (0).

    - derivative_init_cond: int
        This represents the previous input value needed to calculate the
        discrete time derivative.

    - sample_time: int
        Time that passes for a new sample to be taken. By default this value
        is one (1).

    Inputs
    ------

    - setpoint:
        This input should receive the input component to the PID.

    - measurement:
        This input should receive the component that is measured and fed back
        into the error sum of the PID.

    Outputs
    -------

    - pid: pid_sum
        The output of this component is the sum of the proportional, integral
        and derivative parts of the PID.

    """

    default_name = base_comp.generate_default_name("pid")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    prop_info = base_comp.generate_prop_info(
        {

            "inputs": ({"setpoint", "measurement"}, {"setpoint", "measurement"}),
            "outputs": ({"pid"}, {"pid"}),
            "parameters": ({}, {"proportional_gain": 0, "integral_gain": 0, "derivative_gain": 0,
                                "integral_init_cond": 0, "derivative_init_cond": 0, "sample_time": 1})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(PID, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def _create_components(self):

        self.error_sum = Sum(self, comp_signs=["+", "-"])

        self.pid_comps = 3 - [self.parameters["proportional_gain"], self.parameters["integral_gain"],
                              self.parameters["derivative_gain"]].count(None)

        if not self.pid_comps:
            raise TypeError("All pid gains cannot be zero. At least a proportional or integral gain must be defined.")

        if self.pid_comps == 1 and self.parameters["derivative_gain"]:
            raise TypeError("The pid controller cannot be only derivative.")

        if self.pid_comps == 2 and not self.parameters["proportional_gain"]:
            raise TypeError("The pid controller cannot be integral-derivative")

        self.pid_sum = Sum(self, comp_signs=self.pid_comps*["+"])

        if self.parameters["proportional_gain"]:
            self.proportional = Gain(self, gain=self.parameters["proportional_gain"])
            self.proportional.inputs.update({"value": self.error_sum})
            self.pid_sum.inputs.add(self.proportional)

        if self.parameters["integral_gain"]:
            self.integral = Integrator(self, init_cond=self.parameters["integral_init_cond"],
                                       sample_time=self.parameters["sample_time"])
            self.integral.inputs.update({"value": self.error_sum})
            self.gained_integral = Gain(self, gain=self.parameters["integral_gain"])
            self.gained_integral.inputs.update({"value": self.integral})
            self.pid_sum.inputs.add(self.gained_integral)

        if self.parameters["derivative_gain"] and self.parameters["proportional_gain"]:
            self.derivative = Derivative(self, init_cond=self.parameters["derivative_init_cond"],
                                         sample_time=self.parameters["sample_time"])
            self.derivative.inputs.update({"value": self.error_sum})
            self.gained_derivative = Gain(self, gain=self.parameters["derivative_gain"])
            self.gained_derivative.inputs.update({"value": self.derivative})
            self.pid_sum.inputs.add(self.gained_derivative)

        self.outputs.update({"pid": self.pid_sum})

    def verify_properties(self):

        self.error_sum.inputs.add(self.inputs["setpoint"])
        self.error_sum.inputs.add(self.inputs["measurement"])

        init_cond_str = str([0]*self.pid_comps)
        var_arr = []

        if self.parameters["proportional_gain"]:
            var_arr.append(self.proportional)

        if self.parameters["integral_gain"]:
            var_arr.append(self.gained_integral)

        if self.parameters["derivative_gain"]:
            var_arr.append(self.gained_derivative)

        var_str = str(var_arr)
        self.code_str["Set Up"] = "{} = {}".format(var_str, init_cond_str)

        super().verify_properties()
