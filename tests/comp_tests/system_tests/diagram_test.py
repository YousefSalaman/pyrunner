import pyrunner.components as comps


class TestSystem(comps.systems.BaseSubsystem):

    default_name = comps.generate_default_name("test")

    direct_feedthrough = comps.generate_direct_feedthrough(False)

    prop_info = comps.generate_prop_info(
        {
            "inputs": None,
            "outputs": None,
            "parameters": None
        }
    )

    def _create_components(self):
        pass


# BlockDiagram test objects

MAIN_SYS = comps.systems.BlockDiagram("main_sys", "seq")
MAIN_SYS_1 = comps.systems.BlockDiagram("main_sys", "seq")


# Test BlockDiagram component

def test_block_diagram():

    _test_block_diagram_clear_diagram()
    _test_block_diagram_remove_component()
    _test_block_diagram_register_component_name()
    _test_block_diagram_unregister_component_name()


def _test_block_diagram_clear_diagram():

    # Sum components for test
    const = comps.sources.Constant(MAIN_SYS_1)
    const.parameters.add(value=0)

    const_1 = comps.sources.Constant(MAIN_SYS_1)
    const_1.parameters.add(value=1)

    adder = comps.math_op.Sum(MAIN_SYS_1)
    adder.inputs.add(const, const_1)
    adder.parameters.add(comp_signs=['+', '-'])

    print(adder.inputs)  # Should be {'input_1': const, 'input_2': const_1}

    # This will remove every component from the list in the BlockDiagram object and it will remove each component from
    # any input or run that references it

    print(MAIN_SYS_1.comps)  # Should be this [const, const_1, add]
    print(MAIN_SYS_1._name_mgr._registry)  # Should be this {'main_sys': 1, 'const': 2, 'add': 1}
    MAIN_SYS_1.clear_diagram()
    print(MAIN_SYS_1.comps)  # Should be []
    print(MAIN_SYS_1._name_mgr._registry)  # Should be this {'main_sys': 1}
    print(adder.inputs)  # Should be {}


def _test_block_diagram_remove_component():

    # Sum components for test
    const = comps.sources.Constant(MAIN_SYS_1)
    const_1 = comps.sources.Constant(MAIN_SYS_1)

    adder = comps.math_op.Sum(MAIN_SYS_1)
    adder.inputs.add(const, const_1)

    print(adder.inputs)  # Should be {'input_1': const, 'input_2': const_1}

    # This will remove the specified component from the list in the BlockDiagram object and it will remove the component
    # from any input or run that references it

    print(MAIN_SYS_1.comps)  # Should be this [const, const_1, add]
    print(MAIN_SYS_1._name_mgr._registry)  # Should be this {'main_sys': 1, 'const': 2, 'add': 1}
    MAIN_SYS_1.remove_components(const_1)
    print(MAIN_SYS_1.comps)  # Should be [const, add]
    print(MAIN_SYS_1._name_mgr._registry)  # Should be this {'main_sys': 1, 'const': 1, 'add': 1}
    print(adder.inputs)  # Should be {'input_1': const}

    MAIN_SYS_1.clear_diagram()  # Clear for other tests


def _test_block_diagram_register_component_name():

    # Everytime a component is created and you specify a system object, the system object will call the BlockDiagram
    # object to register a name in its name manager. Note the system object could be the BlockDiagram itself, so in that
    # case it will just directly call its name manager to register the name

    # When no name is specified, the name will be generated

    const = comps.sources.Constant(MAIN_SYS_1)  # Will be registered as "const"
    const_1 = comps.sources.Constant(MAIN_SYS_1)  # Will be registered as "const_1"

    print(const, const_1)  # This should be "const const_1"

    # If a custom name is given, then that name is registered as is

    const_2 = comps.sources.Constant(MAIN_SYS_1, "const_42")  # Will be registered as "const_42"

    print(const_2)  # This should be "const_42"

    # If a custom name is given and the name was already generated, then the name will be registered but every component
    # that was generated using the same base name and has a higher index number will be shifted to the right, so in this
    # case, const_1 will have the name "const_2", but const will still have its original name since it has a lower
    # index number

    const_3 = comps.sources.Constant(MAIN_SYS_1, "const_1")  # Will be registered as "const_1"

    print(const, const_1, const_2, const_3)  # This should be "const, const_2, const_42, const_1"

    MAIN_SYS_1.clear_diagram()  # Clear diagram for test


def _test_block_diagram_unregister_component_name():

    const = comps.sources.Constant(MAIN_SYS_1)  # Will be registered as "const"
    const_1 = comps.sources.Constant(MAIN_SYS_1)  # Will be registered as "const_1"
    const_2 = comps.sources.Constant(MAIN_SYS_1)  # Will be registered as "const_2"
    const_3 = comps.sources.Constant(MAIN_SYS_1)  # Will be registered as "const_3"

    print(const, const_1, const_2, const_3)  # This should be "const, const_1, const_2, const_3"

    # When removing a component, it will unregister its name. It will verify the amount of times the base name "const"
    # has been registered and it will use the index number (in this case 1) to shift the subsequent names to the left
    # to fill in the gap of the missing registered name. That is, const_2 and const_3 will be named "const_1" and
    # "const_2", respectively.

    MAIN_SYS_1.remove_components(const_1)  # It will unregister "const_1"

    print(const, const_2, const_3)  # This should be "const, const_1, const_2"


# Test _NameManager class

def test_name_manager():

    _test_name_manager_registering()
    _test_name_manager_unregistering()
    _test_name_manager_name_generation()  # TODO: This one is probably outdated since this is done in the components
    _test_name_manager_component_name_registration_status()
    _test_name_manager_get_name_count()
    _test_name_manager_get_name_attrs()


def _test_name_manager_registering():

    MAIN_SYS._name_mgr.register_custom_name("const_1")  # This registers the custom name

    print(MAIN_SYS._name_mgr._registry)  # This should result in {'main_sys': 1, 'const_1': 1}

    # By creating these objects, MAIN_SYS will be registering the object
    # Since no name is provided, MAIN_SYS will tell the name manager to generate a name

    const = comps.sources.Constant(MAIN_SYS)  # Generated name is "const"
    const_1 = comps.sources.Constant(MAIN_SYS)  # Generated name is "const_2"

    # Because "const_1" was registered, the name manager will unregister "const_1" and count the registered name
    # as one of the generated names (since it matches the name generation format for that component). The code will
    # then proceed to generate the next available name, which would be "const_2" for the component const_1

    print(const)  # Should be "const"
    print(const_1)  # Should be "const_2"

    print(MAIN_SYS._name_mgr._registry)  # This should result in {'main_sys': 1, 'const': 3}

    # Expected registration errors

    # If a custom name is entered and that name was already explicitly registered, then the code will raise an error
    # MAIN_SYS._name_mgr.register_custom_name("const_1")


def _test_name_manager_unregistering():

    # Unregistering a name means decreasing the internal component count in the name registry. A component's default
    # name is deleted only when the count reaches 1.

    print(MAIN_SYS._name_mgr._registry)  # This should result in {'main_sys': 1, 'const': 3}

    MAIN_SYS._name_mgr.unregister_name("const_2")
    MAIN_SYS._name_mgr.unregister_name("const")

    print(MAIN_SYS._name_mgr._registry)  # This should result in {'main_sys': 1, 'const': 1}

    # The line below won't unregister anything because the count in the name registry is lower than the name index
    # in the name "const_2", which would be 2 in this case and this would indicate that this number is not registered
    # This should seem weird since I only unregistered "const" and not "const_2", but this object also relies on the
    # fact that the BlockDiagram object will shift the names accordingly, so in this case, when the names are shifted
    # the component that was named "const_2" will change its name to "const".
    MAIN_SYS._name_mgr.unregister_name("const_1")

    print(MAIN_SYS._name_mgr._registry)  # This should result in {'main_sys': 1, 'const': 1}

    MAIN_SYS._name_mgr.unregister_name("const")  # Unregister const completely from the name registry

    print(MAIN_SYS._name_mgr._registry)  # This should result in {'main_sys': 1}

    # Expected unregistration errors

    # MAIN_SYS._name_mgr.unregister_name("const")  # Results in NameError since name is not registered anymore


def _test_name_manager_name_generation():

    # Components directly on the BlockDiagram object will only use their default name to generate a new name

    main_const = comps.sources.Constant(MAIN_SYS)
    main_const_1 = comps.sources.Constant(MAIN_SYS)

    print(main_const)  # Should be "const" since that's the component's default name
    print(main_const_1)  # Should be "const_1" since the component's default name was registered once

    test_sys = TestSystem(MAIN_SYS)
    test_sys_1 = TestSystem(MAIN_SYS)

    print(test_sys)  # Should be "test"
    print(test_sys_1)  # Should be "test_1"

    # The rest of the components are within subsystems, so these components will use the name of the subsystem they're
    # contained plus their default name to generate the new name, aside from this it should follow the same pattern as
    # code above this segment

    test_const = comps.sources.Constant(test_sys)
    test_const_1 = comps.sources.Constant(test_sys)

    print(test_const)  # Should be "test_const"
    print(test_const_1)  # Should be "test_const_1"

    test_1_const = comps.sources.Constant(test_sys_1)
    test_1_const_1 = comps.sources.Constant(test_sys_1)

    print(test_1_const)  # Should be "test_1_const"
    print(test_1_const_1)  # Should be "test_1_const_1"

    # The only exception to the "system name" + "component default name" rule is a subsystem within another subsystem.
    # The code will just generate the inner subsystem's name only using its default name. This is done to avoid verbose
    # generated names

    test_sys_2 = TestSystem(test_sys)
    test_sys_3 = TestSystem(test_sys_1)

    print(test_sys_2)  # Should be "test_2"
    print(test_sys_3)  # Should be "test_3"

    print(main_const, main_const_1)  # This should be "const const_1"
    main_const_2 = comps.sources.Constant(MAIN_SYS)
    main_const_3 = comps.sources.Constant(MAIN_SYS, "const_1")
    print(main_const, main_const_1, main_const_2, main_const_3)  # This should be "const const_2 const_3 const_1"

    MAIN_SYS.remove_components(main_const)
    print(main_const_1, main_const_2, main_const_3)  # This should be "const_1 const_2 const"

    MAIN_SYS.remove_components(main_const_1)
    print(main_const_2, main_const_3)  # This should be "const_1 const"


def _test_name_manager_component_name_registration_status():

    # The method shown here just verifies if the name is in the registry or not

    # Should be True since it is currently registered
    print(MAIN_SYS._name_mgr.is_name_registered('const'))

    # Should be True since it is registered implicitly through the name registry internal counter. Internally, the
    # system will store the base name "const" and count how many times it has been used to register the name
    print(MAIN_SYS._name_mgr.is_name_registered('const_1'))

    # Should be True since it was just registered
    MAIN_SYS._name_mgr.register_custom_name("const_777")  # Register name
    print(MAIN_SYS._name_mgr.is_name_registered('const_777'))

    # Should be False since it hasn't been registered
    print(MAIN_SYS._name_mgr.is_name_registered('const_42'))


def _test_name_manager_get_name_count():

    # The method presented here gets how many times the name and if the name is not registered in the name manager. If
    # the name is not found, it will check if the base name of the component is in the name manager.

    print(MAIN_SYS._name_mgr.get_name_count('const'))

    # Will be the same as the above since it will look for the name "const_1" and won't find it
    print(MAIN_SYS._name_mgr.get_name_count('const_1'))


def _test_name_manager_get_name_attrs():

    # The method presented will extract the "base name" and an index from a given name or component. It checks if the
    # given name has the format regex format ([a-z][A-Z][0-9])*(_[1-9][0-9]*)+$. Examples of names that match this
    # format are "const_1" and "test_3_const_42". The code doesn't check for the section ([a-z][A-Z][0-9])*. It will
    # try to extract the part (_[1-9][0-9]*)+$, which results in "_1" and "_42" for our examples. If it fails to do so,
    # then the name is unique and it doesn't match the name generation format which is the original regex format I
    # showed. It will just return the name as it was given.

    print(MAIN_SYS._name_mgr.get_name_attrs("const"))  # Will return ("const", 0)
    print(MAIN_SYS._name_mgr.get_name_attrs("const_1"))  # Will return ("const_1", 1)
    print(MAIN_SYS._name_mgr.get_name_attrs("test_3_const_42"))  # Will return ("test_3_const", 42)
