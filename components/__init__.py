"""
This package contains all the components of the Simupynk system.
"""

__all__ = ["math_op", "sources", "systems"]

import Simupynk.components.math_op as math_op
import Simupynk.components.sources as sources
import Simupynk.components.systems as systems
from .systems.base_sys import BaseSystem, BaseSubsystem
from .base_comp import (BaseComponent, generate_default_name, generate_input_info,
                        generate_output_info, generate_parameter_info, generate_has_init_cond)
