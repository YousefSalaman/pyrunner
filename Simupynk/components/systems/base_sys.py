
__all__ = ["BaseSystem",
           "BaseSubsystem"]

from ...runners import *  # Do not remove
from ..base_comp import BaseComponent
from ...utils.type_abc import abstractclassproperty


class BaseSystem(BaseComponent):
    """
    A base class for system component objects.

    The attribute diagram must be defined in the
    child classes that inherit from this class before calling this class' init method through super.
    """

    def __init__(self, sys_obj=None, name=None, **parameters):

        self.sys_comps = []  # Dictionary with components within the system along with their inputs
        self.builder = eval(f'{self.diagram.runner_name}_runner.Builder()')  # Define a builder object for the system

        super().__init__(sys_obj, name, **parameters)

    @abstractclassproperty
    def default_name(self):
        pass

    @abstractclassproperty
    def direct_feedthrough(self):
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

    def pass_default_parameters(self):

        super().pass_default_parameters()
        for comp in self.sys_comps:
            comp.pass_default_parameters()

    def generate_component_string(self):

        for comp in self.sys_comps:
            comp.generate_component_string()

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

    def search_component_name(self, name):

        comp_with_name = []  # List of components that contain name in their name
        for comp in self.sys_comps:
            if name in comp.name:
                comp_with_name.append(comp)
            if isinstance(comp, BaseSystem):
                comp_with_name.extend(comp.search_component_name(name))  # Get components from subsystems
        return set(comp_with_name)

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

    def _unregister_system_components(self):

        for comp in self.sys_comps:
            if isinstance(comp, BaseSystem):
                comp._unregister_system_components()
            self.diagram.unregister_component_name_in_diagram(comp)

    def _remove_component(self, comp):

        for sys_comp in self.sys_comps:
            self._remove_component_from_component_properties(comp, sys_comp)
            if isinstance(sys_comp, BaseSystem):
                sys_comp._remove_component(comp)

        if comp in self.sys_comps:
            self.sys_comps.remove(comp)

    def _remove_component_from_component_properties(self, comp, sys_comp):

        for prop in (sys_comp.inputs, sys_comp.outputs):
            for key, value in prop.copy().items():
                if value == comp:
                    if getattr(self, prop.prop_name + "_info") is None:  # If component property is order-dependent
                        del prop[key]
                    else:  # If component property is order-invariant
                        prop[key] = None


class BaseSubsystem(BaseSystem):
    """
    This is the base class for subsystem components (systems within a block diagram.)
    """

    def __init__(self, sys_obj, name=None, **parameters):

        self.diagram = sys_obj.diagram  # Pass reference to diagram to current system
        if not isinstance(sys_obj, BaseSystem):
            raise TypeError("The parameter sys_obj needs to be a block diagram or subsystem")

        super().__init__(sys_obj, name, **parameters)

    @abstractclassproperty
    def default_name(self):
        pass

    @abstractclassproperty
    def direct_feedthrough(self):
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
