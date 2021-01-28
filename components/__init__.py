"""
This package contains all the components of the Simupynk system.
"""

from abc import abstractmethod
from Simupynk.utils.cls_prop import classproperty
from Simupynk.utils.type_abc import CPEnabledTypeABC, abstractclassproperty


__all__ = []


class BaseComponent(CPEnabledTypeABC):
    """
    Base class for component objects.
    """

    def __init__(self, name=None, inputs=None, sys_obj = None):  # Inputs might not be needed for all components

        self.sys = sys_obj  # System that contains object
        self.comp_name = name  # Name of the component
        self.comp_inputs = inputs  # Inputs for the component

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
    def input_lim(self):
        """
        The input range limiter for a component. It dictates how many input
        components a component can have.
        """

    @abstractmethod
    def generateComponentString(self) -> str:
        """
        This generates the functionality of the component within a string.
        """

    def verifyInputSize(self):  # TODO: Mention how the input lims work in doc. Might change this to private

        num_of_inputs = len(self.comp_inputs)
        if num_of_inputs < self.input_lim[0]:  # Lower bound of allowed inputs
            raise AttributeError('Not enough inputs were entered for component of type "{}"'.format(self.default_name))
        if num_of_inputs > self.input_lim[1] and not self.input_lim[1] < 0:  # Upper bound of allowed inputs
            raise AttributeError("Number of inputs for '{}' exceeds component's input limit".format(self.default_name))


# Useful attributes, functions, and variables that can used for components building

def _constant_classproperty_helper_factory(name, doc):
    """
    Function factory that generates helper functions for creating a constant
    classproperty for a given class attribute.
    """

    def generateConstantClassAttributeHelper(value) -> classproperty:
        """Constant classproperty generator for a given attribute"""
        
        return classproperty.constant_classproperty(name, value, doc)

    return generateConstantClassAttributeHelper


# "default_name" attribute

_DEFAULT_NAME_DOC = """
        Default name for a component type. It's used in the creation of its
        name if one wasn't given.
        """  # Docstring for default_name

generateDefaultName = _constant_classproperty_helper_factory("default_name", _DEFAULT_NAME_DOC)  # Helper function

# "input_lim" attribute

_INPUT_LIM_DOC = """
        The input range limiter for a component. It dictates how many input
        components a component can have.
        """

generateInputLim = _constant_classproperty_helper_factory("input_lim", _INPUT_LIM_DOC)  # Helper function

# "has_init_cond" attribute

_HAS_INIT_COND_DOC = """
        States whether or not a component has initial conditions.
        """  # Docstring for has_init_cond

HAS_INIT_COND_TRUE = classproperty.constant_classproperty("has_init_cond", True, _HAS_INIT_COND_DOC)
HAS_INIT_COND_FALSE = classproperty.constant_classproperty("has_init_cond", False, _HAS_INIT_COND_DOC)
