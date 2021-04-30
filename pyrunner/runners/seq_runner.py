
from collections.abc import Generator

from . import base_runner


class Builder(base_runner.BaseBuilder):

    def gather_code_parts(self, diagram):

        self.inits = ""
        self.processes = ""

        self.processes += "\n\t" "while True:"
        self.inits += "\n\n" f"def {diagram.name}():"
        self._merge_component_code(diagram)

        self.inits += '\n\t' + self.build_yield(diagram, enable_output=False)
        self.processes += '\n\t\t' + self.build_yield(diagram) + self._generate_executor_str(diagram)

    @classmethod
    def merge_code_parts(cls, imports: str, builders: set) -> str:

        code = imports
        for builder in builders:
            code += builder.inits + builder.processes
        return code

    def _merge_component_code(self, system):

        for comp in system.organizer.ordered_comps:
            if comp.code_str["Set Up"] is not None:  # Build Set Up
                self.inits += "\n\t" + comp.code_str['Set Up']
            if comp.code_str["Execution"] is not None:  # Build process
                self.processes += '\n\t\t' + comp.code_str['Execution']
            if comp.is_system():  # Get code from subsystem
                self._merge_component_code(comp)

    @staticmethod
    def _generate_executor_str(diagram):

        return '\n\n\n' + f'{diagram.name}_exec = {diagram.runner_name}.Executor("{diagram.name}", ' \
                        f'{diagram.name}(), {[str(comp) for comp in diagram.inputs.sort()]})'

    @staticmethod
    def build_yield(diagram, enable_output=True):

        yield_str = 'yield '
        if len(diagram.inputs) != 0:
            yield_str = ', '.join(input_.name for input_ in diagram.inputs.sort()) + ' = ' + yield_str
        if enable_output and len(diagram.outputs) != 0:
            yield_str += ', '.join(output.name for output in diagram.outputs.sort())
        return yield_str


class Executor(base_runner.BaseExecutor):

    def __init__(self, name: str, evaluators: Generator, input_order):

        super().__init__(name, evaluators)

        next(self.evaluators)  # Initialize system
        self.input_order = input_order  # Order in which the inputs are entered in the system

    def run(self, inputs=None):

        if inputs is None:
            return self.evaluators.send()
        sys_inputs = [inputs[var] for var in self.input_order]  # Pass inputs in the order the system requires it
        return self.evaluators.send(sys_inputs)


class Organizer(base_runner.BaseOrganizer):

    def map_component(self, comp):

        self.ordered_comps.append(comp)
