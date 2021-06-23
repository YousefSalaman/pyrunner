"""
This module contains the Product component.

This component performs the same operation as Simulink's Product block:

- https://www.mathworks.com/help/simulink/slref/product.html
"""

from .. import base_comp


# Function helpers


def _generate_string_for_mult(inputs, parameters):
    # checking that type parameter is correct
    mult_string =  ['element', 'matrix1', 'matrix2']
    if parameters['mult'] not in mult_string:
        raise AttributeError('{} is not a valid mode'.format(parameters['multiplication']))

    code_str = ""

    if parameters["mult"] == "element":
        code_str = 'np.multiply({},{})'.format(inputs["value"], inputs["constant"])

    elif parameters["mult"] == "matrix1":
        code_str = 'np.dot({},{})'.format(inputs["value"], inputs["constant"])

    elif parameters["mult"] == "matrix2":
        code_str = 'np.dot({},{})'.format(inputs["constant"], inputs["value"])

    return code_str


# Product component definition


class Product(base_comp.BaseComponent):
    """The Product component outputs the result of multiplying two inputs: two scalars,
    a scalar and a nonscalar, or two nonscalars that have the same dimensions.

    Parameters
    ----------

    - name : str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

    - mult : string
        This parameter allows the user to specify element_wise or matrix multiplcation.
        element (K.*u): Each element of the input is multiplied by each element of the gain.
        matrix1 (K*u): The input and the gain are matrix-multiplied with the input as the
        second operand.
        matrix2 (u*K): The input and the gain are matrix-multiplied with the input as the
        first operand.
        Default is None(it will proceed to do it element by element).

    - constant : scalar, vector, matrix or component
        This parameter specifies what value will be used for the multiplication.
        Default is 1.

    Inputs
    ------
     - Value:
        It can vary, but it must be more than or equal to one.
        :type scalar, vector, matrix or component

    Outputs
    -------
    - The output is a scalar value, equal to the minimum or maximum of the input elements

    """

    default_name = base_comp.generate_default_name("product")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"value", "constant"}, {"value", "constant"}),
            "outputs": ({}, {}),
            "parameters": ({}, {"mult": None})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(Product, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        start_str = self.name + " = "
        mult_string = _generate_string_for_mult(self.inputs, self.parameters)
        self.code_str["Execution"] = start_str + mult_string
