from .. import base_comp


def generate_integral_str(comp_name, inputs, parameters):
    init_cond, sample_time = parameters["init_cond"], parameters["sample_time"]
    input_comp = inputs["value"]

    setup_str = "{0}_prev_cond = {1}".format(comp_name, init_cond)

    difference_str = "{0}_prev_cond + {1}*{2}\n" \
                     "\t{0}_prev_cond = {0}\n".format(comp_name, sample_time, input_comp.name)

    return setup_str, difference_str


class Integrator(base_comp.BaseComponent):

    default_name = base_comp.generate_default_name("integral")

    direct_feedthrough = base_comp.generate_direct_feedthrough(False)

    prop_info = (
        {
            "inputs": ({"value"}, {"value"}),
            "outputs": ({}, {}),
            "parameters": ({}, {"init_cond": 0, "sample_time": 1})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Integrator, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        if self.parameters["sample_time"] == 0:
            raise ArithmeticError("The sample time can't be zero in order to calculate the integral.")

        start_str = self.name + " = "

        setup_str, integral_str = generate_integral_str(self.name, self.inputs, self.parameters)

        self.code_str["Set Up"] = setup_str
        self.code_str["Execution"] = start_str + integral_str
