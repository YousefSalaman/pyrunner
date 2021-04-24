
from ..base_comp import *


_INPUT_INFO = ({"input"},
               {"input"})

_PARAMETER_INFO = ({},
                   {})


class Abs(BaseNormalComponent):

    default_name = generate_default_name("absolute")

    direct_feedthrough = generate_direct_feedthrough(True)

    input_info = generate_input_info(_INPUT_INFO)

    parameter_info = generate_parameter_info(_PARAMETER_INFO)

    def generate_code_string(self):

        self.code_str['Execution'] = f'{self.name} = np.abs({self.inputs["input"].name})'
