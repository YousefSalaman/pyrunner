"""
This module contains the Sum component.

This component performs the same operation as Simulink's Sum block:

- https://www.mathworks.com/help/simulink/slref/add.html
"""

import sys
if sys.version_info[:2] <= (2, 7):  # If Python 2.7 or lower
    from collections import Sequence
else:
    from collections.abc import Sequence

from .. import base_comp


# Function helpers

def _generate_string_for_normal_addition(inputs, parameters):

    comp_signs = parameters["comp_signs"]

    # Generate the sum
    sum_str = ""
    for comp, comp_sign in zip(inputs, comp_signs):
        sum_str += comp_sign + comp.name

    # Eliminate plus if the sum starts with it
    if sum_str.startswith("+"):
        sum_str = sum_str.split("+", 1)[1]

    return sum_str


def _generate_string_for_dimension_sum(inputs, parameters):

    sum_str = "np.sum({}".format(inputs[0].name)

    # Sum negative sign
    comp_sign = parameters["comp_signs"][0].strip()
    if comp_sign == '-':
        sum_str = '-' + sum_str

    # Write dimension parameter
    dim = parameters['dimension']
    if dim is not None:
        sum_str += ",axis={}".format(dim)

    # Sum dytpe parameter
    dtype = parameters['dtype']
    if dtype is not None:
        sum_str += ",dtype=np.{}".format(dtype)

    return sum_str + ")"


def _verify_comp_signs(comp_signs, input_len):

    if not isinstance(comp_signs, Sequence):
        raise TypeError('The parameter "comp_signs" must be a sequence.')

    if len(comp_signs) != input_len:
        raise AttributeError('The length of the parameter "comp_sign" and the amount of inputs must be the same.')

    if not all(isinstance(comp_sign, str) and comp_sign.strip() in ('+', '-') for comp_sign in comp_signs):
        raise TypeError('All of the elements of "comp_signs" must be either one of these strings: "+", "-".')


def _verify_for_dimension_addition(parameters):

    dim = parameters["dimension"]
    if not (isinstance(dim, type(None)) or (isinstance(dim, int) and dim >= 0)):
        raise TypeError('The "dimension" parameter must be a non-negative integer.')

    if not isinstance(parameters['dtype'], (str, type(None))):
        raise TypeError('The parameter "dtype" must be a string with the name of the dtype. '
                        'For example, "float64" and "int32" are dtype names.')


# Sum component definition


class Sum(base_comp.BaseComponent):
    """A component that performs addition and subtraction with its inputs.

    If the component has only one input, it will sum over the input vector/matrix.
    You can control over what dimension/axis it sums over by specifying it in the
    dimension parameter. By default, it will sum over all of the components of the
    inputs.

    If the component has more than one input, then it will find the sum of the
    inputs. All of the inputs must be of the same dimension.

    In both case, you need to specify the sign of each component through the
    comp sign parameter with an object that is considered a "Sequence" like
    a tuple, string, list, etc. For example:

    - Assume the input is the component "a", then comp_sign must be of the
      same length and it can be one of the following if it has to be a sum
      "+", ["+"], or ("+",).

    - Assume the inputs are the components "a", "b", where "c" and "a" is positive,
      "b" is negative, and "c" is positive , then comp_sign must be of the same
      length and it can be of the following to represent this "+-+", ["+","-","+"],
      or ("+","-","+").

    Parameters
    ----------

    - name : str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

    - comp_signs : Sequence
        Sequence of characters specifying the sign of a number. This is a required
        parameter.

    - dimension : int
        Positiver integer that specifies over what dimension to sum over. This is only
        relevant if the component has one input. The default is None and this will sum
        over all of the input component's elements.

    - dtype : str
        A string specifying what numpy dtype to use to perform the sum. This is only
        relevant if the component has one input. The default is None and this will
        just use the dtype of the input component.

    Inputs
    ------

    - It can vary, but it must be more than or equal to one.

    Outputs
    -------

    - The sum of the inputs if there is more than input. Otherwise, it will be
      the sum of the elements in a specified dimension or all the elements of
      the given input.
    """

    default_name = base_comp.generate_default_name("add")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": None,
            "outputs": ({}, {}),
            "parameters": ({"comp_signs"},
                           {"comp_signs": None, "dimension": None, "dtype": None})
        }
    )

    def generate_code_string(self):

        start_str = self.name + " = "
        inputs = self.inputs.sort()

        if len(inputs) == 1:
            sum_str = _generate_string_for_dimension_sum(inputs, self.parameters)
        else:
            sum_str = _generate_string_for_normal_addition(inputs, self.parameters)

        self.code_str["Execution"] = start_str + sum_str

    def verify_properties(self):

        super(Sum, self).verify_properties()

        input_len = len(self.inputs)
        _verify_comp_signs(self.parameters["comp_signs"], input_len)
        if input_len >= 1:
            if input_len == 1:
                self._lib_deps = {"numpy": "np"}  # Add numpy to the library
            _verify_for_dimension_addition(self.parameters)
        else:
            raise AttributeError("The Sum component must contain at least one input.")
