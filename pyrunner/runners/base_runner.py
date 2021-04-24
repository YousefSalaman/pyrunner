
__all__ = ["BaseRunner",
           "BaseBuilder"]


from abc import abstractmethod

from ..utils.type_abc import TypeABC


# TODO: Remove the group key from runner to simplify code
class BaseRunner(TypeABC):
    """A base class for runner objects."""

    _runner_instances = {}  # Dictionary to store runner instances

    def __init__(self, group_key, group_func_lists, group_vars, group_trans=None):

        self.group_key = group_key  # String/key to identify system
        self.group_vars = group_vars  # Dictionary for variables
        self.group_trans = group_trans  # Dictionary for system translators
        self.group_func_lists = group_func_lists  # List containing the functions/process to runs the system.

        self._runner_instances[group_key] = self  # Save instance

    @classmethod
    def run_system(cls, group_key, sys_name, **kwargs):
        """Evaluates stored functions and returns relevant values."""

        runner = cls._runner_instances[group_key]
        return runner._run_system_private(group_key, sys_name, kwargs)

    @abstractmethod
    def _run_system_private(self, group_key, sys_name, kwargs):
        pass

    def _extract_data_from_system_variables(self, sys_name):

        if self.group_trans is not None:
            curr_sys_vars = self.group_vars[sys_name]  # Current system shared variables
            curr_sys_trans = self.group_trans[sys_name]  # Current system transitions
            return {curr_sys_trans[key]: value for key, value in curr_sys_vars.items() if key in curr_sys_trans}
        return None


class BaseBuilder(TypeABC):
    """Base class for builder objects"""

    def __init__(self):

        self.sys_info = None
        self._sys_trail = []   # Store components in trail to detect if the system is cyclic (has a feedback loop)
        self.ordered_comps = []

    @abstractmethod
    def map_component(self, comp):
        """
        Determine where a component should be in its system order of
        execution based on the criteria established by this method.
        """

    def define_sys_info(self, sys_comps):
        """
        Create a dictionary to hold relevant information of each component of
        the system. This is used to define some attributes of the builder
        object for code generation.

        Sys info is a dictionary with the following structure:

        - As keys, it has the system's components.

        - As values, it has dictionaries with additional information of the
          component. By default, the dictionary contains an entry with
          key = 'inputs' and value = list of the components inputs. This is the
          only one that is used in the traversal process of the system.

        The diagram below shows the structure of the dictionary:

        {
            comp_1 : {'inputs': [...], ...},
            .
            .
            .
            comp_n : {'inputs': [...], ...}
        }

        To add any additional entries to each sub-dictionary, just override
        this method, update the resulting dictionary, and return it.
        """

        self.sys_info = {comp: {'inputs': list(set(comp.inputs.values()))} for comp in sys_comps}

    def build_system_order(self, comp):

        self._sys_trail.append(comp)  # Record component in the trail

        comp_inputs = self.sys_info[comp]['inputs']
        for input_comp in comp_inputs:
            if input_comp in self._sys_trail:  # There's a feedback loop in your system (system is cyclic)
                self._sever_system_loop(input_comp)
            if input_comp.is_not_mapped:
                self.build_system_order(input_comp)

        if comp.is_not_mapped:
            self.map_component(comp)
            comp.is_not_mapped = False
            if comp in self._sys_trail:  # Remove component from trail after finishing
                self._sys_trail.remove(comp)

    def _sever_system_loop(self, comp):
        """
        Split the system loop by removing the input component to a component
        that is non-direct feedthrough, where both components are within the
        loop.
        """

        non_direct_comp, loop_input_comp = self._get_loop_components(comp)
        self.sys_info[non_direct_comp]['inputs'].remove(loop_input_comp)

        self._sys_trail.clear()

    def _get_loop_components(self, comp):
        """
        Gets non-direct feedthrough component and its input component in the
        loop.
        """

        input_index = self._sys_trail.index(comp)
        sys_loop = self._sys_trail[input_index:]  # Gets the loop portion in the recorded trail

        for loop_comp_index, loop_comp in enumerate(sys_loop):
            loop_input_comp = self._get_component_input_in_loop(loop_comp_index, sys_loop)
            if not loop_input_comp.direct_feedthrough:
                return loop_comp, loop_input_comp

        raise Exception("System cannot process algebraic loops. There needs to be "
                        "a non-direct feedthrough component in your feedback loop.")

    @staticmethod
    def _get_component_input_in_loop(loop_comp_index, sys_loop):
        """Get loop component's input within a system loop."""

        try:  # Normally, next element in sys_loop is the input
            return sys_loop[loop_comp_index + 1]
        except IndexError:  # If loop_comp is the last element, its input is first comp in sys_loop
            return sys_loop[0]
