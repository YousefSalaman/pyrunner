"""This package contains runner objects.

Their main purpose is to wrap a set of functions, so they can be set up and
ran without the need of knowing the how the code is structured inside these
objects. Runners are composed of three parts:

    - Organizer: This object contains the instructions of how to organize
      each component of a diagram.

    - Builder: This object contains the instructions of how to build the
      set of functions based on the connections of the system.

    - Executer: This object contains the instructions of how to run the
      set of functions based on the connections of the system. This is
      the object that will be returned for users to run.
"""

available_runners = frozenset(["seq", "para"])  # This is used for verification. Add any runner here

__all__ = [runner + "_runner" for runner in available_runners]

