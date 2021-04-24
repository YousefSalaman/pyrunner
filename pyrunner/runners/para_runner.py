# -*- coding: utf-8 -*-

import itertools as it
import multiprocessing as mp

from .base_runner import *


class Runner(BaseRunner):
    """
    This is a concurrent-enabled runner.
    """

    def __init__(self, group_key, group_func_lists, group_vars, group_trans=None):
        """
        Sum system to the ParallelRunner class. This must be used after creating an instance of this class for the
        system.
        """

        self.pool = None
        self.sys_locks = {}  # Dictionary for function locks
        self.sys_ranges = {}  # Dictionary for system ranges
        self._create_system_storages()

        super().__init__(group_key, group_func_lists, group_vars, group_trans)

    def _run_system_private(self, group_key, sys_name, kwargs):

        self.act_sys[group_key] = sys_name  # Update the active system
        self.group_vars.update(kwargs)  # Update the necessary variables before running

        self._use_pool(sys_name)
        self._lock_all_functions(sys_name)

        return self._extract_data_from_system_variables(sys_name)

    @classmethod
    def start_process_concurrency(cls, runner_pool_cnt=None):
        # Initialize all the concurrent elements for the class and its instances

        cls.global_mgr = mp.Manager()  # Sum proxy to manage all runner objects
        act_sys = cls.global_mgr.dict()  # Dictionary to see which system is active in a group

        # Initialize runner-specific concurrent variables
        for runner in cls._runner_instances.values():
            runner.act_sys = act_sys
            runner.act_sys[runner.group_key] = None  # Initialize runner active system to none
            runner._pass_instance_values_to_manager()
            runner._create_runner_process_pool(runner_pool_cnt)

    @classmethod
    def end_process_concurrency(cls):
        """Terminate all the runner instance pools"""

        for runner in cls._runner_instances.values():
            runner.pool.close()
            runner.pool.join()

    def _create_system_storages(self):  # TODO: Add initializer for the system variables

        for sys_name, func_list in self.group_func_lists.items():
            self.sys_ranges[sys_name] = range(len(func_list))
            self.sys_locks[sys_name] = {sys_func.__name__: True for sys_func in func_list}

    def _pass_instance_values_to_manager(self):

        group_vars = self.global_mgr.dict()  # Manager dictionary for variables
        sys_locks = self.global_mgr.dict()  # Manger dictionary for the current locks

        for sys_name in self.group_func_lists:
            # Create manager dictionaries for storages
            group_vars[sys_name] = self.global_mgr.dict()
            sys_locks[sys_name] = self.global_mgr.dict()

            # Update dictionaries with previously defined dictionaries
            group_vars[sys_name].update(self.group_vars[sys_name])
            sys_locks[sys_name].update(self.sys_locks[sys_name])

        # Pass values
        self.group_vars = group_vars
        self.sys_locks = sys_locks

    def _create_runner_process_pool(self, runner_pool_cnt):

        if runner_pool_cnt is None or self.group_key not in runner_pool_cnt:
            self.pool = mp.Pool()
        else:
            self.pool = mp.Pool(processes=runner_pool_cnt[self.group_key])

    def _use_pool(self, sys_name):  # Might put directly in runSystem
        """
            This serves as an indirect way for running the different process
        functions. It only accepts the index of the function you want to run.
        """

        self.pool.map(self._run_functions_concurrently, self.sys_ranges[sys_name])

    def _run_functions_concurrently(self, func_num):

        sys_name = self.act_sys[self.group_key]  # Get system name
        sys_func = self.group_func_lists[sys_name][func_num]

        # This prevents the function from running until the prerequisite functions are ran
        while eval(sys_func.lock_logic):
            pass

        # Evaluate function and update variables
        curr_sys_vars = self.sys_vars[sys_name]  # Current system variables

        res_dict = sys_func(**curr_sys_vars)
        if res_dict is not None:
            curr_sys_vars.update(res_dict)

        self.sys_locks[sys_name][sys_func.__name__] = False  # This unlocks the function

    def _lock_all_functions(self, sys_name):  # Might put directly in runSystem

        curr_sys_locks = self.sys_locks[sys_name]
        for func_name in curr_sys_locks.keys():
            curr_sys_locks[func_name] = True

    def __getstate__(self):
        # This method is called before pickling the class and it can modify how its pickled

        pickle_dict = self.__dict__.copy()  # Dictionary to be pickled
        del pickle_dict['pool']  # Remove pool attribute from copy

        return pickle_dict  # This will be the input of __setstate__

    def __setstate__(self, unpickle_dict):

        self.__dict__.update(unpickle_dict)


# Order of Execution builder

class Builder(BaseBuilder):

    def __init__(self):

        self.comp = None  # This is not used for code generation but it's useful in the builder
        self.front_cnt = 0
        self.is_meshable = True

        super().__init__()

    def define_sys_info(self, sys_comps):
        """
        sys_info legend:

        'inputs' - inputs of comp
        'comp_loc' - which path the comp is located on (initialized at 0)
        'call_cnt' - # of times it is used as an input in graph (initialized at 0)
        """

        super().define_sys_info(sys_comps)

        for value in self.sys_info.values():
            value.update({'comp_loc': 0, 'call_cnt': 0})

    def map_component(self, comp):
        """
        This determines where a component should be placed using a "path"
        scheme. With the appropriate structure, these paths can be run in
        parallel.
        """

        self.comp = comp

        if len(self.sys_info[comp]['inputs']) == 0:
            self._build_start_component()
        else:
            self._build_non_start_component()

    def _build_start_component(self):

        self._add_component_to_path(0)

        self.front_cnt += 1
        if self.front_cnt > 1:  # Check for meshability
            self.is_meshable = False

    def _build_non_start_component(self):

        if len(self.sys_info[self.comp]['inputs']) == 1:
            self._handle_single_input_component()
        else:
            self._handle_multiple_input_component()

    def _handle_single_input_component(self):

        input_comp = self.sys_info[self.comp]['inputs'][0]
        input_loc = self.sys_info[input_comp]['comp_loc']
        input_path = self.ordered_comps[input_loc]
        input_index = input_path.index(input_comp)

        self.sys_info[input_comp]['call_cnt'] += 1  # Update input call _key_gen_count
        input_call_cnt = self.sys_info[input_comp]['call_cnt']

        # If called only once, the current comp is placed right next to its input
        if input_call_cnt == 1:  # This calls
            input_path.insert(input_index + 1, self.comp)
            self.sys_info[self.comp]['comp_loc'] = input_loc

        # If called twice, the previous comp that calls input_comp is
        # separated into a new path
        if input_call_cnt == 2:
            self.ordered_comps.insert(input_loc + 1, input_path[input_index + 1:])
            input_path[input_index + 1:] = []

        # For inputs that are called more than once, the current component is
        # placed into a new path
        if input_call_cnt > 1:
            self._add_component_to_path(input_loc + 1)

    def _handle_multiple_input_component(self):
        """
        Finds the highest input path location and places current component in
        a new path after this.
        """

        comp_inputs = self.sys_info[self.comp]['inputs']
        max_input_loc = max(self.sys_info[input_comp]['comp_loc'] for input_comp in comp_inputs)

        self._add_component_to_path(max_input_loc + 1)

    def _add_component_to_path(self, comp_loc):

        self._update_other_path_indices(comp_loc)

        self.sys_info[self.comp]['comp_loc'] = comp_loc  # Update component location
        self.ordered_comps.insert(comp_loc, [self.comp])  # Sum component to assigned path

    def _update_other_path_indices(self, start_index):
        """
        Update path index for all the components that were mapped from the
        starting index and forward.
        """

        paths_to_shift = self.ordered_comps[start_index:]
        for comp in it.chain.from_iterable(paths_to_shift):
            self.sys_info[comp]['comp_loc'] += 1
