
import os
import importlib
from glob import glob

import pyrunner


def find_module(module_name, package):
    """Get module object from within pyrunner source.

    It returns the module object along with its name."""

    pyrunner_path = os.path.dirname(pyrunner.__file__)
    modules = glob(os.path.join(pyrunner_path, package, "*.py"))
    for module in modules:
        if module_name in module:
            module = os.path.basename(module).replace(".py", "")
            return importlib.import_module("pyrunner.{}.{}".format(package, module)), module
    raise ModuleNotFoundError("No runner could be found using the name {}".format(module_name))
