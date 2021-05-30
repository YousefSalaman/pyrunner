
from .. import base_comp


class Constant(base_comp.BaseComponent):

    default_name = base_comp.generate_default_name("const")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({}, {}),
            "outputs": ({}, {}),
            "parameters": ({"value"}, {"value"})
         }
    )

    def __init__(self, sys_obj, name=None, lib_deps=None, **parameters):

        super(Constant, self).__init__(sys_obj, name, **parameters)
        if lib_deps is not None:
            self._lib_deps = lib_deps

    def generate_code_string(self):

        self.code_str['Set Up'] = '{} = '.format(self.name) + str(self.parameters['value'])

    def verify_properties(self):

        super(Constant, self).verify_properties()
        if not isinstance(self._lib_deps, (type(None), dict)):
            raise TypeError("The argument 'lib_deps' must be a dictionary.")
