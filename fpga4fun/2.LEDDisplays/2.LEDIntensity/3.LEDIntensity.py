#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class LEDPWM(Elaboratable):
    def __init__(self, width=16):
        self.led = Signal()
        self.pwm_input = Signal(4)

    def elaborate(self, platform):
        m = Module()

        pwm = Signal(5)
        m.d.sync += pwm.eq(pwm[0:4] + self.pwm_input)

        m.d.comb += self.led.eq(pwm[4])

        return m

class LEDPWMTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.led_pwm = led_pwm = LEDPWM()

        cnt = Signal(24)
        m.d.sync += cnt.eq(cnt + 1)

        intensity = Signal(4)
        m.d.comb += intensity.eq(Mux(cnt[23], cnt[19:23], ~cnt[19:23]))

        led_pin = platform.request("led", 0)

        m.d.comb += [
            led_pin.o.eq(led_pwm.led),
            led_pwm.pwm_input.eq(intensity)
        ]

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(LEDPWMTop(), do_program=True)
