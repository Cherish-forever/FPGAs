#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class SimpleBeep(Elaboratable):
    def __init__(self, width=16):
        self.speaker = Signal()

    def elaborate(self, platform):
        m = Module()

        counter = Signal(16)
        m.d.sync += counter.eq(counter + 1)
        m.d.comb += self.speaker.eq(counter[-1])

        return m

class SimpleBeepTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.simple_beep = simple_beep = SimpleBeep()

        speaker_pin = platform.request("led", 0)

        m.d.comb += speaker_pin.o.eq(simple_beep.speaker)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(SimpleBeepTop(), do_program=True)
