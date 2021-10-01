"""
This module contains the Gain component.

This component performs the same operation as Simulink's Gain block:

- https://www.mathworks.com/help/simulink/slref/gain.html
"""

from ..systems import BaseSubsystem
from .. import base_comp
from .product import Product
from ..discontinuities.saturation import Saturation


# Helper functions

def _generate_product_component(system, parameters):
    mult = ""
    if parameters["multiplication"] == "element_wise" or parameters["multiplication"] is None:
        mult = Product(system, mult="element")
    elif parameters["multiplication"] == "matrix_mode1":
        mult = Product(system, mult="matrix")
    elif parameters["multiplication"] == "matrix_mode2":
        mult = Product(system, mult="matrix2")

    return mult


# Gain component definition


class Gain(BaseSubsystem):
    """A component that multiplies the input by a constant value (gain).

    Parameters
    ----------

    - name : str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

     - gain : constant value (scalar, vector, matrix or component)
        Parameter used to specify the value of the gain.
        Default is 1.

    - lower_limit : int
        Parameter used to specify the minimum value of the gain.
        Default is None.


    - upper_limit : int
        Parameter used to specify the maximum value of the gain.
        Default is None.

    - multiplication : string
        This parameter allows the user to specify element_wise or matrix multiplcation.
        element_wise (K.*u): Each element of the input is multiplied by each element of the gain.
        matrix_mode1 (K*u): The input and the gain are matrix-multiplied with the input as the
        second operand.
        matrix_mode2 (u*K): The input and the gain are matrix-multiplied with the input as the
        first operand.
        Default is None(it will proceed to do it element by element).

    Inputs
    ------

    - It can vary, but it must be more than or equal to one.
    :type scalar, vector, matrix or component

    Outputs
    -------

    - The Gain object outputs the input multiplied by a constant gain value.

    """

    default_name = base_comp.generate_default_name("gain")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"value", "gain"}, {"value", "gain"}),
            "outputs": ({"output"}, {"output"}),
            "parameters": ({}, {"lower_limit": None, "upper_limit": None, "multiplication": None})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super().__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def _create_components(self):
        self.mult = _generate_product_component(self, self.parameters)
        # self.saturator = Saturation(self, low_lim=self.parameters["lower_limit"],
        #                             up_lim=self.parameters["upper_limit"], out_min=-10, out_max=1000)
        # self.saturator.inputs.update({"value": self.mult})
        self.outputs.update({"output": self.mult})

    def verify_properties(self):
        self.mult.inputs.update({"value": self.inputs["value"]})
        self.mult.inputs.update({"constant": self.inputs["gain"]})
        super().verify_properties()
        if self.parameters["lower_limit"] is None and self.parameters["upper_limit"] is None:
            raise AttributeError("Both Limits cannot be None. Insert a value to at least 1 limit.")
