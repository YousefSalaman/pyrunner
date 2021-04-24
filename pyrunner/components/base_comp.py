"""
This module holds the base component class
"""

__all__ = ["BaseComponent",
           "BaseNormalComponent",
           "generate_default_name",
           "generate_direct_feedthrough",
           "generate_input_info",
           "generate_output_info",
           "generate_parameter_info"]


import re
from numbers import Number
from functools import wraps
from abc import abstractmethod
from collections.abc import Callable, Collection

import numpy as np

from ..utils.mixins import CPEnabledTypeABC
from ..utils.cls_prop import classproperty, abstractclassproperty


# Base component classes

class BaseComponent(CPEnabledTypeABC):
    """Interface for component objects.

    All of the necessary component behavior is defined in this class. If you
    want to create a custom component, you only need to inherit and override
    the abstract methods.
    """

    def __init__(self, sys_obj, name=None, **parameters):

        self.sys = sys_obj  # System that contains object
        self.is_not_mapped = True  # Indicates if component has been ordered
        self.code_str = {"Set Up": None, "Execution": None}  # Storage for generated code string
        self.name = sys_obj.register_component_name(self, name)  # Name of the component
        self._input = _ComponentProperty.init("input", self.input_info)  # Inputs of the component
        self._output = _ComponentProperty.init("output", self.output_info)  # Outputs of the component
        self._parameter = _ComponentProperty.init("parameter", self.parameter_info)  # Parameters of the component

        self.parameters.add(**parameters)  # Add any parameters that were specified in the constructor
        if not self.is_block_diagram():
            sys_obj.comps.append(self)  # Add component to system component

    def __repr__(self):

        return self.name

    @abstractclassproperty
    def default_name(self):
        """
        Default name for a component type. It's used in the creation of its
        name if one wasn't given.
        """

    @abstractclassproperty
    def direct_feedthrough(self):
        """
        This indicates if the component is solely dependent of its input
        components or not.

        The attribute is used for determining an order of execution for a
        system. It only comes into question if there is a feedback loop within
        your system. If the loop is composed of only components are direct
        feedthrough, then that loop is considered to be an "algebraic loop". In
        that case, the code will raise an error since solving these is not yet
        supported. Otherwise, if there is a component that is not this in the
        loop, then the loop can be resolved.
        """

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
    def generate_code_string(self):
        """Create the code for the component."""

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

    def is_block_diagram(self):
        """Verifies if component is a block diagram component."""

        return self.sys is self
        # return self.sys is None

    def is_system(self):
        """Verifies if component is a system component."""

        return hasattr(self, "comps")

    def generate_name(self) -> str:
        """Generates a name for a component.

        The name is generated by doing the following:

        - When a component is a system or it does not reside within a subsystem,
          the name for the using the default name of the component, its name is
          generated only using its default name.

        - Otherwise, the component uses the component's system's name + the
          component's default name to generate the name.
        """

        sys_comp = self.sys  # Component's system container (could be a diagram or subsystem)

        # Get the component's name
        name = self.default_name
        is_in_subsystem = not sys_comp.is_block_diagram()
        if not self.is_system() and is_in_subsystem:
            name = sys_comp.name + "_" + name

        return name

    def pass_default_parameters(self):
        """Pass the default parameters stored in the attribute
        parameter_info.

        For this to work, parameter_info[1] has to be a dictionary. If not,
        it will skip the value passing process.
        """

        if self.parameter_info is not None and isinstance(self.parameter_info[1], dict):
            req_parameters, all_parameters = self.parameter_info

            # Get the non-required parameters that were not initialized with a value
            non_init_parameters = {}
            for parameter, default_value in all_parameters.items():
                if parameter not in req_parameters and self.parameters[parameter] is None:
                    non_init_parameters[parameter] = default_value

            self.parameters.update(update_dict=non_init_parameters)

    def verify_properties(self):
        """Verify if the component's properties are well-defined for a
        component.

        By default, it will verify if the component's required properties
        from its inputs, outputs, and parameters were assigned values. If
        you want to add another verification, just override this method,
        use "super" to reference this method and add your verification for
        the component that inherits from this class.
        """

        prop_names = ["inputs", "outputs", "parameters"]
        prop_infos = [self.input_info, self.output_info, self.parameter_info]

        for prop_name, prop_info in zip(prop_names, prop_infos):
            if prop_info is not None:
                self._verify_required_values(prop_name, prop_info)

    def _verify_required_values(self, prop_name, prop_info):

        req_props = prop_info[0]
        comp_prop = getattr(self, prop_name)
        non_assigned_req_props = [req_prop for req_prop in req_props if comp_prop[req_prop] is None]

        if len(non_assigned_req_props) > 0:
            raise TypeError(f'For component "{self}", the following variables {non_assigned_req_props}'
                            f' in "{prop_name}" were not assigned values."')


# Useful functions, and variables that can used for components building

def _persistent_classprop_factory(name, types):
    """Function factory creating persistent classproperties for a given
    class attribute.
    """

    doc = BaseComponent.__dict__[name].__doc__
    try:
        type_names = [cls_type.__name__ for cls_type in types]
    except TypeError:
        type_names = types.__name__  # In case only one class was entered

    def persistent_classprop(value) -> classproperty:
        """Constant classproperty generator for a given attribute"""

        if not isinstance(value, types):
            raise TypeError(f'The value for "{name}" must be one of these types: {", ".join(type_names)}')
        return classproperty.persistent(name, value, doc)

    return persistent_classprop


# Attribute factories
# These functions will generate the corresponding attribute (while ensuring it has the correct type for the attribute)

generate_default_name = _persistent_classprop_factory("default_name", str)
generate_direct_feedthrough = _persistent_classprop_factory("direct_feedthrough", bool)
generate_input_info = _persistent_classprop_factory("input_info", (tuple, type(None)))
generate_output_info = _persistent_classprop_factory("output_info", (tuple, type(None)))
generate_parameter_info = _persistent_classprop_factory("parameter_info", (tuple, type(None)))


class BaseNormalComponent(BaseComponent):
    """Interface for "normal" component objects.

    "Normal" components are components that are not system components, so
    these cannot store items inside of them. In addition to this, these
    components have the following restrictions:

    - Their output property cannot be modified. That is, you cannot add
      items to their output. This is only reserved for system components.

    All of these restrictions are present in this base class, so you do not
    need to recreate them if you inherit from this class.
    """

    output_info = generate_output_info(({}, {}))

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
    def parameter_info(self):
        pass

    @abstractmethod
    def generate_code_string(self):
        pass


# ComponentProperty definition and helper decorators

def _non_erasable_order_dependent_method(func):
    """Decorator to disable item deletion for order-dependent properties."""

    @wraps(func)
    def method_wrapper(*args):
        self = args[0]
        if self.is_order_invariant:
            return func(*args)
        raise AttributeError("You cannot erase the items of an order-dependent property.")

    return method_wrapper


def _detect_invalid_key_entry(func):
    """Decorator to detect if an invalid key was entered in a method."""

    @wraps(func)
    def method_wrapper(*args):

        self = args[0]
        try:
            func(*args)
        except KeyError as error:
            raise KeyError("Item could not be deleted. You either entered an invalid key "
                           f"or the {self.prop_name}s are empty.") from error

    return method_wrapper


def _block_outside_modification(func):
    """Decorator to lock item accessor methods from working outside a method."""

    def block_wrapper(*args):
        self = args[0]
        if self._within_method:
            func(*args)
        else:
            raise AttributeError("You can only modify property items through the publicly "
                                 "available methods.")

    return block_wrapper


class _ComponentProperty(dict):
    """A class for storing and mapping component properties such as
    inputs, outputs, and parameters (for calculations.)

    These properties are classified as follows:

    - Order-invariant:
        These properties either have one or a variable amount of components.
        One can specify a property is of this type by putting "None" in the
        property in the component's class.

    - Order-dependent:
        These properties have an explicit finite amount of elements in the
        system. This is specified by putting a 2-tuple with elements, which are
        containers, that indicate the required elements and all the elements,
        respectively. That is:

        (
        {"var_i", ..., "var_i+k"},  <- The required variables (marked by the subscript "i")
        {"var_1", ..., "var_i", ..., "var_i+k", ..., "var_n"} <- All the variables defined by the property
        )

    ComponentProperty objects have the following properties:

    - Order-dependent properties can only assign values to the keys determined
      by the class, the second element in the property's info tuple,

    - Order-invariant components can only assign values to keys that match
      the regex "{prop_type}_[1-9][0-9]*", where prop_type is input, output,
      or parameter.

    - Order-invariant components generate keys by using the add method,
      which means you should use this method to add new property entries. To
      change the value of the property, you can use the generated key to
      access and modify the value or use the update method.

    - For a component to not accept any entries on the property, set the
      system to be order-dependent with the info tuple ({},{}). This tells
      the class that you have a finite amount of entries (the amount being 0
      in this case) and it will reject any input it is given.

    - For order-invariant properties, when an item is deleted, the other
      subsequent items are "shifted" to the "left". That is, suppose we have
      a property with n variables named "prop_name". If for some i such that
      i < n, its respective key-value pair, (prop_name i, value i), is
      deleted, then the following happens:

        - Original property:

            key_gen_count = n + 1

            {(prop_name 1, value 1),
             ...,
             (prop_name i, value i),
             ...,
             (prop_name n, value n)}

        - Delete (prop_name i, value i):

            key_gen_count = n  <- This is adjusted so the new generated value has the key "prop_name n"

            {...,
            (prop_name i-1, value i-1), (prop_name i+1, value i+1),
            ...,
            (prop_name n, value n)}

        - Pass entry values to the left (The subsequent steps are skipped if i = key_gen_count):

            key_gen_count = n

            {(prop_name 1, value 1),
            ...,
            (prop_name i-1, value i-1), (prop_name i, value i+1),
            ...,
            (prop_name n-1, value n), (prop_name n, value n)}

        - Delete the nth entry:

            key_gen_count = n

            {(prop_name 1, value 1),
            ...,
            (prop_name i-1, value i-1), (prop_name i, value i+1),
            ...,
            (prop_name n-1, value n)}

      The resulting dictionary has n-1 items. Notice the key "prop_name i"
      reappears, but it now has the value of the next item entry of the
      original dictionary. These steps result in a "left shift" of the
      values.
    """

    _ALLOWED_TYPES = {"input": (BaseComponent, type(None)),
                      "output": (BaseComponent, type(None)),
                      "parameter": (Number, Callable, Collection, np.generic, np.ndarray, type(None))}

    # Component property initialization

    def __init__(self, new_dict: dict, prop_name: str, prop_info):

        self.prop_name = prop_name  # Property name
        self._within_method = False  # Verify if the object is being modified within a method
        if prop_info is None:
            self._key_gen_count = 1
            self.is_order_invariant = True
        else:
            self.is_order_invariant = False

        super().__init__(new_dict)

    @_block_outside_modification
    @_non_erasable_order_dependent_method
    def __delitem__(self, key: str):

        if re.match(self.prop_name + "_[1-9][0-9]*", key):  # If it matches generated key format
            self._key_gen_count -= 1  # Adjust key generator count for the next generated key
            super().__delitem__(key)
            self._shift_values_to_the_left(key)
        else:
            raise KeyError(f"{key} does not match the generated key format of this class. "
                           "You can check the available keys with the show_variables method.")

    @_block_outside_modification
    def __setitem__(self, key: str, value):

        self._check_key_type(key)
        self._check_value_type(value)
        if self.is_order_invariant:
            self._check_for_key_generated_format(key)
        else:
            self._check_if_key_is_in_defined_variables(key)

        super().__setitem__(key, value)

    def add(self, *args, **kwargs):
        """Add value(s) to the component property.

        For positional arguments (order-invariant properties), the key is
        generated by the class.

        For named key arguments (order-dependent properties), the key is
        verified to see if it's one of the variables declared by the
        component.
        """

        self._within_method = True

        # Add item(s)
        if self.is_order_invariant:
            for value in args:
                self[self.prop_name + f"_{self._key_gen_count}"] = value
                self._key_gen_count += 1
        else:
            for key, value in kwargs.items():
                self[key] = value

        self._within_method = False

    @_non_erasable_order_dependent_method
    def clear(self):
        """Remove all items from the component property.

        This only works for order-invariant components.
        """

        super().clear()
        self._key_gen_count = 1

    def get_prop_variables(self):
        """Display all the variables of the component property."""

        return list(self)

    @staticmethod
    def init(prop_name, prop_info):
        """Shorthand constructor for initializing component properties."""

        if prop_info is None:
            return _ComponentProperty({}, prop_name, prop_info)
        return _ComponentProperty({prop_name: None for prop_name in prop_info[1]}, prop_name, prop_info)

    @_detect_invalid_key_entry
    def pop(self, key: str):
        """Remove the specified entry and return its value.

        Note the key will still be there if it wasn't the last one generated.
        The last key will be deleted and from the chosen key onwards
        """

        self._within_method = True

        # Pop the specified entry
        value = self[key]
        del self[key]

        self._within_method = False
        return value

    @_detect_invalid_key_entry
    @_non_erasable_order_dependent_method
    def popitem(self):
        """Remove and return last generated key entry."""

        self._within_method = True

        # Pop the item
        prop_name = self.prop_name + f"_{self._key_gen_count - 1}"
        item = (prop_name, self[prop_name])
        del self[prop_name]

        self._within_method = False
        return item

    def remove(self, value):
        """Remove the given value from the property."""

        self._within_method = True

        # Remove the component
        for key, prop_comp in self.copy().items():
            if prop_comp == value:
                if self.is_order_invariant:
                    del self[key]
                else:
                    self[key] = None

        self._within_method = False

    def sort(self) -> list:
        """Returns an ordered list of values of an order-invariant property.

        The returned list is ordered using the internal generated component property key
        count. That is, if k is the current key generated count and a property called
        "prop", then for every i, j such that k > i > j, "prop_j" will appear before
        "prop_i" in the resulting list.

        For example, if k = 4, then ["prop_1", "prop_2", "prop_3"] is the resulting list.
        """

        if self.is_order_invariant:
            return [self[self.prop_name + f"_{i}"] for i in range(1, self._key_gen_count)]
        raise AttributeError("Order-dependent component properties do not need to be organized."
                             " Extract the relevant value by using its key/variable.")

    def update(self, update_dict=None, **kwargs):
        """Update existing component property entries."""

        if isinstance(update_dict, dict):
            self._update(update_dict)
        elif not isinstance(update_dict, type(None)):
            raise TypeError('The argument "kwargs" must be a dictionary.')

        self._update(kwargs)

    @staticmethod
    def _check_key_type(key: str):

        if not isinstance(key, str):
            raise TypeError("The key/variable of a component property must be a string.")

    def _check_value_type(self, value):

        prop_types = self._ALLOWED_TYPES[self.prop_name]
        if not isinstance(value, prop_types):
            try:
                prop_type_names = [prop_type.__name__ for prop_type in prop_types]
            except TypeError:
                prop_type_names = [prop_types.__name__]
            raise TypeError(f'The value "{value}" must be an instance of one '
                            f'of these classes: {", ".join(prop_type_names)}')

    def _check_for_key_generated_format(self, key):

        generated_key_format = self.prop_name + "_[1-9][0-9]*"  # Generated key format for order-invariant property
        if re.match(generated_key_format, key):
            key_index = int(key.rsplit('_', maxsplit=1)[1])
            if key_index > self._key_gen_count:  # Check if extracted key number is among the generated count
                raise KeyError(f'The key "{key}" belongs to a key that has not been generated.'
                               "Use the add method to register values or the show_variables "
                               "method to display the created keys.")
        else:
            raise KeyError(f'"{key}" does not match the format {self.prop_name}_#, which '
                           'is the one used to generate for order-invariant properties. '
                           'Use the method to register values or the show_variables method '
                           'to display the created keys.')

    def _check_if_key_is_in_defined_variables(self, key):

        if key not in self:
            if len(self) == 0:
                raise KeyError(f"No entries are allowed for the component's {self.prop_name}s.")
            raise KeyError(f'The variable "{key}" is not among these variables: {", ".join(self.keys())}.')

    def _shift_values_to_the_left(self, key):

        key_index = int(key.rsplit('_', maxsplit=1)[1])
        if key_index < self._key_gen_count:  # "Shift" old entries to the left if it wasn't the last entered
            prop_name = self.prop_name + "_{}"
            new_prop_entries = {prop_name.format(i): self[prop_name.format(i + 1)] for i in
                                range(key_index, self._key_gen_count)}

            self[key] = new_prop_entries[key]  # Re-register the deleted key
            self.update(new_prop_entries)  # Add the rest of the entries
            super().__delitem__(prop_name.format(self._key_gen_count))  # Delete last entry

    def _update(self, kwargs: dict):

        non_registered_keys = [key for key in kwargs if key not in self]  # List of invalid keys
        if len(non_registered_keys) == 0:  # If no invalid key was entered
            super().update(kwargs)
        else:
            raise KeyError(f"The keys '{', '.join(non_registered_keys)}' are "
                           f"not among the registered keys: {', '.join(self.keys())}.")
