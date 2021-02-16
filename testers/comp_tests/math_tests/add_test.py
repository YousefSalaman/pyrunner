from Simupynk.components import *


if __name__ == "__main__":

    main_sys = systems.BlockDiagram("main_sys", "para")

    # Create constant source
    const = sources.Constant(main_sys)
    const_1 = sources.Constant(main_sys)
    const_2 = sources.Constant(main_sys)

    const.parameters.add(value=1)
    const_1.parameters.add(value=3.1415)
    const_2.parameters.add(value="np.array([1,2,3])")

    # Normal addition
    adder = math_op.Add(main_sys)
    adder.inputs.add(const, const_1, const_2)
    adder.parameters['comp_signs'] = ['+', '-', '+']

    # Dimensional addition
    adder_1 = math_op.Add(main_sys)
    adder_1.inputs.add(const)
    adder_1.parameters.add(comp_signs=['+'])

    # Dimensional addition with dimension
    adder_2 = math_op.Add(main_sys)
    adder_2.inputs.add(const)
    adder_2.parameters.add(comp_signs=['+'], dimension=0)

    # Dimensional addition with dimension and dtype
    adder_3 = math_op.Add(main_sys)
    adder_3.inputs.add(const_1)
    adder_3.parameters.add(comp_signs=['+'], dimension=1, dtype="float64")

    # Dimensional addition with dimension and dtype
    adder_4 = math_op.Add(main_sys)
    adder_4.inputs.add(const)
    adder_4.parameters.add(comp_signs=['-'], dimension=1, dtype="float64")

    # # Add component errors
    # adder_err = math_op.Add(main_sys)
    # adder_err.inputs.add(const)
    #
    # # Will raise a TypeError when built since comp_signs needs to be a sequence
    # adder_err.parameters.add(comp_signs=2)
    #
    # # Will raise an AttributeError when built since len(inputs) =/= len(comp_signs)
    # adder_err.parameters.update(comp_signs=[])
    #
    # # Will raise a TypeError when built since all the elements in comp_signs must be either '+' or '-'
    # adder_err.parameters.update(comp_signs=[2])
    #
    # adder_err.parameters.update(comp_signs=['+'])  # Fixes the errors above
    #
    # # Will raise a TypeError when built since the dimension parameter must be a non-negative integer (or None)
    # adder_err.parameters.add(dimension="k")
    #
    # adder_err.parameters.add(dimension=None)  # Fixes the error above
    #
    # # Will raise a TypeError when built since dtype must be a string or None
    # adder_err.parameters.add(dtype=3)
    #
    # adder_err.parameters.update(dtype="int32")  # Fixes the error above
    #
    # # Will raise an AttributeError when built since no input is present in the component
    # adder_err.parameters.update(comp_signs=[])  # Update comp_signs parameter with empty list, so len(comp_signs) = 0
    # del adder_err.inputs["input_1"]  # Delete the input const to produce the error

    main_sys.build_diagram()

