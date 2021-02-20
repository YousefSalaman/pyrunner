"""
This package contains runner objects. These serve as wrappers to a set of
functions/system. The main purpose of these objects is to simplify code that
run different calculations and require different set-ups. External code that
call these objects don't need to worry about how to run a system since the
set-ups and functions to run a system are contained within the runner objects
and these can be ran indirectly through the method runSystem method.
"""

available_runners = frozenset(["seq", "para"])  # This is used for verification. Add any runner here

__all__ = [runner + "_runner" for runner in available_runners]

