from .. import base_comp


def generate_diff_str(inputs, parameters):

    init_cond = parameters["init_cond"]
    input_comp = inputs["value"]

    setup_str = "{0}_prev_cond = {1}".format(input_comp.name, init_cond)

    difference_str = "{0} - {0}_prev_cond\n" \
                     "\t{0}_prev_cond = {0}".format(input_comp.name)

    return setup_str, difference_str


class Difference(base_comp.BaseComponent):
    """The difference component subtracts the previous value stored from
    the currently received value.

    Parameters
    ----------

    - name: str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

    - init_cond: int
        First value that is going to be subtracted from the first input. The
        default value is zero (0).

    Inputs
    ------

    - value:
        Only accepts one input of type: scalar, vector or component.

    Outputs
    -------

    - Output value that represents the difference of the current value
    minus the previous value.
    """

    default_name = base_comp.generate_default_name("diff")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"value"}, {"value"}),
            "outputs": ({}, {}),
            "parameters": ({}, {"init_cond": 0})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Difference, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        start_str = self.name + " = "

        setup_str, difference_str = generate_diff_str(self.inputs, self.parameters)

        self.code_str["Set Up"] = setup_str
        self.code_str["Execution"] = start_str + difference_str
