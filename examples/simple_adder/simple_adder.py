#!/usr/bin/env python

from __future__ import print_function

import os

from pyrunner.components import *
from pyrunner.runners import executors


simple_adder = systems.BlockDiagram("simple_adder", "seq")  # Initialize the block diagram to hold components

# Create components and store them in the block diagram

# Add constant sources
const_1 = sources.Constant(simple_adder, value=3.1415)
const_2 = sources.Constant(simple_adder, value='np.array([1,2,3])')
const_3 = sources.Constant(simple_adder, value=1)

# Add the Sum blocks
adder = math_op.Sum(simple_adder, comp_signs="-+")
adder_1 = math_op.Sum(simple_adder, comp_signs='+--')
adder_2 = math_op.Sum(simple_adder, comp_signs='-')

# Add the inputs to Sums
adder.inputs.add(adder_1, adder_2)
adder_1.inputs.add(const_1, const_2, const_3)
adder_2.inputs.add(const_2)

simple_adder.outputs.add(adder, adder_1)  # Say the "adder" component is the output of the system

# The lines below generate an executable object, called the executor, and you use it by importing
# the executors module and running the run function (shown below)

simple_adder.build()
print(executors.run('simple_adder'))  # Run an iteration of our simple_adder system

# The following creates a python script named 'adder_example.py" with the simple_adder system's
# code. When you run this, the executable object (i.e. the executor) will be stored for later use
# through the run method of the executor

file_path = os.path.join(os.path.dirname(__file__), 'adder_example.py')
simple_adder.build(file_path)  # Creates a file with the code
