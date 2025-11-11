#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class PoloceSiren(Elaboratable):
    def __init__(self):
        self.speaker = Signal()

    def elaborate(self, platform):
        m = Module()

        tone = Signal(23)
        m.d.sync += tone.eq(tone + 1)

        ramp = Signal(7)
        m.d.comb += ramp.eq(Mux(tone[22], tone[15:21], ~tone[15:21]))

        clkdivider = Signal(15)
        m.d.comb += clkdivider.eq(Cat(Const(0b01, 2), ramp, Const(0b000000, 6)))

        counter = Signal(15)
        with m.If(counter == 0):
            m.d.sync += counter.eq(clkdivider)
        with m.Else():
            m.d.sync += counter.eq(counter - 1)

        with m.If(counter == 0):
            m.d.sync += self.speaker.eq(~self.speaker)

        return m

class PoloceSirenTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.poloce_siren = poloce_siren = PoloceSiren()

        poloce_siren_pin = platform.request("led", 0)

        m.d.comb += poloce_siren_pin.o.eq(poloce_siren.speaker)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(PoloceSirenTop(), do_program=True)
