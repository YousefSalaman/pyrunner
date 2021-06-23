"""
This module contains the Saturation component.

This component performs the same operation as Simulink's Saturation block:

- https://www.mathworks.com/help/simulink/slref/saturation.html#f8-893573
"""
from .. import base_comp


class Saturation(base_comp.BaseComponent):
    """A component that produces an output signal that is the value of the input signal
    bounded to the upper and lower saturation values. For this component to work properly
    it needs an input signal value and the specified parameter (upper_limit and lower_limit).

    Parameters
    ----------

    - name : str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

    - lower_limit : int
        Positive or negative integer that specifies the lower limit of the input signal.
        If the input signal is less than this boundary, then the output signal is set
        to this saturation value and the parameter will be converted into the output.
        The lower limit must also be greater than the out_min parameter and less
        than the out_max parameter. The default is none and this will simply execute
        the saturation without an lower limit.

    - upper_limit : int
        Positive or negative integer that specifies the upper limit of the input signal.
        If the input signal is greater than this boundary, then the output signal is set
        to this saturation value and the parameter will be converted into the output.
        The upper limit must also be greater than the out_min parameter and less
        than the out_max parameter. The default is none and this will simply execute
        the saturation without an upper limit.

    Inputs
    ------
    - Value:
        It can vary, but it must be more than or equal to one.
        :type scalar, vector, matrix or component


     Outputs
     -------
     - Output:
        Output signal that is the value of the input signal, upper saturation limit,
        or lower saturation limit.

    """

    default_name = base_comp.generate_default_name("saturation")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"value"}, {"value"}),
            "outputs": ({}, {}),
            "parameters": ({}, {"low_lim": None, "up_lim": None})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Saturation, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        start_str = self.name + " = "
        saturation_str = 'np.clip({},{},{})'.format(self.inputs['value'],
                                                    self.parameters["low_lim"],
                                                    self.parameters["up_lim"])

        self.code_str['Execution'] = start_str + saturation_str

    def verify_properties(self):
        if self.parameters["low_lim"] is None and self.parameters["up_lim"] is None:
            raise AttributeError("Both Limits cannot be None. Insert a value to at least 1 limit.")
        super(Saturation, self).verify_properties()
