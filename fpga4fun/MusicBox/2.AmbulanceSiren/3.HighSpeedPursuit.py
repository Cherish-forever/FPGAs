#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class HighSpeedPursuit(Elaboratable):
    def __init__(self):
        self.speaker = Signal()

    def elaborate(self, platform):
        m = Module()

        tone = Signal(28)
        m.d.sync += tone.eq(tone + 1)

        fastsweep = Signal(7)
        m.d.comb += fastsweep.eq(Mux(tone[22], tone[15:22], ~tone[15:22]))

        slowsweep = Signal(7)
        m.d.comb += slowsweep.eq(Mux(tone[25], tone[18:25], ~tone[18:25]))

        clkdivider = Signal(15)
        m.d.comb += clkdivider.eq(Cat(Const(0b01, 2),
                                      Mux(tone[27], slowsweep, fastsweep),
                                      Const(0b000000, 6)))

        counter = Signal(15)
        with m.If(counter == 0):
            m.d.sync += counter.eq(clkdivider)
        with m.Else():
            m.d.sync += counter.eq(counter - 1)

        with m.If(counter == 0):
            m.d.sync += self.speaker.eq(~self.speaker)

        return m

class HighSpeedPursuitTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.high_speed_pursuit = high_speed_pursuit = HighSpeedPursuit()

        high_speed_pursuit_pin = platform.request("led", 0)

        m.d.comb += high_speed_pursuit_pin.o.eq(high_speed_pursuit.speaker)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(HighSpeedPursuitTop(), do_program=True)
