#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class LEDBlink(Elaboratable):
    def __init__(self, width=16):
        self.led = Signal()

    def elaborate(self, platform):
        m = Module()

        cnt = Signal(24)
        m.d.sync += cnt.eq(cnt + 1)

        m.d.comb += self.led.eq(cnt[23])

        return m

class LEDBlinkTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.led_blink = led_blink = LEDBlink()

        led_pin = platform.request("led", 0)

        m.d.comb += led_pin.o.eq(led_blink.led)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(LEDBlinkTop(), do_program=True)
