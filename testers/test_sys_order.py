
import Simupynk.components as comps
from Simupynk.components.systems import BaseSubsystem
from Simupynk.components.systems.diagram import BlockDiagram


class OrderedSystem(BaseSubsystem):

    has_init_cond = comps.generate_has_init_cond(False)

    input_info = comps.generate_input_info(None)

    output_info = comps.generate_output_info(None)

    parameter_info = comps.generate_parameter_info(None)

    default_name = comps.generate_default_name("test_sys")


class TestCompInitCondTrue(comps.BaseComponent):

    has_init_cond = comps.generate_has_init_cond(True)

    input_info = comps.generate_input_info(None)

    output_info = comps.generate_output_info(None)

    parameter_info = comps.generate_parameter_info(None)

    default_name = comps.generate_default_name("init_cond_true")

    def generate_component_string(self):

        print("Just a test")


class TestCompInitCondFalse(comps.BaseComponent):

    has_init_cond = comps.generate_has_init_cond(False)

    input_info = comps.generate_input_info(None)

    output_info = comps.generate_output_info(None)

    parameter_info = comps.generate_parameter_info(None)

    default_name = comps.generate_default_name("init_cond_false")

    def generate_component_string(self):

        print("Just a test")


if __name__ == "__main__":

    # This should give me a ModuleNotFoundError since "error" is not one of the available runners
    # err_sys = OrderedSystem(name="err_sys", runner_name="error")

    # Main systems for test
    seq_sys = BlockDiagram("seq_sys", "seq")
    para_sys = BlockDiagram("para_sys", "para")

    a = TestCompInitCondFalse(seq_sys, 'a')
    a1 = TestCompInitCondTrue(seq_sys, 'a1')
    a2 = TestCompInitCondFalse(seq_sys, 'a2')
    b = TestCompInitCondFalse(seq_sys, 'b')
    b1 = TestCompInitCondFalse(seq_sys, 'b1')
    b2 = TestCompInitCondFalse(seq_sys, 'b2')
    b3 = TestCompInitCondFalse(seq_sys, 'b3')
    c = TestCompInitCondFalse(seq_sys, 'c')
    d = TestCompInitCondFalse(seq_sys, 'd')
    e = TestCompInitCondFalse(seq_sys, 'e')
    f = TestCompInitCondTrue(seq_sys, 'f')
    f1 = TestCompInitCondTrue(seq_sys, 'f1')
    f2 = TestCompInitCondFalse(seq_sys, 'f2')
    g = TestCompInitCondFalse(seq_sys, 'g')
    h = TestCompInitCondFalse(seq_sys, 'h')
    i = TestCompInitCondFalse(seq_sys, 'i')
    j = TestCompInitCondTrue(seq_sys, 'j')
    k = TestCompInitCondFalse(seq_sys, 'k')

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

    a = TestCompInitCondFalse(para_sys, 'a')
    a1 = TestCompInitCondTrue(para_sys, 'a1')
    a2 = TestCompInitCondFalse(para_sys, 'a2')
    b = TestCompInitCondFalse(para_sys, 'b')
    b1 = TestCompInitCondFalse(para_sys, 'b1')
    b2 = TestCompInitCondFalse(para_sys, 'b2')
    b3 = TestCompInitCondFalse(para_sys, 'b3')
    c = TestCompInitCondFalse(para_sys, 'c')
    d = TestCompInitCondFalse(para_sys, 'd')
    e = TestCompInitCondFalse(para_sys, 'e')
    f = TestCompInitCondTrue(para_sys, 'f')
    f1 = TestCompInitCondTrue(para_sys, 'f1')
    f2 = TestCompInitCondFalse(para_sys, 'f2')
    g = TestCompInitCondFalse(para_sys, 'g')
    h = TestCompInitCondFalse(para_sys, 'h')
    i = TestCompInitCondFalse(para_sys, 'i')
    j = TestCompInitCondTrue(para_sys, 'j')
    k = TestCompInitCondFalse(para_sys, 'k')

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

    a = TestCompInitCondFalse(para_sys, 'a')
    b = TestCompInitCondFalse(para_sys, 'b')
    c = OrderedSystem(para_sys, name='c')
    d = TestCompInitCondFalse(para_sys, 'd')
    e = TestCompInitCondFalse(para_sys, 'e')
    f = TestCompInitCondTrue(para_sys, 'f')
    g = TestCompInitCondFalse(para_sys, 'g')
    h = TestCompInitCondFalse(para_sys, 'h')
    i = TestCompInitCondFalse(para_sys, 'i')
    j = TestCompInitCondTrue(para_sys, 'j')
    k = TestCompInitCondFalse(para_sys, 'k')

    l = TestCompInitCondFalse(c, 'l')
    m = TestCompInitCondFalse(c, 'm')
    n = TestCompInitCondFalse(c, 'n')
    o = TestCompInitCondFalse(c, 'o')
    p = TestCompInitCondTrue(c, 'p')
    q = TestCompInitCondFalse(c, 'q')

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
