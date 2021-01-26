
import Simupynk.components as comps


class TestComp(comps.BaseComponent):

    has_init_cond = comps.HAS_INIT_COND_TRUE

    short_name = comps.generateShortName("t")

    input_lim = comps.generateInputLim((1, 3))  # Input ranges from 1 to 3

    default_name = comps.generateDefaultName("test")

    def generateComponentString(self):

        print("Just a test")
        super().generateComponentString()


if __name__ == "__main__":

    a = TestComp(inputs=[])
    b = TestComp(inputs=[0,1,2,3])  # Should give you an Attribute error for
    a.verifyInputSize()
    b.verifyInputSize()