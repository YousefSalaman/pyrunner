"""
This module contains the Divide component.

This component performs the same operation as Simulink's Divide block:

- https://www.mathworks.com/help/simulink/slref/divide.html
"""

from .. import base_comp


class Divide(base_comp.BaseComponent):
    """The divide component outputs the result of dividing its first input by its second.

     Parameters
     ----------

     - name : str
         Name of the component. The default is None and this will generate a name
         for the component since it was not given one.

     Inputs
     ------

     - numerator : scalar, nonscalar or component
         Sequence of characters specifying the sign of a number. This is a required
         parameter.

    - denominator : scalar, nonscalar or component
         Sequence of characters specifying the sign of a number. This is a required
         parameter.

     Outputs
     -------

     Output computed by dividing inputs.

     -
     """

    default_name = base_comp.generate_default_name("divide")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"numerator", "denominator"},{"numerator", "denominator"}),
            "outputs": ({}, {}),
            "parameters": ({},{})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):

        super(Divide, self).__init__(sys_obj, name,**parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        start_str = self.name + " = "
        divide_str = 'np.divide({},{})'.format(self.inputs["numerator"],self.inputs["denominator"])
        self.code_str['Execution'] = start_str + divide_str
