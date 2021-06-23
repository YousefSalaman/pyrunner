"""
This module contains the Sqrt component.

This component performs the same operation as Simulink's Sqrt block:

- https://www.mathworks.com/help/simulink/slref/sqrt.html
"""

from .. import base_comp


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
            "parameters": ({}, {})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Sqrt, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):

        self.code_str['Execution'] = '{} = np.emath.sqrt({})'.format(self.name, self.inputs["value"])
