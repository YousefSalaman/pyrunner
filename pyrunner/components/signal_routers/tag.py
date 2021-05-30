from .. import base_comp


class Tag(base_comp.BaseComponent):
    """A proxy component used to transfer data in and out external sources.

    The main feature of this component is that one names this object, so one
    can use that name to read or write information from a system:

    - Reading: When a system needs to read from an external source of data,
      this component needs to be used. The only thing you need to do is you
      need to specify with what name will the data come with by giving the
      component the same name.

      For example, let's say that you run a system that requires an external
      source. This input must be entered in the run method of a runner as a
      dictionary where the key is the name of the input and the value is the
      data you wish to pass to the system. When creating the system, you only
      need to create the tag component with the name of the incoming input
      and pass this as the input to the components that require the external
      source of information.

    - Writing: Unlike reading from an external source, writing to an external
      source does not require this component. For this functionality, you
      specify that the input of this component is the output you wish to send
      to an external source.

      For example, a pyrunner system will output a dictionary with the
      variable names of the components that were specified as outputs in the
      system as keys with their respective values. Since the name of these
      components might not be the same as the output keys an external source
      might expect, you can create a tag component for each of these to match
      the external sources names by putting the key the source expects as the
      name of the tag, putting the key's respective output component as the
      input of the tag component, and putting the tag component as as output
      of the system. This will create an output with the correct names.

      However, you can achieve this effect by naming the output components
      like the external source expects and the output dictionary will have
      the correct variable names.
    """

    default_name = base_comp.generate_default_name("")

    direct_feedthrough = base_comp.generate_direct_feedthrough(True)

    prop_info = base_comp.generate_prop_info(
        {
            "inputs": ({}, {"input"}),
            "outputs": ({}, {}),
            "parameters": ({}, {})
        }
    )

    def __init__(self, sys_obj, name):

        super(Tag, self).__init__(sys_obj, name)

    def generate_code_string(self):

        input_ = self.inputs["input"]
        if input_ is not None:
            self.code_str["Execution"] = "{} = {}".format(self.name, input_.name)
