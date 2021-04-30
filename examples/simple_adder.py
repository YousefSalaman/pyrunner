
from pyrunner import components as comps


main_sys = comps.systems.BlockDiagram("main_sys", "seq")  # Initialize the BlockDiagram


# Add constant sources
const = comps.sources.Constant(main_sys, value=42)
const_1 = comps.sources.Constant(main_sys, value=3.1415)
const_2 = comps.sources.Constant(main_sys, value='np.array([1,2,3])')
const_3 = comps.sources.Constant(main_sys, value=1)

# Add the Sum blocks
adder = comps.math_op.Sum(main_sys, comp_signs="-+")
adder_1 = comps.math_op.Sum(main_sys, comp_signs='+--')
adder_2 = comps.math_op.Sum(main_sys, comp_signs='-')

# Add the inputs to Sums
adder.inputs.add(adder_1, adder_2)
adder_1.inputs.add(const_1, const_2, const_3)
adder_2.inputs.add(const_2)

main_sys.outputs.add(adder)  # Say the "adder" component is the run

dir_path = 'C:\\Users\\Yousef\\PycharmProjects\\RUMarino\\pyrunner\\examples'
main_sys.build(dir_path, "adder_example")
