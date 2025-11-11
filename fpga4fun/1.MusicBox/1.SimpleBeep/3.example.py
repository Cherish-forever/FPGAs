#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class SimpleBeep(Elaboratable):
    def __init__(self, max_count=65535):
        self.speaker = Signal()
        self.max_count = max_count

    def elaborate(self, platform):
        m = Module()

        counter = Signal(16)

        with m.If(counter == self.max_count):
            m.d.sync += counter.eq(0)
        with m.Else():
            m.d.sync += counter.eq(counter + 1)

        with m.If(counter == self.max_count):
            m.d.sync += self.speaker.eq(~self.speaker)

        return m

class SimpleBeepTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 50000 / 2 = 270HZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.simple_beep = simple_beep = SimpleBeep(max_count=50000)

        speaker_pin = platform.request("led", 0)

        m.d.comb += speaker_pin.o.eq(simple_beep.speaker)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(SimpleBeepTop(), do_program=True)
