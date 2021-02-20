
from Simupynk.Simupynk.components import *


def generate_final_code_string(diagram):

    inf_loop = "while True:"
    yield_statement = "yield "
    import_statement = "import numpy as np\n"

    code_str = import_statement + f"def {diagram.name}():"

    for comp in diagram.builder.ordered_comps:
        if comp.code_str["Set Up"]:
            code_str += "\n\t" + comp.code_str["Set Up"]

    code_str += "\n\t" + inf_loop

    for comp in diagram.builder.ordered_comps:
        if comp.code_str["Execution"]:
            code_str += "\n\t\t" + comp.code_str["Execution"]

    code_str += "\n\t\t" + yield_statement + ", ".join(comp.name for comp in diagram.outputs.values())
    return code_str


if __name__ == "__main__":

    main_sys = systems.BlockDiagram("main_sys", "seq")  # Initialize the BlockDiagram

    # Add constant sources
    const = sources.Constant(main_sys)
    const_1 = sources.Constant(main_sys)
    const_2 = sources.Constant(main_sys)
    const_3 = sources.Constant(main_sys)

    # Add values to constant sources
    const.parameters.add(value=42)
    const_1.parameters.add(value=3.1415)
    const_2.parameters.add(value='np.array([1,2,3])')
    const_3.parameters.add(value=1)

    # Add the Sum blocks
    adder = math_op.Sum(main_sys)
    adder_1 = math_op.Sum(main_sys)
    adder_2 = math_op.Sum(main_sys)

    # Add the inputs and parameters to the Sum blocks
    adder_1.inputs.add(const_1, const_2, const_3)
    adder_1.parameters.add(comp_signs='+--')

    adder_2.inputs.add(const_2)
    adder_2.parameters.add(comp_signs='-')

    adder.inputs.add(adder_1, adder_2)
    adder.parameters.add(comp_signs="-+")

    main_sys.outputs.add(adder)  # Say the "adder" component is the output
    main_sys.build_diagram()
    generator_str = generate_final_code_string(main_sys)

    print(generator_str)
