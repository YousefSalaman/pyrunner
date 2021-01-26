"""
This package contains runner objects. These serve as wrappers to a set of
functions/system. The main purpose of these objects is to simplify code that
run different calculations and require different set-ups. External code that
call these objects don't need to worry about how to run a system since the
set-ups and functions to run a system are contained within the runner objects
and these can be ran indirectly through the method runSystem method.
"""

from simupynk.utils.type_abc import TypeABC, abstractmethod


__all__ = ["seq_runner", "para_runner"]


class BaseRunner(TypeABC):
    """A base class for runner objects."""

    _runner_instances = {}  # Dictionary to store runner instances

    def __init__(self, group_key, group_func_lists, group_vars, group_trans=None):

        self._runner_instances[group_key] = self  # Save instance

        self.group_key = group_key  # String/key to identify system
        self.group_vars = group_vars  # Dictionary for variables
        self.group_trans = group_trans  # Dictionary for system translators
        self.group_func_lists = group_func_lists  # List containing the functions/process to runs the system.

    @classmethod
    def runSystem(cls, group_key, sys_name, **kwargs):
        """Evaluates stored functions and returns relevant values."""

        runner = cls._runner_instances[group_key]
        return runner._runSystemPrivate(group_key, sys_name, kwargs)

    @abstractmethod
    def _runSystemPrivate(self, group_key, sys_name, kwargs):
        pass

    def _extractDataFromSystemVariables(self, sys_name):

        if self.group_trans is not None:
            curr_sys_vars = self.group_vars[sys_name]  # Current system shared variables
            curr_sys_trans = self.group_trans[sys_name]  # Current system transitions
            return {curr_sys_trans[key]: value for key, value in curr_sys_vars.items() if key in curr_sys_trans}
        return None
