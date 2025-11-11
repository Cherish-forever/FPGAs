#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class LEDHalfLit(Elaboratable):
    def __init__(self, width=16):
        self.led = Signal()

    def elaborate(self, platform):
        m = Module()

        toggle = Signal()
        m.d.sync += toggle.eq(~toggle)

        m.d.comb += self.led.eq(toggle)

        return m

class LEDHalfLitTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.led_half_lit = led_half_lit = LEDHalfLit()

        led_pin = platform.request("led", 0)

        m.d.comb += led_pin.o.eq(led_half_lit.led)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(LEDHalfLitTop(), do_program=True)
