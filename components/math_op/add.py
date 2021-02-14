
from collections.abc import Sequence

import Simupynk.components.base_comp as base_comp


_OUTPUT_INFO = ({},
                {})

_PARAMETER_INFO = ({"comp_signs"},
                   {"comp_signs"})


class Add(base_comp.BaseComponent):
    """
    A component that performs addition and subtraction with its inputs.
    """

    default_name = base_comp.generate_default_name("add")

    has_init_cond = base_comp.generate_has_init_cond(False)

    input_info = base_comp.generate_input_info(None)

    output_info = base_comp.generate_output_info(_OUTPUT_INFO)

    parameter_info = base_comp.generate_parameter_info(_PARAMETER_INFO)

    def generate_component_string(self):

        start_str = f"{self.name} = "
        inputs = self.inputs.organize_property()
        comp_signs = self.parameters["comp_signs"]

        # Generate the sum
        sum_str = ""
        for comp, comp_sign in zip(inputs, comp_signs):
            sum_str += comp_sign + comp.name

        # Eliminate plus if the sum starts with it
        if sum_str.startswith("+"):
            sum_str = sum_str.split("+", 1)[1]

        self.code_str["Execution"] = start_str + sum_str

    def verify_component_properties(self):

        comp_signs = self.parameters["comp_signs"]
        super().verify_component_properties()

        if not isinstance(comp_signs, Sequence):
            raise TypeError('The parameter "comp_signs" must be a sequence.')

        if len(self.inputs) < 2:
            raise ArithmeticError('The Add component performs binary operations, '
                                  'so it requires a minimum of two inputs.')

        if len(comp_signs) != len(self.inputs):
            raise AttributeError('The length of the parameter "comp_sign" and the amount of inputs must be the same.')

        if not all(isinstance(comp_sign, str) and comp_sign.strip() in ('+', '-') for comp_sign in comp_signs):
            raise TypeError('All the ')
