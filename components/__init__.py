"""
This package contains all the components of the Simupynk system.
"""

import re
from numbers import Number
from abc import abstractmethod
from Simupynk.utils.cls_prop import classproperty
from Simupynk.utils.type_abc import CPEnabledTypeABC, abstractclassproperty

__all__ = []


class BaseComponent(CPEnabledTypeABC):
    """
    Base class for component objects.
    """

    def __init__(self, sys_obj, name=None):  # Inputs might not be needed for all components

        self.sys = sys_obj  # System that contains object
        self.name = self._assign_component_name(name)
        self._input = self._init_component_property("input", self.input_info)
        self._output = self._init_component_property("output", self.output_info)
        self._parameter = self._init_component_property("parameter", self.parameter_info)

    def __repr__(self):

        return self.name

    @property
    def inputs(self):  # TODO: Elaborate more on how inputs work
        """Inputs for the component."""

        return self._input

    @property
    def outputs(self):  # TODO: Elaborate more on how outputs work
        """Outputs for the component."""

        return self._output

    @property
    def parameters(self):  # TODO: Elaborate more on how parameters work
        """Parameters used for calculations in the system."""

        return self._parameter

    def verify_component_properties(self):
        """
        Verify if the component's properties follows the component's set of
        rules. By default, it will verify if the component's required
        properties from its inputs, outputs, and parameters were assigned
        values. If you want to add another verification, just override this
        method, use "super" to reference this method and add your verification
        for the component that inherits from this class.
        """

        comp_props = [self._input, self._output, self._parameter]
        prop_infos = [self.input_info, self.output_info, self.parameter_info]

        for comp_prop, prop_info in zip(comp_props, prop_infos):
            if prop_info is not None:
                self._verify_required_component_properties(comp_prop, prop_info)

    def _assign_component_name(self, name):

        if self.sys is None:  # This means this component is a main system
            return name
        self.name = name  # Temporarily assign name (it can be None in some cases)
        return self.sys.register_component_name_in_system(self)  # This will output the actual name for the component

    @staticmethod
    def _init_component_property(prop_type, prop_info):

        if prop_info is None:
            return _ComponentPropertyDict({}, prop_type, prop_info)
        return _ComponentPropertyDict({prop_name: None for prop_name in prop_info[1]}, prop_type, prop_info)

    def _verify_required_component_properties(self, comp_prop, prop_info):

        req_props = prop_info[0]
        for req_prop in req_props:
            if comp_prop[req_prop] is None:
                raise TypeError(f'"{req_prop}" was not overwritten for component the component "{self}"')

    @abstractclassproperty
    def default_name(self):
        """
        Default name for a component type. It's used in the creation of its
        name if one wasn't given.
        """

    @abstractclassproperty
    def has_init_cond(self):
        """States whether or not a component has initial conditions."""

    @abstractclassproperty
    def input_info(self):
        """
        A 2-tuple (or NoneType) that indicates a component's required inputs
        and all its available inputs.
        """

    @abstractclassproperty
    def output_info(self):
        """
        A 2-tuple (or NoneType) that indicates a component's required outputs
        and all its available outputs.
        """

    @abstractclassproperty
    def parameter_info(self):
        """
        A 2-tuple (or NoneType) that indicates a component's required
        parameters and all its available parameters.
        """

    @abstractmethod
    def generate_component_string(self) -> str:
        """
        This generates the functionality of the component within a string.
        """


class _ComponentPropertyDict(dict):
    """
    This class is used to store and map component properties such as the
    inputs, outputs, and parameters (for calculations.)

    These properties are classified as follows:

    [1] Order-invariant:
        These properties either have one element or a variable amount of
        components. This is marked by putting "None" in the respective property
        in the component's class.

    [2] Order-dependent:
        These properties have an explicit finite amount of elements in the
        system. This is marked by putting a 2-tuple with elements, which are
        containers, that indicate the required elements and all the elements,
        respectively.

    It sets the following rules on these properties:

    [1] A component property can only store numeric values or component
        objects.

    [2] Order dependent systems can only assign values to the keys determined
        by the class.

    [3] Order invariant systems can only assign values to keys that match the
        regex "{prop_type}_[0-9]+", where prop_type is input, output, or
        parameter.

    [4] Order invariant systems generate keys by using the update method,
        which means you should use this method to add new property entries. To
        change the value of the property, you can use the generated key to
        access and modify the value or use the update method.
    """

    def __init__(self, new_dict, prop_type, prop_info):

        self.prop_type = prop_type  # Property name
        self._determine_property_order_invariance(prop_info)

        super().__init__(new_dict)

    def __setitem__(self, key, value):

        # Checks correct value types
        if not isinstance(value, (BaseComponent, Number)):
            raise TypeError("The value you entered is neither a component nor an integer")

        # This checks/matches if the key was generated (at least try) by this
        # class
        if self.is_order_invariant and not re.match(self.prop_type + "_[0-9]+", key):
            raise KeyError(
                "Custom keys cannot be entered for order-invariant systems. Use the update method to register"
                + " components or numbers.")

        # This check if the key is part of the set properties of the component
        if not (self.is_order_invariant or key in self):
            prop_names = list(self.keys())
            raise KeyError(f"{key} is not among these properties: {prop_names}")

        super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        """
        For positional arguments (order-invariant components), the key is
        generated by the class. For named key arguments (order-variant
        components), the key is verified to see if it's one of the properties
        declared by the component. Both these are used to correctly map and
        name the variables in the generated code.
        """

        if self.is_order_invariant:
            for value in args:
                self.count += 1
                self[self.prop_type + f"_{self.count}"] = value

        for key, value in kwargs.items():  # TODO: Check if dict is necessary for this
            self[key] = value

    def _determine_property_order_invariance(self, prop_info):

        if prop_info is None:
            self.count = 0
            self.is_order_invariant = True
        else:
            self.is_order_invariant = False


# Useful functions, and variables that can used for components building

def _constant_classproperty_helper_factory(name, types):
    """
    Function factory that generates helper functions for creating a constant
    classproperty for a given class attribute.
    """

    doc = BaseComponent.__dict__[name].__doc__

    def generate_constant_class_attribute_helper(value) -> classproperty:
        """Constant classproperty generator for a given attribute"""

        if not isinstance(value, types):
            raise TypeError(f'The value for "{name}" must be one of these types: {types}')
        return classproperty.constant_classproperty(name, value, doc)

    return generate_constant_class_attribute_helper


# Attribute factories
# These functions will generate the corresponding attribute (while ensuring it has the correct type for the attribute)

generate_default_name = _constant_classproperty_helper_factory("default_name", str)
generate_input_info = _constant_classproperty_helper_factory("input_info", (tuple, type(None)))
generate_output_info = _constant_classproperty_helper_factory("output_info", (tuple, type(None)))
generate_parameter_info = _constant_classproperty_helper_factory("parameter_info", (tuple, type(None)))
generate_has_init_cond = _constant_classproperty_helper_factory("has_init_cond", bool)
