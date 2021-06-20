"""
This module contains the MinMax component.

This component performs the same operation as Simulink's MinMax block:

- https://www.mathworks.com/help/simulink/slref/minmax.html
"""

from .. import base_comp


class MinMax(base_comp.BaseComponent):
    """The MinMax block outputs either the minimum or the maximum element or elements
    of the inputs. You choose whether the objects outputs the minimum or maximum values
    by setting type parameter.

    Parameters
    ----------

    - name : str
        Name of the component. The default is None and this will generate a name
        for the component since it was not given one.

    - type : str
        A string specifying what numpy function will be used to perform the min/max:
        min : triggers numpy's amin function to calculate the minimum of the input.
        max : triggers numpy's amax function to calculate the maximum of the input.

    Inputs
    ------
     - Value:
        It can vary, but it must be more than or equal to one.
        :type scalar, vector, matrix or component

    Outputs
    -------

    - The output is a scalar value, equal to the minimum or maximum of the input elements

    """

    default_name = base_comp.generate_default_name("min_max")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({"value"},{"value"}),
            "outputs": ({}, {}),
            "parameters": ({"type"}, {"type"})
        }
    )

    _LIB_DEPS = {"numpy": "np"}

    def __init__(self, sys_obj, name=None, **parameters):
        super(MinMax, self).__init__(sys_obj, name, **parameters)

        self._lib_deps = self._LIB_DEPS

    def generate_code_string(self):
        if self.parameters["type"] == min:
            self.code_str['Execution'] = '{} = np.amin({})'.format(self.name,self.inputs["value"])
        elif self.parameters["type"] == max:
            self.code_str['Execution'] = '{} = np.amax({})'.format(self.name,self.inputs["value"])
