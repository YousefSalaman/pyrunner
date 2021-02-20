
from ..base_comp import *


_INPUT_INFO = ({},
               {})

_PARAMETER_INFO = ({'value'},
                   {'value'})


class Constant(BaseNormalComponent):

    default_name = generate_default_name("const")

    direct_feedthrough = generate_direct_feedthrough(False)

    input_info = generate_input_info(_INPUT_INFO)

    parameter_info = generate_parameter_info(_PARAMETER_INFO)

    def generate_component_string(self):

        self.code_str['Set Up'] = f'{self.name} = ' + str(self.parameters['value'])
