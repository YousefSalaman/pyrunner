"""
A namespace to store the executor objects.

This guarantees all the executors can be found in one place and can be called
when needed by any script when running a custom Executor object.
"""


_POOL = {}  # Storage for executor objects


def add(name, executor_obj):
    """Register an executor object/system in executor pool."""

    if name in _POOL:
        raise NameError("A system by the of '{}' has already been registered".format(name))
    _POOL[name] = executor_obj


def run(name, inputs):
    """Run an executor object/system from the executor pool."""

    executor = _POOL.get(name)
    if executor is None:
        raise NameError("A system by the name of '{}' has not been registered".format(name))
    return executor.run(inputs)
