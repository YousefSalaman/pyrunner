
from Simupynk.runners import BaseRunner, BaseBuilder


class Runner(BaseRunner):

    def __init__(self, group_key, group_funcs, group_vars, group_trans=None):

        super().__init__(group_key, group_funcs, group_vars, group_trans)

    def _run_system_private(self, group_key, sys_name, **kwargs):

        curr_sys_vars = self.group_vars[sys_name]
        sys_func = self.group_func_lists[sys_name]
        curr_sys_vars.update(sys_func(**curr_sys_vars))
        return self._extract_data_from_system_variables(sys_name)


class Builder(BaseBuilder):

    def determine_component_placement(self, comp):

        self.ordered_comps.append(comp)
