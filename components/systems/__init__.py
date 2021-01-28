"""
Placeholder
"""

import Simupynk.components as comps
from Simupynk.utils.sys_utils import *
from Simupynk.utils.type_abc import abstractclassproperty


class BaseSystem(comps.BaseComponent):

    @abstractclassproperty
    def default_name(self):
        pass

    @abstractclassproperty
    def has_init_cond(self):
        pass

    @abstractclassproperty
    def input_lim(self):
        pass

    def __init__(self, name=None, inputs=None, sys_obj=None):

        self._sys_comp_struct = {}  # Dictionary with components within the system along with their inputs
        self._name_mgr = name_mgr.NameManager()  # Name manager for system
        super().__init__(name, inputs, sys_obj)

    def generateComponentString(self):
        pass


if __name__ == "__main__":

    a = BaseSystem()