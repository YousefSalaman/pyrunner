
from .. import base_comp


class Abs(base_comp.BaseComponent):

    default_name = base_comp.generate_default_name("absolute")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"input"}, {"input"}),
            "outputs": ({}, {}),
            "parameters": ({}, {})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None):

        super(Abs, self).__init__(sys_obj, name)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):

        self.code_str['Execution'] = '{} = np.abs({})'.format(self.name, self.inputs["input"].name)
