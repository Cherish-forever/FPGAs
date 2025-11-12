#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class Decoder4x(Elaboratable):
    def __init__(self, width=16):
        self.quad_a = Signal()
        self.quad_b = Signal()
        self.cnt = Signal(width)
        self.direction = Signal()

    def elaborate(self, platform):
        m = Module()

        quad_a_delayed = Signal(3)
        quad_b_delayed = Signal(3)

        m.d.sync += [
            quad_a_delayed.eq(Cat(quad_a_delayed[0:2], self.quad_a)),
            quad_b_delayed.eq(Cat(quad_b_delayed[0:2], self.quad_b)),
        ]

        count_enable = Signal()
        m.d.comb += [
            count_enable.eq(quad_a_delayed[1] ^ quad_a_delayed[2] ^ quad_b_delayed[1] ^ quad_b_delayed[2]),
            self.direction.eq(quad_a_delayed[1] ^ quad_b_delayed[2])
        ]

        with m.If(count_enable):
            with m.If(self.direction):
                m.d.sync += self.cnt.eq(self.cnt + 1)
            with m.Else():
                m.d.sync += self.cnt.eq(self.cnt - 1)

        return m

class Decoder4xTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.decode_4x = decode_4x = Decoder4x()

        leds = [platform.request("led", i) for i in range(6)]

        for i, led in enumerate(leds):
            m.d.comb += led.o.eq(decode_4x.cnt[i])

        quad_a = platform.request("button", 0)
        quad_b = platform.request("button", 1)

        m.d.comb += [
            decode_4x.quad_a.eq(quad_a.i),
            decode_4x.quad_b.eq(quad_b.i),
        ]

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(Decoder4xTop(), do_program=True)
