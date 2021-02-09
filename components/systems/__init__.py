"""
Placeholder
"""

import abc
from Simupynk.runners import *
from Simupynk.components import BaseComponent
from Simupynk.runners import available_runners
from Simupynk.utils.type_abc import abstractclassproperty


class BaseSystem(BaseComponent):
    """
    A base class for system component objects.
    """

    _main_systems = []

    def __init__(self, sys_obj=None, runner_name=None, name=None):

        self.sys_comps = []  # Dictionary with components within the system along with their inputs
        if sys_obj is None:
            self._init_main_system(name, runner_name)
        else:
            self._init_inner_system(sys_obj, runner_name)

        self.builder = eval(f'{self.main_sys.runner_name}_runner.Builder()')  # Define a builder object for the system

        super().__init__(sys_obj, name)

    def build_system(self):
        """
        This method will do the following:

        [1] Verify the properties for each component in the system follows the
            criteria established by each component, respectively.

        [2] It will determine in what order the system will execute each
            component

        [3] It will generate the code string for the system.
        """

        if self is not self.main_sys:
            raise TypeError(f'"{self}" cannot be built since it is not a "main" system')
        self.verify_system_component_properties()
        self.organize_system()
        self.generate_component_string()

    @classmethod
    def build_systems(cls):
        """
        For multiple main systems that share the same system class, you can use
        this method to build all of them.
        """

        for main_sys in cls._main_systems:
            main_sys.build_system()

    def generate_component_string(self):
        pass

    def organize_system(self) -> None:
        """
        This method defines the variables to traverse and build the system
        appropriately. It references the build_system_order of the system's
        builder.
        """

        sys_trail = []  # Store components in trail to detect if the system is cyclic (has a feedback loop)
        self.builder.define_sys_info(self.sys_comps)

        for comp in self.sys_comps:
            if comp.is_not_mapped:
                self.builder.build_system_order(comp, sys_trail)  # Build system order
                if isinstance(comp, BaseSystem):
                    comp.organize_system()

    def verify_system_component_properties(self):
        """
        This method will go through all the components within the system and
        verify if their properties satisfy the criteria established by its
        respective component class.
        """

        for comp in self.sys_comps:
            comp.verify_component_properties()
            if isinstance(comp, BaseSystem):  # If component is a also system, verify its attributes
                comp.verify_system_component_properties()

    def register_component_name_in_system(self, comp):
        """
        This method will register a components name into the main system's
        Name Manager (namespace). When registering a name, the system will do
        one of two things:

        [1] If a name was entered, the system will check if was not entered
            before. In the case the same name was entered, the system will
            raise an error indicating this.

        [2] If a name was not entered, the name manager will generate a name
            for the system.
        """

        if comp.name is None:
            return self.main_sys.name_mgr.generate_component_name(comp)
        return self.main_sys.name_mgr.verify_custom_component_name(comp.name)

    def _init_main_system(self, name, runner_name):

        self._main_systems.append(self)  # Register main system in class

        self.main_sys = self  # State that you're the main system to your inner system components
        self.name_mgr = _NameManager()  # A "namespace" to register components

        self._verify_runner_type(runner_name)
        self.runner_name = runner_name

        if name is None:
            raise NameError('A "main" system must have a name')
        self.name_mgr.verify_custom_component_name(name)  # Register main system name in its own namespace

    def _init_inner_system(self, sys_obj, runner_name):

        self.main_sys = sys_obj.main_sys  # Pass reference to main system to current system
        if not (self.main_sys is self or runner_name is None):
            raise AttributeError("Only the main system can define the runner name")

    @staticmethod
    def _verify_runner_type(runner_name):

        if runner_name is None:
            raise NameError('A "main" system must specify a runner name')
        if not isinstance(runner_name, str):
            raise TypeError('The argument "runner_name" has to be a string')
        if runner_name not in available_runners:
            raise ModuleNotFoundError(f'A runner with the name "{runner_name}" was not found. ' +
                                      f'The available runner names are {", ".join(available_runners)}.')

    @abstractclassproperty
    def default_name(self):
        pass

    @abstractclassproperty
    def has_init_cond(self):
        pass

    @abstractclassproperty
    def input_info(self):
        pass

    @abstractclassproperty
    def output_info(self):
        pass

    @abstractclassproperty
    def parameter_info(self):
        pass


class _NameManager:
    """
    This is the name manager for system components. It keep tracks of the
    variables registered in the system. The information kept within the name
    registry in a NameManager object is used to ensure components are given
    unique names to correctly reference variables within calculations.

    The name registry attribute "_sys_var_names" keeps track of how many times
    a variable has been used in a system to make sure repeated generated
    variable names are given a unique name within the system.
    """

    def __init__(self):

        self._sys_var_names = {}  # Name registry for a system

    def generate_component_name(self, comp_obj):
        """
        Generate a name for a component if one wasn't assigned to it. The name
        is generated by using the default name of the component, it's container
        system and the amount of times this combination of names has been
        registered in the system's name manager.
        """

        comp_obj_sys = comp_obj.sys  # Component's system container
        main_sys = comp_obj_sys.main_sys  # System that contains all components
        comp_is_a_system = hasattr(comp_obj, "sys_comps")

        comp_name = comp_obj.default_name
        if not (comp_obj_sys is main_sys or comp_is_a_system):
            comp_name += "_" + comp_obj_sys.name
        return self._register_component_name(comp_name)

    def verify_custom_component_name(self, comp_name):
        """
        This will verify if the custom component name was registered in the
        name manager. If it was registered, it will produce a NameError
        indicating this.
        """

        if comp_name in self._sys_var_names:
            raise NameError(f'The name "{comp_name}" was registered more than once.')
        return self._register_component_name(comp_name)

    def _register_component_name(self, comp_name):

        if comp_name in self._sys_var_names:  # Update name registry
            new_comp_name = comp_name + "_" + str(self._sys_var_names[comp_name])
            self._sys_var_names[comp_name] += 1
            return new_comp_name

        # Register name
        self._sys_var_names[comp_name] = 1
        return comp_name
