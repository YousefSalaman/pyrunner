"""
Placeholder
"""

from Simupynk.utils.sys_utils import *
from Simupynk.components import BaseComponent
from Simupynk.utils.type_abc import abstractclassproperty


class BaseSystem(BaseComponent):

    _main_systems = []

    def __init__(self, name=None, sys_obj=None):

        self.sys_comps = []  # Dictionary with components within the system along with their inputs
        if sys_obj is None:
            self._initMainSystem(name)
        else:
            self.main_sys = sys_obj.main_sys  # Pass reference to main system to current system
        super().__init__(name, sys_obj)

    def generateComponentString(self):
        pass

    def buildSystem(self):  # Might not leave this here. Will only define for user-defined systems

        if self is not self.main_sys:
            raise TypeError('Only "main" systems can be built')
        self.verifyAttributesForSystemComponents()
        organizeSystem()
        self.generateComponentString()

    @classmethod
    def buildSystems(cls):
        """
        For multiple main systems, you can use this method to build all of them contained within a system class.
        """

        for main_sys in cls._main_systems:
            main_sys.buildSystem()

    def verifyAttributesForSystemComponents(self):

        for comp in self.sys_comps:
            self._verifyComponentName(comp)
            comp.verifyComponentProperties()
            if isinstance(comp, BaseSystem):  # If component is a also system, verify its attributes
                comp.verifyAttributesForSystemComponents()

    def _initMainSystem(self, name):  # Might move this from here, so other systems don't have access to this

        if name is None:
            raise NameError('A "main" system must have a name')

        self.name = name
        self.main_sys = self
        self.name_mgr = name_mgr.NameManager()  # A "namespace" to register components

        self._main_systems.append(self)  # Register main system in class

    def _verifyComponentName(self, comp):

        if comp.name is None:
            self.main_sys.name_mgr.generateComponentName(comp)
        else:
            self.main_sys.name_mgr.verifyCustomComponentName(comp.name)

    @abstractclassproperty
    def default_name(self):
        pass

    @abstractclassproperty
    def has_init_cond(self):
        pass

    @abstractclassproperty
    def input_info(self):
        pass

    @abstractclassproperty
    def output_info(self):
        pass

    @abstractclassproperty
    def parameter_info(self):
        pass
