__all__ = ["BaseSystem",
           "BaseSubsystem"]

from abc import abstractmethod

from ..base_comp import BaseComponent
from ...utils.cls_prop import abstractclassproperty


class BaseSystem(BaseComponent):
    """Base class for system component objects.

    It contains the methods and attributes that a system object must
    have. The diagram attribute must be defined in the child classes
    that inherit from this class before calling this class' __init__
    method through super.
    """

    def __init__(self, sys_obj, name=None, **parameters):

        self.comps = []  # List with components within the system
        self.diagram = sys_obj.diagram  # Pass reference to diagram to current system
        self.organizer = self.diagram.runner.Organizer()  # Define a organizer object for the system

        super(BaseSystem, self).__init__(sys_obj, name, **parameters)

    @abstractclassproperty
    def default_name(cls):
        pass

    @abstractclassproperty
    def direct_feedthrough(cls):
        pass

    @abstractclassproperty
    def prop_info(cls):
        pass

    def clear(self):
        """Remove all components in the system and its subsystems."""

        for comp in self.comps.copy():
            if comp.is_system():
                comp.clear()
            self.diagram.unregister_component_name(comp)
            self.remove_component(comp)

    def generate_code_string(self):
        """Generate the code string for all the system's components."""

        for comp in self.comps:
            comp.generate_code_string()

    def organize(self):
        """Determine an order of evaluation for the system's components.

        This method uses the diagram's runner's organizer class to find
        in what order it should place the components. If a system has a
        subsystem within it, it will call this method on that component,
        so it can also organize the components within the subsystem.
        """

        self.organizer.define_sys_info(self.comps)
        for comp in self.comps:
            if comp.is_not_mapped:
                self.organizer.build_system_order(comp)
            if comp.is_system():
                comp.organize()

    def search_component_name(self, name):
        """Return a set of components that match the given name."""

        comps_with_name = []  # List of components that contain name in their name
        for comp in self.comps:
            if name in comp.name:
                comps_with_name.append(comp)
            if comp.is_system():  # Get component that match the names from subsystem
                comps_with_name.extend(comp.search_component_name(name))  # Get components from subsystems
        return set(comps_with_name)  # Removes duplicates

    def setup(self):

        for comp in self.comps:
            if comp.is_system():
                comp.setup()
            comp.pass_default_parameters()
            self.diagram.pass_imports(comp.lib_deps)

    def unregister_all_components(self):
        """Unregister all component names in the system from name registry."""

        for comp in self.comps:
            if comp.is_system():
                comp.unregister_all_components()
            self.diagram.unregister_component_name(comp)

    def verify_properties(self):

        super(BaseSystem, self).verify_properties()
        for comp in self.comps:
            comp.verify_properties()

    def register_component_name(self, comp, name):

        return self.diagram.register_component_name(comp, name)

    def remove_component(self, input_comp):
        """Removes component from the system."""

        # Remove component from inputs and outputs from all components within a system
        for comp in self.comps:
            comp.inputs.remove(input_comp)
            comp.outputs.remove(input_comp)
            if comp.is_system():
                comp.remove_component(input_comp)

        # Remove component from system components if present
        if input_comp in self.comps:
            self.comps.remove(input_comp)


class BaseSubsystem(BaseSystem):
    """Base class for systems within a block diagram."""

    def __init__(self, sys_obj, name=None, **parameters):

        super(BaseSubsystem, self).__init__(sys_obj, name, **parameters)

        self._create_components()  # Create the components

    @abstractmethod
    def _create_components(self):
        """Create and connect the components stored in the subsystem.

        When creating these components, one must put the subsystem as
        their system object, so the objects can reside in the subsystem
        instead of the block diagram object. One should specify which
        components are the outputs of the system, so these can be used
        as inputs for components outside of the subsystem.
        """

    @abstractclassproperty
    def default_name(cls):
        pass

    @abstractclassproperty
    def direct_feedthrough(cls):
        pass

    @abstractclassproperty
    def prop_info(cls):
        pass
