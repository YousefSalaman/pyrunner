
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

    a1.inputs.update(a)
    a2.inputs.update(a1)
    b1.inputs.update(b)
    b2.inputs.update(b1)
    b3.inputs.update(b2)
    c.inputs.update(a2, b3)
    d.inputs.update(c, g)
    e.inputs.update(i)
    f.inputs.update(e)
    f1.inputs.update(f)
    f2.inputs.update(f1)
    g.inputs.update(f2)
    h.inputs.update(d, k)
    i.inputs.update(h)
    j.inputs.update(i)
    k.inputs.update(j)

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

    a1.inputs.update(a)
    a2.inputs.update(a1)
    b1.inputs.update(b)
    b2.inputs.update(b1)
    b3.inputs.update(b2)
    c.inputs.update(a2, b3)
    d.inputs.update(c, g)
    e.inputs.update(i)
    f.inputs.update(e)
    f1.inputs.update(f)
    f2.inputs.update(f1)
    g.inputs.update(f2)
    h.inputs.update(d, k)
    i.inputs.update(h)
    j.inputs.update(i)
    k.inputs.update(j)

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

    c.inputs.update(a, b)
    d.inputs.update(c, g)
    e.inputs.update(i)
    f.inputs.update(e)
    g.inputs.update(f)
    h.inputs.update(d, k)
    i.inputs.update(h)
    j.inputs.update(i)
    k.inputs.update(j)

    m.inputs.update(l, q)
    n.inputs.update(m)
    o.inputs.update(n)
    p.inputs.update(n)
    q.inputs.update(p)

    para_sys.build_diagram()
