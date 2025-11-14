#!/usr/bin/env python3

from logicgate import LogicGate

from amaranth import *

from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class LogicGateTop(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        m.submodules.logicgate = logicgate = LogicGate()

        leds = [platform.request("led", i) for i in range(6)]

        for i, led in enumerate(leds):
            m.d.comb += led.o.eq(logicgate.leds[i])

        switch1 = platform.request("button", 0)
        switch2 = platform.request("button", 1)

        m.d.comb += [
            logicgate.switch1.eq(switch1.i),
            logicgate.switch2.eq(switch2.i),
        ]

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(LogicGateTop(), do_program=True)
