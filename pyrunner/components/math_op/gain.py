from .. import base_comp


class Gain(base_comp.BaseComponent):
    """This component multiplies the input value by given gain value.

    Parameters
    ----------

    - gain: int
        Value by which the input will be multiplied.

    Inputs
    ------

    - value:
        Only accepts one input of type int, array or component.

    Outputs
    -------

    - The output represents the multiplied input value.

    """

    default_name = base_comp.generate_default_name("gain")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"value"}, {"value"}),
            "outputs": ({}, {}),
            "parameters": ({}, {"gain": 1})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Gain, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        self.code_str["Execution"] = self.name + " = {0}*{1}\n".format(self.parameters["gain"], self.inputs["value"])
