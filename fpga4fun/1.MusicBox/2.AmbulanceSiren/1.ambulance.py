#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class AmbulanceSiren(Elaboratable):
    def __init__(self, clkdivider):
        self.speaker = Signal()
        self.clkdivider = clkdivider

    def elaborate(self, platform):
        m = Module()

        tone = Signal(24)
        m.d.sync += tone.eq(self.tone + 1)

        counter = Signal(15)
        with m.If(self.counter == 0):
            m.d.sync += counter.eq(Mux(tone[23], self.clkdivider - 1, self.clkdivider // 2 - 1))
        with m.Else():
            m.d.sync += counter.eq(self.counter - 1)

        with m.If(counter == 0):
            m.d.sync += self.speaker.eq(~self.speaker)

        return m

class AmbulanceSirenTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        clk_freq = 27_000_000
        base_freq = 440
        clkdivider = clk_freq // base_freq // 2

        m.submodules.ambulance_siren = ambulance_siren = AmbulanceSiren(clkdivider=clkdivider)

        ambulance_siren_pin = platform.request("led", 0)

        m.d.comb += ambulance_siren_pin.o.eq(ambulance_siren.speaker)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(AmbulanceSirenTop(), do_program=True)
