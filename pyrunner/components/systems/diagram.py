
import re
import os
import importlib
from glob import glob
from functools import wraps

from ..base_comp import *
from .base_sys import BaseSystem
# from ...runners import available_runners


# BlockDiagram definition and helpers


def _shift_component_names_helper(func):
    """
    Decorator that helps with name shifting.

    It provides the shift methods in the BlockDiagram class with
    the following:

    - comp_base_name: The component's base name to search for
      components with similar names and use that to rename the
      components that share the same name, if indicated by
      the wrapped method.

    - comp_name_index: The number of the component in the name
      manager object. This is used as a criteria to shift certain
      names only.

    - similar_comp: A component that shares a similar name to the
      original component. The decorator will only pass the
      components that have the same base name as the original
      component to the shift method.

    - similar_comp_name_index: The number of the component that
      shares a similar name to the original component.
    """

    @wraps(func)
    def method_wrapper(diagram, comp):

        comp_base_name, comp_name_index = _NameManager.get_component_base_name_attributes(comp)

        base_name_count = diagram._name_mgr.get_name_count(comp_base_name)  # Gets registered count for the base name
        similar_name_comps = diagram.search_component_name(comp_base_name)  # List with similar names
        for similar_comp in similar_name_comps:
            _, similar_comp_name_index = _NameManager.get_component_base_name_attributes(similar_comp)
            similar_name_match = similar_comp is not comp \
                                 and base_name_count > similar_comp_name_index \
                                 and re.match(comp_base_name + '(_[1-9][0-9]*)?', similar_comp.name)

            if similar_name_match:
                func(diagram, comp_base_name, comp_name_index, similar_comp, similar_comp_name_index)

    return method_wrapper


# TODO: Change runner name for the actual runner class and use that to create runner objects in the subsystems
class BlockDiagram(BaseSystem):
    """
    A system object that acts as the main container for a set of components.

    Every component, that is not a BlockDiagram component, must be contained
    either directly in one of these or in a subsystem component that is
    contained in the BlockDiagram.

    It functions as "component manager" in the sense that it can manipulate
    the properties of the components contained within it. It does the
    following:

    - It can register or unregister component names.

      It manipulates other component names when it registers names to avoid any
      conflict with the name of the component that is being registered.

      This also happens when unregistering a component name. It manipulates the
      component names so it reflects the count of the names registered with the
      same "base name"

    - It builds the different components.

      It initiates the building phase for components by passing its default
      parameters and generate its component string.

    The BlockDiagram uses the runner _modules to change how it organizes the
    components and construct the system's code. In other words, the runners
    tell the BlockDiagram object how they want the code to organize and
    generate, so they can run the code without any problem.
    """

    _DIAGRAMS = []

    default_name = generate_default_name("")

    direct_feedthrough = generate_direct_feedthrough(False)

    input_info = generate_input_info(None)

    output_info = generate_output_info(None)

    parameter_info = generate_parameter_info(None)

    # Diagram initialization

    def __init__(self, name, runner_name):

        self.diagram = self  # State that you're the block diagram for your subsystems
        self._DIAGRAMS.append(self)  # Register diagram in class
        self.runner_name = runner_name
        self.runner = self._find_runner(runner_name)
        self._name_mgr = _NameManager()  # A "namespace" to register components

        self._verify_runner_type(runner_name)
        self._name_mgr.register_component_name(name)  # Register main system name in its own namespace

        super().__init__(name=name)

    @staticmethod
    def _find_runner(runner_name):

        runners = glob(os.path.join("..", "..", "runners", "*_runner.py"))  # Get runner modules
        print("Test:", glob("*"))
        print("Regex path:", os.path.join("..", "..", "runners", "*_runner.py"))
        print("Path exists?", os.path.exists(os.path.join("..", "..", "..", "runners", "*_runner.py")))
        print(runners)
        for runner in runners:
            if runner_name in runner:
                return importlib.import_module("...runners." + os.path.basename(runner))
        raise ModuleNotFoundError(f"No runner could be found using the name {runner_name}")

    def build_diagram(self):
        """
        Builds up the BlockDiagram object.

        This method will do the following to accomplish this:

        - Verify the properties for each component in the system follows the
          criteria established by each component, respectively.

        - It will determine in what order the system will execute each
          component.

        - Pass the default parameters to its respective components

        - It will generate the code string for the system.
        """

        self.pass_default_parameters()
        self.verify_system_component_properties()
        self.organize_system()
        self.generate_component_string()

    @classmethod
    def build_diagrams(cls):
        """
        For multiple main systems that share the same system class, you can use
        this method to build all of them.
        """

        for diagram in cls._DIAGRAMS:
            diagram.build_diagram()

    def clear_diagram(self):
        """
        This removes all the components from the diagram.

        The method will only remove the items that are directly on the
        BlockDiagram's component list. However, it will unregister every
        component name in the BlockDiagram component.
        """

        for comp in self.sys_comps.copy():
            if isinstance(comp, BaseSystem):
                comp._unregister_system_components()
            self.remove_components(comp)

    def register_component_name_in_diagram(self, comp) -> str:
        """
        This method will register a components name into the BlockDiagram's
        NameManager object. When registering a name, the system will do
        one of two things:

        - If a name was entered, the system will check if was not entered
          before. In the case the same name was entered, the system will
          raise an error indicating this.

        - If a name was not entered, the name manager will generate a name
          for the system.
        """

        if comp.name is None:
            return self._name_mgr.generate_component_name(comp)

        self._name_mgr.register_component_name(comp.name)
        if self._name_mgr.get_name_count(comp.name) > 1:  # Perform right shift if custom name is not unique
            self._shift_component_names_right(comp)
        return comp.name

    def remove_components(self, *comps):
        """
        Remove a collection of components from the system. The
        component(s) can directly be in the BlockDiagram object or
        they can reside in a system component within the BlockDiagram
        object.
        """

        for comp in comps:
            self.unregister_component_name_in_diagram(comp)
            self._remove_component(comp)

    def unregister_component_name_in_diagram(self, comp):
        """
        This will unregister a component from the block diagram's name
        manager. After unregistering the component's name, the code will
        verify if the name was generated by the name register and the
        diagram will shift the component names that were generated
        afterward to the left by renaming the components using the base
        name and name index

        Although this method is public, it should be used with caution
        since this will rename the components that use the same base
        name. Only use this when you compensate for this name change.
        """

        if self._name_mgr.component_name_registered(comp.name):
            self._shift_component_names_left(comp)
            self._name_mgr.unregister_component_name(comp.name)

    @_shift_component_names_helper
    def _shift_component_names_left(self, comp_base_name, comp_name_index, similar_comp, similar_comp_name_index):
        """
        This method shifts the names to the left.

        This is done by renaming the components that are higher
        than the
        the names to the left by renam
        """

        if similar_comp_name_index > comp_name_index:
            if similar_comp_name_index == 1:
                similar_comp.name = comp_base_name
            else:
                similar_comp.name = comp_base_name + '_' + str(similar_comp_name_index - 1)

    @_shift_component_names_helper
    def _shift_component_names_right(self, comp_base_name, comp_name_index, similar_comp, similar_comp_name_index):

        if similar_comp_name_index >= comp_name_index:
            similar_comp.name = comp_base_name + '_' + str(similar_comp_name_index + 1)

    @staticmethod
    def _verify_runner_type(runner_name):

        if runner_name is None:
            raise NameError('A "main" system must specify a runner name. '
                            f'Here is a list of the available runner names: {", ".join(available_runners)}')

        if not isinstance(runner_name, str):
            raise TypeError('The argument "runner_name" has to be a string')

        if runner_name not in available_runners:
            raise ModuleNotFoundError(f'A runner with the name "{runner_name}" was not found. '
                                      f'The available runner names are: {", ".join(available_runners)}.')


# Name manager definition

class _NameManager:
    """
    The variable name manager for BlockDiagram components. It keep tracks of the
    variables registered in the system by registering or unregistering
    them from the name registry that is stored within a NameManager object.
    The information kept within the name registry is used to ensure components
    are given unique names to correctly reference variables within calculations.

    When a component is created, it is registered in the NameManager. There a
    two ways the BlockDiagram object goes about registering names:

    - Generating names: When a name is not specified by the component, the
      NameManager will extract a "base name" for the component by using the
      formula component's system's name + component's default name. From here
      a couple of things can happen:

      - When a base name is not registered in the NameManager, the name will be
        registered explicitly by entering the name directly into the NameManager.

      - For subsequent components with the same "base name", the name will be
        generated by using the component's base nae + current amount of times the
        base name has been registered, the latter being called its "name index".
        Most of the generated names are "implicitly" registered in this manner.
        Implicit registration uses the base name + amount of times its been
        registered to keep track of how many variables with the same base name are
        within a BlockDiagram.

    - Custom names: If a name is specified, the NameManager will register the
      name as it was given. Depending on the format of the name, the variable
      can be explicitly or implicitly registered:

      - If the name is unique, that is, if its base name does not match the base
        name of another component, then it will be registered explicitly.

      - If the custom has the format base name + number higher than the current
        base name count, then the name will be registered explicitly.

      - If the base name count has reached the number in the case above, then
        the custom name will be explicitly unregistered by removing it from
        the name registry and it will be implicitly registered by raising the
        number count.

      - If a custom name is entered and it has the format base name + number
        lower than the current base name count, then the name will be implicitly
        registered.
    """

    def __init__(self):

        self._sys_var_names = {}  # Name registry for a BlockDiagram object

    def component_name_registered(self, comp_name):
        """
        Verify if the component name is registered in the name registry.
        """

        # True for generated names whose name is the base name
        # and custom names that are explicitly in the name
        # registered
        if comp_name in self._sys_var_names:
            return True

        # Check if the name has the generated name format and then verify if the base name is in the registry
        elif re.search("(_[1-9][0-9]*)+$", comp_name):
            _, comp_name_in_name_registry = self._component_base_name_in_registry(comp_name)
            return comp_name_in_name_registry

        return False  # Otherwise, it's not there

    def generate_component_name(self, comp_obj):
        """
        Generate a name for a component if one wasn't assigned to it.

        The name is generated by using the default name of the component, it's
        container system and the amount of times this combination of names has
        been registered in the system's name manager.
        """

        comp_obj_sys = comp_obj.sys  # Component's system container (could be a diagram or subsystem)
        comp_is_not_in_subsystem = isinstance(comp_obj_sys, BlockDiagram)

        comp_name = comp_obj.default_name
        if not (isinstance(comp_obj, BaseSystem) or comp_is_not_in_subsystem):
            comp_name = comp_obj_sys.name + "_" + comp_name
        return self._register_component_name(comp_name)

    def get_name_count(self, comp_name):
        """
        Gets the amount of times a value has been registered.
        """

        if comp_name in self._sys_var_names:
            return self._sys_var_names[comp_name]

        comp_base_name, comp_name_in_name_registry = self._component_base_name_in_registry(comp_name)
        if comp_name_in_name_registry:
            return self._sys_var_names[comp_base_name]

        raise NameError(f'The name "{comp_name}" was not found in the name registry.')

    @staticmethod
    def get_component_base_name_attributes(comp_info):
        """Extracts a component's base name and its name index."""

        if isinstance(comp_info, BaseComponent):
            comp_name = comp_info.name
        else:  # Otherwise, it's a string
            comp_name = comp_info

        try:
            comp_base_name, comp_name_index, _ = re.split("(_[1-9][0-9]*)+$", comp_name)
            comp_name_index = int(comp_name_index.split('_')[1])
        except ValueError:
            comp_name_index = 0
            comp_base_name = comp_name

        return comp_base_name, comp_name_index

    def register_component_name(self, comp_name):
        """
        This will register a custom component name. Two things can happen
        when using this method:

        - If the component has a generated "base name" is registered and its "component
          name index" is less than the registered base name's count, then
          the base name will be registered instead of the input name.

        - Otherwise, the component's name is registered as is.
        """

        # Register component base name if its in registry
        if re.search("(_[1-9][0-9]*)+$", comp_name):
            comp_base_name, comp_name_in_name_registry = self._component_base_name_in_registry(comp_name)
            if comp_name_in_name_registry:
                self._register_component_name(comp_base_name)  # Register the base of the name
                return comp_name

        return self._register_component_name(comp_name)  # Otherwise, register the name as is

    def unregister_component_name(self, comp_name):
        """
        Unregister a component name from the name registry. Three
        things can happen when using this method:

        - If the component's name is found in the name registry,
          then it is unregistered.

        - If the component's base name is found in the name
          registry, then the base name is unregistered instead.

        - Otherwise, it will count as an invalid name entry was
          going to be deleted.
        """

        # It's a custom name or the default name of a component (i.e. its "base name")
        if comp_name in self._sys_var_names:
            self._unregister_component_name(comp_name)

        # It's a generated name or it's a custom name that matches the name generation format
        elif re.search("(_[1-9][0-9]*)+$", comp_name):
            comp_base_name, _ = self.get_component_base_name_attributes(comp_name)
            if comp_base_name in self._sys_var_names:
                self._unregister_component_name(comp_base_name)

        # An invalid name was entered
        else:
            raise NameError(f"Component name {comp_name} was not found in name registry.")

    def _component_base_name_in_registry(self, comp_name):
        """
        Verifies whether or not a component's base name is in the
        system and if it was generated.

        This is True for custom names that match the name generation
        format or a generated name whose base name count in the
        registry is higher than 1. Otherwise, it is False.
        """

        comp_base_name, comp_base_name_index = self.get_component_base_name_attributes(comp_name)
        comp_name_in_name_registry = comp_base_name in self._sys_var_names \
                                     and comp_base_name_index < self._sys_var_names[comp_base_name]

        return comp_base_name, comp_name_in_name_registry

    def _register_component_name(self, comp_name):

        if comp_name in self._sys_var_names:  # Update name registry
            while True:
                new_comp_name = comp_name + "_" + str(self._sys_var_names[comp_name])
                self._sys_var_names[comp_name] += 1
                if new_comp_name in self._sys_var_names:  # There's a name that clashes with the generated name
                    self.unregister_component_name(new_comp_name)  # Unregister the name that clashes
                else:
                    return new_comp_name

        # Register name
        self._sys_var_names[comp_name] = 1
        return comp_name

    def _unregister_component_name(self, comp_name):

        name_cnt = self._sys_var_names[comp_name]  # The amount of times the name has been registered
        if name_cnt == 1:
            del self._sys_var_names[comp_name]
        elif name_cnt > 1:
            self._sys_var_names[comp_name] -= 1
