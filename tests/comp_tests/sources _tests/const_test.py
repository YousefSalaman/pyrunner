from Simupynk.Simupynk.components import *

if __name__ == "__main__":
    main_sys = systems.BlockDiagram("main_sys", "seq")

    const_1 = sources.Constant(main_sys)
    const_2 = sources.Constant(main_sys)

    # const_1.inputs.add(test=const_2)  # This will produce a KeyError since no inputs can be added
    # const_1.outputs.add(test=const_2)  # This will produce a KeyError since no outputs can be added

    # main_sys.build()  # This will result in a TypeError since "value" in parameters was not assigned a value

    const_1.parameters.add(value=1)
    const_2.parameters.add(value=3.1415)

    main_sys.build()
