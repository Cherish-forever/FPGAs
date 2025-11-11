#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class LED7Seg(Elaboratable):
    def __init__(self, width=16):
        self.segs = Signal(8)

    def elaborate(self, platform):
        m = Module()

        cnt = Signal(24)
        m.d.sync += cnt.eq(cnt + 1)

        cntovf = Signal()
        m.d.comb += cntovf.eq(cnt.all())

        bcd_new = Signal(4)
        bcd_old = Signal(4)

        with m.If(cntovf):
            with m.If(bcd_new == 9):
                m.d.sync += bcd_new.eq(0)
            with m.Else():
                m.d.sync += bcd_new.eq(bcd_new + 1)

        with m.If(cntovf):
            m.d.sync += bcd_old.eq(bcd_new)

        pwm = Signal(5)
        pwm_input = Signal(4)
        m.d.comb += pwm_input.eq(cnt[19:23])
        m.d.sync += pwm.eq(pwm[0:4] + pwm_input)

        bcd = Signal(4)
        with m.If(cnt[23] | pwm[4]):
            m.d.comb += bcd.eq(bcd_new)
        with m.Else():
            m.d.comb += bcd.eq(bcd_old)

        seven_seg = Signal(8)
        with m.Switch(bcd):
            with m.Case(0):
                m.d.comb += seven_seg.eq(Const(0b11111100, 8))
            with m.Case(1):
                m.d.comb += seven_seg.eq(Const(0b01100000, 8))
            with m.Case(2):
                m.d.comb += seven_seg.eq(Const(0b11011010, 8))
            with m.Case(3):
                m.d.comb += seven_seg.eq(Const(0b11110010, 8))
            with m.Case(4):
                m.d.comb += seven_seg.eq(Const(0b01100110, 8))
            with m.Case(5):
                m.d.comb += seven_seg.eq(Const(0b10110110, 8))
            with m.Case(6):
                m.d.comb += seven_seg.eq(Const(0b10111110, 8))
            with m.Case(7):
                m.d.comb += seven_seg.eq(Const(0b11100000, 8))
            with m.Case(8):
                m.d.comb += seven_seg.eq(Const(0b11111110, 8))
            with m.Case(9):
                m.d.comb += seven_seg.eq(Const(0b11110110, 8))

        m.d.comb += self.segs.eq(seven_seg)

        return m

class SmoothCounterTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.led_7seg = led_7seg = LED7Seg()

        leds = [platform.request("led", i) for i in range(6)]

        for i, led in enumerate(leds):
            m.d.comb += led.o.eq(led_7seg.segs[i])

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(SmoothCounterTop(), do_program=True)
