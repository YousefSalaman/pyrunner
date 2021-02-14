"""
This module holds the base component class
"""

import re
from numbers import Number
from functools import wraps
from abc import abstractmethod
from collections.abc import Callable, Collection

import numpy as np

from Simupynk.utils.cls_prop import classproperty
from Simupynk.utils.type_abc import CPEnabledTypeABC, abstractclassproperty


class BaseComponent(CPEnabledTypeABC):
    """
    Base class for component objects.
    """

    def __init__(self, sys_obj, name=None):  # Inputs might not be needed for all components

        self._verify_if_component_is_diagram(sys_obj)

        self.sys = sys_obj  # System that contains object
        self.is_not_mapped = True  # Indicates if component has been ordered
        self.name = self._assign_component_name(name)  # Name of the component
        self.code_str = {"Set Up": None, "Execution": None}  # Storage for generated strings
        self._input = self._init_component_property("input", self.input_info, BaseComponent)
        self._output = self._init_component_property("output", self.output_info, BaseComponent)
        self._parameter = self._init_component_property("parameter", self.parameter_info,
                                                        (Number, Callable, Collection, np.generic, np.ndarray))

    def __repr__(self):

        return self.name

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

        prop_names = ["inputs", "outputs", "parameters"]
        prop_infos = [self.input_info, self.output_info, self.parameter_info]

        for prop_name, prop_info in zip(prop_names, prop_infos):
            if prop_info is not None:
                self._verify_required_component_values(prop_name, prop_info)

    def _assign_component_name(self, name):

        if self.sys is None:  # This means this component is a main system
            return name
        self.name = name  # Temporarily assign name (it can be None in some cases)
        return self.sys.register_component_name_in_system(self)  # This will output the actual name for the component

    @staticmethod
    def _init_component_property(prop_name, prop_info, prop_types):

        if prop_info is None:
            return _ComponentProperty({}, prop_name, prop_info, prop_types)
        return _ComponentProperty({prop_name: None for prop_name in prop_info[1]}, prop_name, prop_info, prop_types)

    def _verify_required_component_values(self, prop_name, prop_info):

        req_props = prop_info[0]
        comp_prop = getattr(self, prop_name)
        non_assigned_req_props = [req_prop for req_prop in req_props if comp_prop[req_prop] is None]

        if len(non_assigned_req_props) > 0:
            raise TypeError(f'For component "{self}", the following variables {non_assigned_req_props}'
                            f' in "{prop_name}" were not assigned values."')

    def _verify_if_component_is_diagram(self, sys_obj):

        if sys_obj is None:
            if not hasattr(self, "sys_comps"):
                raise TypeError("Non-system components must reside in a block diagram or subsystem")
        else:
            sys_obj.sys_comps.append(self)  # Add component to system


# ComponentProperty definitions

def _non_erasable_order_dependent_method(func):
    """
    Decorator to disable item deletion for order-dependent component properties.
    """

    @wraps(func)
    def method_wrapper(*args):
        self = args[0]
        if self.is_order_invariant:
            return func(*args)
        raise AttributeError("You cannot erase the items of an order-dependent property.")

    return method_wrapper


def _detect_invalid_key_entry(func):
    """
    Decorator to detect if an invalid key was entered in a method.
    """

    @wraps(func)
    def method_wrapper(*args):

        self = args[0]
        try:
            func(*args)
        except KeyError:
            raise KeyError("Item could not be deleted. You either entered an invalid key "
                           f"or the {self._prop_name}s are empty.")

    return method_wrapper


class _ComponentProperty(dict):
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

    [2] Order-dependent systems can only assign values to the keys determined
        by the class.

    [3] Order-invariant components can only assign values to keys that match the
        regex "{prop_type}_[0-9]+", where prop_type is input, output, or
        parameter.

    [4] Order-invariant components generate keys by using the add method,
        which means you should use this method to add new property entries. To
        change the value of the property, you can use the generated key to
        access and modify the value or use the update method.
    """

    _allowed_prop_types = {}  # Store the allowed property types, so it doesn't have to be associated with an instance

    def __init__(self, new_dict, prop_name, prop_info, prop_types):

        self._prop_name = prop_name  # Property name
        if prop_name not in self._allowed_prop_types:
            self._allowed_prop_types[prop_name] = prop_types

        self._determine_property_order_invariance(prop_info)

        super().__init__(new_dict)

    def __setitem__(self, key, value):

        # Check if key is a string
        if not isinstance(key, str):
            raise TypeError("The key/variable of a component property must be a string.")

        # Checks correct value types
        prop_types = self._allowed_prop_types[self._prop_name]
        if not isinstance(value, prop_types):
            try:
                prop_type_names = [prop_type.__name__ for prop_type in prop_types]
            except TypeError:
                prop_type_names = [prop_types.__name__]
            raise TypeError(f'The value "{value}" must be an instance of one '
                            f'of these classes: {", ".join(prop_type_names)}')

        # This checks if the key was generated by this class by verifying
        # if it matches the generated format and if its property number is
        # among the generated ones
        if self.is_order_invariant \
                and \
                not (re.match(self._prop_name + "_[1-9][0-9]*", key)  # Check if key has the class' generated key format
                     and int(key.rsplit('_', maxsplit=1)[
                                 1]) <= self._key_gen_count):  # Check if property number is among the generated ones

            raise KeyError("Custom keys cannot be entered for order-invariant systems. "
                           "Use the add method to register values.")

        # This checks if the key is part of the set properties of the component
        if not (self.is_order_invariant or key in self):
            if len(self) == 0:
                raise KeyError(f"No entries are allowed for the component's {self._prop_name}s.")
            raise KeyError(f'The variable "{key}" is not among these variables: {", ".join(self.keys())}.')

        super().__setitem__(key, value)

    @_non_erasable_order_dependent_method
    def __delitem__(self, key):
        """
        The item deletion dunder method.

        For this class, this method was modified, so when an item is deleted
        for an order-invariant component, the other the subsequent existent
        items are "shifted" to the left.

        That is, suppose we have a property with n variables named "prop_name".
        If for some i such that i < n, its respective key-value pair,
        (prop_name i, value i), is deleted, then the following happens:

        Original property:

        key_gen_count = n + 1
        {(prop_name 1, value 1), ..., (prop_name i, value i), ..., (prop_name n, value n)}

        1. Delete (prop_name i, value i)

        key_gen_count = n  <- This is adjusted so the new generated value has the key "prop_name n"
        {..., (prop_name i-1, value i-1), (prop_name i+1, value i+1), ..., (prop_name n, value n)}

        2. Shift value to the left (This is skipped if i = key_gen_count)

        key_gen_count = n
        {..., (prop_name i-1, value i-1), (prop_name i, value i+1), ..., (prop_name n-1, value n)}

        The resulting dictionary has n-1 items. Notice the key "prop_name i"
        reappears, but it now has the value of the next item entry of the
        original dictionary. These steps result in a "left shift" of the values.
        """

        if re.match(self._prop_name + "_[1-9][0-9]*", key):  # If it matches generated key format
            self._key_gen_count -= 1  # Adjust key generator count for the next generated key
            super().__delitem__(key)

            key_index = int(key.rsplit('_', maxsplit=1)[1])
            if key_index < self._key_gen_count:  # "Shift" old entries to the left if it wasn't the last entered
                prop_name = self._prop_name + "_{}"
                new_prop_entries = {prop_name.format(i): self[prop_name.format(i + 1)] for i in
                                    range(key_index, self._key_gen_count)}

                self[key] = new_prop_entries[key]  # Re-register the deleted key
                self.update(new_prop_entries)  # Add the rest of the entries
                super().__delitem__(prop_name.format(self._key_gen_count))  # Delete last entry
        else:
            raise KeyError(f"{key} does not match the generated key format of this class. "
                           "You can check the available keys with the show_variables method.")

    def add(self, *args, **kwargs):
        """
        Add value(s) to the component property.

        For positional arguments (order-invariant components), the key is
        generated by the class.

        For named key arguments (order-dependent components), the key is
        verified to see if it's one of the properties declared by the
        component.

        Both these are used to correctly map and name the variables in
        the generated code.
        """

        if self.is_order_invariant:
            for value in args:
                self[self._prop_name + f"_{self._key_gen_count}"] = value
                self._key_gen_count += 1
        else:
            for key, value in kwargs.items():
                self[key] = value

    def organize_property(self):
        """
        For order invariant systems, this returns an ordered list of values of
        an order invariant component property.

        This is ordered using the internal generated component property key
        count.
        """

        if self.is_order_invariant:
            return [self[self._prop_name + f"_{i}"] for i in range(1, self._key_gen_count)]
        raise AttributeError("Order-dependent component properties do not need to be organized."
                             " Extract the relevant value by using its key/variable.")

    @_non_erasable_order_dependent_method
    def clear(self):
        """
        Remove all items from the component property.

        This only works for order-invariant components.
        """

        super().clear()
        self._key_gen_count = 1

    @_detect_invalid_key_entry
    def pop(self, key):

        try:

            value = self[key]
            del self[key]
            return value

        except KeyError:
            raise KeyError(f'"{key}" was not found and cannot be deleted.')

    @_detect_invalid_key_entry
    @_non_erasable_order_dependent_method
    def popitem(self):
        """Remove and return last generated key entry."""

        prop_name = self._prop_name + f"_{self._key_gen_count - 1}"
        item = (prop_name, self[prop_name])
        del self[prop_name]
        return item

    def show_variables(self):
        """Display all the variables of the component property."""

        print("\n".join(self.keys()))

    def update(self, update_dict=None, **kwargs):
        """Update existing component property entries."""

        if isinstance(update_dict, dict):
            self._update(update_dict)
        elif not isinstance(update_dict, type(None)):
            raise TypeError('The argument "update_dict" must be a dictionary.')

        self._update(kwargs)

    def _determine_property_order_invariance(self, prop_info):

        if prop_info is None:
            self._key_gen_count = 1
            self.is_order_invariant = True
        else:
            self.is_order_invariant = False

    def _update(self, update_dict):

        if all(key in self for key in update_dict):
            super().update(update_dict)
        else:
            non_registered_keys = [key for key in update_dict if key not in self]
            raise KeyError(f"The keys {', '.join(str(non_registered_keys))} are "
                           f"not among the registered keys: {', '.join(self.keys())}.")


# Useful functions, and variables that can used for components building

def _constant_classproperty_helper_factory(name, types):
    """
    Function factory that generates helper functions for creating a constant
    classproperty for a given class attribute.
    """

    doc = BaseComponent.__dict__[name].__doc__
    try:
        type_names = [cls_type.__name__ for cls_type in types]
    except TypeError:
        type_names = types.__name__  # In case only one class was entered

    def generate_constant_class_attribute_helper(value) -> classproperty:
        """Constant classproperty generator for a given attribute"""

        if not isinstance(value, types):
            raise TypeError(f'The value for "{name}" must be one of these types: {", ".join(type_names)}')
        return classproperty.constant_classproperty(name, value, doc)

    return generate_constant_class_attribute_helper


# Attribute factories
# These functions will generate the corresponding attribute (while ensuring it has the correct type for the attribute)

generate_default_name = _constant_classproperty_helper_factory("default_name", str)
generate_has_init_cond = _constant_classproperty_helper_factory("has_init_cond", bool)
generate_input_info = _constant_classproperty_helper_factory("input_info", (tuple, type(None)))
generate_output_info = _constant_classproperty_helper_factory("output_info", (tuple, type(None)))
generate_parameter_info = _constant_classproperty_helper_factory("parameter_info", (tuple, type(None)))
