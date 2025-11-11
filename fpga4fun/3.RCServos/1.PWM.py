#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class PWM(Elaboratable):
    def __init__(self, clkdiv):
        self.output = Signal()
        self.position = Signal(8)
        self.clkdiv = clkdiv

    def elaborate(self, platform):
        m = Module()

        clk_count = Signal(7)
        clk_tick = Signal()

        m.d.sync += clk_tick.eq(clk_count == self.clkdiv -2)

        with m.If(clk_tick):
            m.d.sync += clk_count.eq(0)
        with m.Else():
            m.d.sync += clk_count.eq(clk_count + 1)

        pulse_count = Signal(12)
        with m.If(clk_tick):
            m.d.sync += pulse_count.eq(pulse_count + 1)

        rcservo_position = Signal(8)
        with m.If(pulse_count == 0):
            m.d.sync += rcservo_position.eq(self.position)

        with m.If(pulse_count < Cat(Const(0b0001, 4), rcservo_position)):
            m.d.sync += self.output.eq(1)
        with m.Else():
            m.d.sync += self.output.eq(0)

        return m

class PWMTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.pwm = pwm = PWM(98)

        led_pin = platform.request("led", 0)

        m.d.comb += led_pin.o.eq(pwm.output)

        cnt = Signal(20)
        m.d.sync += cnt.eq(cnt + 1)

        with m.If(cnt == 0):
            m.d.sync += pwm.position.eq(pwm.position + 1)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(PWMTop(), do_program=True)
