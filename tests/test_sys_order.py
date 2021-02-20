
import Simupynk.Simupynk.components as comps
from Simupynk.Simupynk.components.systems import BaseSubsystem
from Simupynk.Simupynk.components.systems import BlockDiagram


class OrderedSystem(BaseSubsystem):

    direct_feedthrough = comps.generate_direct_feedthrough(False)

    input_info = comps.generate_input_info(None)

    output_info = comps.generate_output_info(None)

    parameter_info = comps.generate_parameter_info(None)

    default_name = comps.generate_default_name("test_sys")


class TestCompDirect(comps.BaseComponent):

    direct_feedthrough = comps.generate_direct_feedthrough(False)

    input_info = comps.generate_input_info(None)

    output_info = comps.generate_output_info(None)

    parameter_info = comps.generate_parameter_info(None)

    default_name = comps.generate_default_name("direct")

    def generate_component_string(self):

        print("Just a test")


class TestCompNonDirect(comps.BaseComponent):

    direct_feedthrough = comps.generate_direct_feedthrough(True)

    input_info = comps.generate_input_info(None)

    output_info = comps.generate_output_info(None)

    parameter_info = comps.generate_parameter_info(None)

    default_name = comps.generate_default_name("indirect")

    def generate_component_string(self):

        print("Just a test")


if __name__ == "__main__":

    # This should give me a ModuleNotFoundError since "error" is not one of the available runners
    # err_sys = OrderedSystem(name="err_sys", runner_name="error")

    # Main systems for test
    seq_sys = BlockDiagram("seq_sys", "seq")
    para_sys = BlockDiagram("para_sys", "para")

    a = TestCompNonDirect(seq_sys, 'a')
    a1 = TestCompDirect(seq_sys, 'a1')
    a2 = TestCompNonDirect(seq_sys, 'a2')
    b = TestCompNonDirect(seq_sys, 'b')
    b1 = TestCompNonDirect(seq_sys, 'b1')
    b2 = TestCompNonDirect(seq_sys, 'b2')
    b3 = TestCompNonDirect(seq_sys, 'b3')
    c = TestCompNonDirect(seq_sys, 'c')
    d = TestCompNonDirect(seq_sys, 'd')
    e = TestCompNonDirect(seq_sys, 'e')
    f = TestCompDirect(seq_sys, 'f')
    f1 = TestCompDirect(seq_sys, 'f1')
    f2 = TestCompNonDirect(seq_sys, 'f2')
    g = TestCompNonDirect(seq_sys, 'g')
    h = TestCompNonDirect(seq_sys, 'h')
    i = TestCompNonDirect(seq_sys, 'i')
    j = TestCompDirect(seq_sys, 'j')
    k = TestCompNonDirect(seq_sys, 'k')

    a1.inputs.add(a)
    a2.inputs.add(a1)
    b1.inputs.add(b)
    b2.inputs.add(b1)
    b3.inputs.add(b2)
    c.inputs.add(a2, b3)
    d.inputs.add(c, g)
    e.inputs.add(i)
    f.inputs.add(e)
    f1.inputs.add(f)
    f2.inputs.add(f1)
    g.inputs.add(f2)
    h.inputs.add(d, k)
    i.inputs.add(h)
    j.inputs.add(i)
    k.inputs.add(j)

    seq_sys.build_diagram()

    a = TestCompNonDirect(para_sys, 'a')
    a1 = TestCompDirect(para_sys, 'a1')
    a2 = TestCompNonDirect(para_sys, 'a2')
    b = TestCompNonDirect(para_sys, 'b')
    b1 = TestCompNonDirect(para_sys, 'b1')
    b2 = TestCompNonDirect(para_sys, 'b2')
    b3 = TestCompNonDirect(para_sys, 'b3')
    c = TestCompNonDirect(para_sys, 'c')
    d = TestCompNonDirect(para_sys, 'd')
    e = TestCompNonDirect(para_sys, 'e')
    f = TestCompDirect(para_sys, 'f')
    f1 = TestCompDirect(para_sys, 'f1')
    f2 = TestCompNonDirect(para_sys, 'f2')
    g = TestCompNonDirect(para_sys, 'g')
    h = TestCompNonDirect(para_sys, 'h')
    i = TestCompNonDirect(para_sys, 'i')
    j = TestCompDirect(para_sys, 'j')
    k = TestCompNonDirect(para_sys, 'k')

    a1.inputs.add(a)
    a2.inputs.add(a1)
    b1.inputs.add(b)
    b2.inputs.add(b1)
    b3.inputs.add(b2)
    c.inputs.add(a2, b3)
    d.inputs.add(c, g)
    e.inputs.add(i)
    f.inputs.add(e)
    f1.inputs.add(f)
    f2.inputs.add(f1)
    g.inputs.add(f2)
    h.inputs.add(d, k)
    i.inputs.add(h)
    j.inputs.add(i)
    k.inputs.add(j)

    para_sys.build_diagram()

    para_sys = BlockDiagram("para_sys", "para")

    a = TestCompNonDirect(para_sys, 'a')
    b = TestCompNonDirect(para_sys, 'b')
    c = OrderedSystem(para_sys, name='c')
    d = TestCompNonDirect(para_sys, 'd')
    e = TestCompNonDirect(para_sys, 'e')
    f = TestCompDirect(para_sys, 'f')
    g = TestCompNonDirect(para_sys, 'g')
    h = TestCompNonDirect(para_sys, 'h')
    i = TestCompNonDirect(para_sys, 'i')
    j = TestCompDirect(para_sys, 'j')
    k = TestCompNonDirect(para_sys, 'k')

    l = TestCompNonDirect(c)
    m = TestCompNonDirect(c)
    n = TestCompNonDirect(c)
    o = TestCompNonDirect(c)
    p = TestCompDirect(c)
    q = TestCompNonDirect(c)

    c.inputs.add(a, b)
    d.inputs.add(c, g)
    e.inputs.add(i)
    f.inputs.add(e)
    g.inputs.add(f)
    h.inputs.add(d, k)
    i.inputs.add(h)
    j.inputs.add(i)
    k.inputs.add(j)

    m.inputs.add(l, q)
    n.inputs.add(m)
    o.inputs.add(n)
    p.inputs.add(n)
    q.inputs.add(p)

    para_sys.build_diagram()
