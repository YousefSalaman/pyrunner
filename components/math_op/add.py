
from collections.abc import Sequence

import Simupynk.components.base_comp as base_comp


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

    sum_str = f"np.sum({inputs[0].name}"

    # Add negative sign
    comp_sign = parameters["comp_signs"][0].strip()
    if comp_sign == '-':
        sum_str = '-' + sum_str

    # Write dimension parameter
    dim = parameters['dimension']
    if dim is not None:
        sum_str += f",axis={dim}"

    # Add dytpe parameter
    dtype = parameters['dtype']
    if dtype is not None:
        sum_str += f",dtype=np.{dtype}"

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
                        'For example, "float64" and "int32" are dtype names. ')


# Add component definition

_PARAMETER_INFO = ({"comp_signs"},
                   {"comp_signs": None, "dimension": None, "dtype": None})


class Add(base_comp.BaseNormalComponent):
    """
    A component that performs addition and subtraction with its inputs.
    """

    default_name = base_comp.generate_default_name("add")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    input_info = base_comp.generate_input_info(None)

    parameter_info = base_comp.generate_parameter_info(_PARAMETER_INFO)

    def generate_component_string(self):

        start_str = f"{self.name} = "
        inputs = self.inputs.organize_property()

        if len(inputs) == 1:
            sum_str = _generate_string_for_dimension_sum(inputs, self.parameters)
        else:
            sum_str = _generate_string_for_normal_addition(inputs, self.parameters)

        self.code_str["Execution"] = start_str + sum_str

    def verify_component_properties(self):

        super().verify_component_properties()

        input_len = len(self.inputs)
        _verify_comp_signs(self.parameters["comp_signs"], input_len)
        if input_len >= 1:
            _verify_for_dimension_addition(self.parameters)
        else:
            raise AttributeError("The Add component must contain at least one input.")
