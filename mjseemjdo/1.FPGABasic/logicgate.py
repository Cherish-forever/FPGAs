from amaranth import *
from amaranth.lib.wiring import *

class LogicGate(Component):
    switch1: In(1)
    switch2: In(1)
    leds: Out(6)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            self.leds[0].eq(self.switch1 & self.switch2),    # AND
            self.leds[1].eq(~(self.switch1 & self.switch2)), # NAND
            self.leds[2].eq(self.switch1 | self.switch2),    # OR
            self.leds[3].eq(~(self.switch1 | self.switch2)), # NOR
            self.leds[4].eq(self.switch1 ^ self.switch2),    # XOR
            self.leds[5].eq(~(self.switch1 ^ self.switch2)), # NOR
        ]

        return m
