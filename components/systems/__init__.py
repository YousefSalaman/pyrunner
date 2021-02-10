"""
Placeholder
"""

__all__ = ["main_sys"]

import abc
from Simupynk.runners import *  # Do not remove
from Simupynk.components import BaseComponent
from Simupynk.utils.type_abc import abstractclassproperty


class BaseSystem(BaseComponent):
    """
    A base class for system component objects.

    The attribute main_sys must be defined in the
    child classes that inherit from this class before calling this class' init method through super.
    """

    def __init__(self, sys_obj=None, name=None):

        self.sys_comps = []  # Dictionary with components within the system along with their inputs
        self.builder = eval(f'{self.main_sys.runner_name}_runner.Builder()')  # Define a builder object for the system

        super().__init__(sys_obj, name)

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
                self.builder.build_system_order(comp, sys_trail)
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


class BaseInnerSystem(BaseSystem):
    """
    This is the base class for inner systems (systems within other systems)
    """

    def __init__(self, sys_obj, name=None):

        self.main_sys = sys_obj.main_sys  # Pass reference to main system to current system
        if not isinstance(sys_obj, BaseSystem):
            raise TypeError("The parameter sys_obj needs to be a system")

        super().__init__(sys_obj, name)

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
