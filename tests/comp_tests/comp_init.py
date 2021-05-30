import pyrunner.components as comps


INPUT_INFO = (
    {"test", "test1", "test2"},  # Required inputs properties
    {"test", "test1", "test2", "test3"}  # All input properties
)

OUTPUT_INFO = (
    {},  # Required outputs properties
    {}  # All run properties
)

PARAMETER_INFO = (
    {"para", "para1"},  # Required parameters
    {"para", "para1", "para2"}  # All parameters
)


class InitCompDependent(comps.BaseComponent):

    direct_feedthrough = comps.generate_direct_feedthrough(True)

    input_info = comps.generate_input_info(INPUT_INFO)

    output_info = comps.generate_output_info(OUTPUT_INFO)

    parameter_info = comps.generate_parameter_info(PARAMETER_INFO)

    default_name = comps.generate_default_name("test_var")

    def generate_component_string(self):

        print("Just a test")
        super(InitCompDependent).generate_code_string()


class InitCompInvariant(comps.BaseComponent):

    direct_feedthrough = comps.generate_direct_feedthrough(True)

    input_info = comps.generate_input_info(None)

    output_info = comps.generate_output_info(None)

    parameter_info = comps.generate_parameter_info(None)

    default_name = comps.generate_default_name("test_inv")

    def generate_component_string(self):

        print("Just a test")
        super(InitCompInvariant, self).generate_code_string()


class InitCompSystem(comps.BaseSubsystem):

    direct_feedthrough = comps.generate_direct_feedthrough(True)

    input_info = comps.generate_input_info(None)

    output_info = comps.generate_output_info(None)

    parameter_info = comps.generate_parameter_info(None)

    default_name = comps.generate_default_name("System")

    def generate_component_string(self):

        print("Just a test")
        super(InitCompSystem, self).generate_code_string()