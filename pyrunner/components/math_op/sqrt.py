"""
This module contains the Sqrt component.

This component performs the same operation as Simulink's Sqrt block:

- https://www.mathworks.com/help/simulink/slref/sqrt.html
"""

from .. import base_comp


# Function helpers

def _generate_string_for_sqrt(inputs, parameters):
    code_str = ""

    if parameters["type"] == ("square" or None):
        code_str = 'np.emath.sqrt({})'.format(inputs["value"])

    elif parameters["type"] == "sine":
        code_str = 'np.sin({})* (np.emath.sqrt(np.abs({})))'.format(inputs["value"], inputs["value"])

    elif parameters["type"] == "reciprocal":
        code_str = '({})**(-1/2)'.format(inputs["value"])

    return code_str


class Sqrt(base_comp.BaseComponent):
    """The Sqrt component calculates the square root, signed square root,
    or reciprocal of square root.

    Parameters
    ----------

    - name : str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

    - type : str
      A string specifying what numpy function will be used to perform the square equation:

        square : triggers numpy's amin function to calculate the minimum of the input.
        result = sqrt(value)

        sine : Square root of the absolute value of the input, multiplied by the sine
        of the input.
        result = sine(value)*sqrt(abs(value))

        reciprocal : Reciprocal of the square root.
        result = (value)**(-1/2)

    Inputs
    ------
     - Value:
        It can vary, but it must be more than or equal to one.
        :type scalar, vector, matrix or component

    Outputs
    -------
    - Output signal that is the square root, signed square root, or reciprocal of square
    root of the input signal.
    """

    default_name = base_comp.generate_default_name("sqrt")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"value"}, {"value"}),
            "outputs": ({}, {}),
            "parameters": ({"type": None}, {"type": None})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Sqrt, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        start_str = self.name + " = "
        sqrt_string = _generate_string_for_sqrt(self.inputs, self.parameters)
        self.code_str["Execution"] = start_str + sqrt_string
