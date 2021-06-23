"""
This module contains the Exponent component.

"""

from .. import base_comp


class Exponent(base_comp.BaseComponent):
    """
    TODO: Description

    Parameters
    ----------
    - name : str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

    - Exponent:

    Inputs
    ------
    TODO:

    Outputs
    -------
    TODO:

    """

    default_name = base_comp.generate_default_name("exp")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"base"}, {"base"}),
            "outputs": ({}, {}),
            "parameters": ({"exp"}, {"exp"})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Exponent, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        start_str = self.name + " = "
        exp_string = '({})**({})'.format(self.name, self.inputs["base"], self.parameters["exp"])
        self.code_str["Execution"] = start_str + exp_string
