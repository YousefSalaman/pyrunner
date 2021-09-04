from .. import base_comp


def generate_derivative_str(inputs, parameters):
    init_cond, sample_time = parameters["init_cond"], parameters["sample_time"]
    input_comp = inputs["value"]

    setup_str = "{0}_prev_cond = {1}".format(input_comp.name, init_cond)

    difference_str = "(({0} - {0}_prev_cond) / {1})\n" \
                     "\t{0}_prev_cond = {0}\n".format(input_comp.name, sample_time)

    return setup_str, difference_str


class Derivative(base_comp.BaseComponent):
    """A component that calculates the discrete time derivative of the input.

    Parameters
    ----------

    - name: str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

    - init_cond: int
        First reference value to calculate the derivative. The default value is
        zero (0).

    - sample_time: int
        Time between each input and previous values. This value cannot be zero (0).
        The default value is one (1).

    Inputs
    ------

    - value:
        Only accepts one input of type: int, array or component.

    Outputs
    -------

    - The output represents the discrete time derivative of the input based on
    the previous condition stored on the component or the initial condition.

    - This simply subtracts the initial or previous condition from the input
    value and then divides that result by the sample time.

    """

    default_name = base_comp.generate_default_name("derivative")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"value"}, {"value"}),
            "outputs": ({}, {}),
            "parameters": ({}, {"init_cond": 0, "sample_time": 1}),
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Derivative, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        if self.parameters["sample_time"] == 0:
            raise ZeroDivisionError("sample_time cannot be equal to zero (0)")

        start_str = self.name + " = "

        setup_str, derivative_str = generate_derivative_str(self.inputs, self.parameters)

        self.code_str["Set Up"] = setup_str
        self.code_str["Execution"] = start_str + derivative_str
