
import Simupynk.components.base_comp as base_comp


_INPUT_INFO = ({},
               {})

_PARAMETER_INFO = ({'value'},
                   {'value'})


class Constant(base_comp.BaseNormalComponent):

    default_name = base_comp.generate_default_name("const")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    input_info = base_comp.generate_input_info(_INPUT_INFO)

    parameter_info = base_comp.generate_parameter_info(_PARAMETER_INFO)

    def generate_component_string(self):

        self.code_str['Set Up'] = f'{self.name} = ' + str(self.parameters['value'])
