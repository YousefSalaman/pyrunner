from pyrunner.pyrunner.components import *


# Global test components definitions and set-ups

MAIN_SYS = systems.BlockDiagram("main_sys", "seq")

# Create constant source
const = sources.Constant(MAIN_SYS)
const_1 = sources.Constant(MAIN_SYS)
const_2 = sources.Constant(MAIN_SYS)

const.parameters.add(value=1)
const_1.parameters.add(value=3.1415)
const_2.parameters.add(value="np.array([1,2,3])")


# Test functions

def test_normal_addition():

    adder = math_op.Sum(MAIN_SYS, comp_signs="+-+")
    adder.inputs.add(const, const_1, const_2)

    MAIN_SYS.build()  # Build code to generate the strings

    print(adder.code_str["Execution"])  # Should be "add = const-const_1+const_2"

    MAIN_SYS.remove_components(adder)  # Tear down test components


def test_dimension_addition():

    adder_1 = math_op.Sum(MAIN_SYS)
    adder_2 = math_op.Sum(MAIN_SYS)
    adder_3 = math_op.Sum(MAIN_SYS)
    adder_4 = math_op.Sum(MAIN_SYS)

    # Dimensional addition
    adder_1.inputs.add(const)
    adder_1.parameters.add(comp_signs="+")

    # Dimensional addition with dimension
    adder_2.inputs.add(const)
    adder_2.parameters.add(comp_signs="+", dimension=0)

    # Dimensional addition with dimension and dtype
    adder_3.inputs.add(const_1)
    adder_3.parameters.add(comp_signs="+", dimension=1, dtype="float64")

    # Dimensional substraction with dimension and dtype
    adder_4.inputs.add(const)
    adder_4.parameters.add(comp_signs="+", dimension=1, dtype="float64")

    MAIN_SYS.build()  # Build diagram to generate the strings

    print(adder_1.code_str['Execution'])  # Should be "add = np.sum(const)"
    print(adder_2.code_str['Execution'])  # Should be "add_1 = np.sum(const,axis=0)"
    print(adder_3.code_str['Execution'])  # Should be "add_2 = np.sum(const_1,axis=1,dtype=np.float64)"
    print(adder_4.code_str['Execution'])  # Should be "add_3 = -np.sum(const,axis=1,dtype=np.float64)"

    MAIN_SYS.remove_components(adder_1, adder_2, adder_3, adder_4)  # Tear down test components


def test_addition_errors():

    adder_err = math_op.Sum(MAIN_SYS)
    adder_err.inputs.add(const)

    # Sum component errors

    # Will raise a TypeError when built since comp_signs needs to be a sequence
    adder_err.parameters.add(comp_signs=2)
    MAIN_SYS.build()

    # Will raise an AttributeError when built since len(inputs) =/= len(comp_signs)
    adder_err.parameters.update(comp_signs=[])
    MAIN_SYS.build()

    # Will raise a TypeError when built since all the elements in comp_signs must be either '+' or '-'
    adder_err.parameters.update(comp_signs=[2])
    MAIN_SYS.build()

    adder_err.parameters.update(comp_signs='+')  # Fixes the errors above

    # Will raise a TypeError when built since the dimension parameter must be a non-negative integer (or None)
    adder_err.parameters.add(dimension="k")
    MAIN_SYS.build()

    adder_err.parameters.add(dimension=None)  # Fixes the error above

    # Will raise a TypeError when built since dtype must be a string or None
    adder_err.parameters.add(dtype=3)
    MAIN_SYS.build()

    adder_err.parameters.update(dtype="int32")  # Fixes the error above

    # Will raise an AttributeError when built since no input is present in the component
    adder_err.parameters.update(comp_signs=[])  # Update comp_signs parameter with empty list, so len(comp_signs) = 0
    del adder_err.inputs["input_1"]  # Delete the input const to produce the error
    MAIN_SYS.build()
