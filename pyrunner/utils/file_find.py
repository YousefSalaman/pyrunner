
import os
import pathlib
import importlib
from glob import glob


# TODO: find_module might change in what it needs to find if I make this into an official package

def find_module(module_name, package):
    """Get module object from within pyrunner source."""

    pyrunner_path = get_pyrunner_src_path()

    modules = glob(os.path.join(pyrunner_path, package, "*.py"))
    for module in modules:
        if module_name in module:
            module = os.path.basename(module).replace(".py", "")
            return importlib.import_module(f"pyrunner.pyrunner.{package}.{module}")
    raise ModuleNotFoundError(f"No runner could be found using the name {module_name}")


# TODO: This might not be needed if install the package locally

def get_pyrunner_src_path():
    """Get the path for the pyrunner source package."""

    diagram_path = pathlib.Path(__file__)  # Get the path for the current file
    for ancestor_path in diagram_path.parents:
        if "pyrunner" == os.path.basename(ancestor_path):
            return str(ancestor_path)
