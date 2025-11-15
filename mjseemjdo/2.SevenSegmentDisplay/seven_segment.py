from amaranth import *
from amaranth.lib.wiring import *

class SevenSegment(Component):
    number_in: In(4)
    output: Out(7)

    def elaborate(self, platform):
        m = Module()

        segments = Array(Const(x, 7) for x in [
            0b1111110, 0b0110000, 0b1101101, 0b1111001,
            0b1011011, 0b1011011, 0b1011111, 0b1110000,
            0b1111111, 0b1110011, 0b1110111, 0b0011111,
            0b1001110, 0b0111101, 0b1001111, 0b1000111
        ])

        m.d.comb += self.output.eq(~segments[self.number_in])

        return m
