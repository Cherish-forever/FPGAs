from migen import *
from migen.fhdl import verilog

class WaterLed(Module):
    def __init__(self, width):
        self.ios = set()

        self.counter = Signal(max=width)
        self.leds = Signal(width)
        self.reset_n = ResetSignal()

        self.sync += [
            If(~self.reset_n,
               self.counter.eq(0),
               self.leds.eq((1 << width) - 1)
            ).Else(
                self.counter.eq(self.counter + 1),
                If(self.counter == width -1,
                   self.leds.eq(~(1 << 0))
                ).Else (
                    self.leds.eq(self.leds << 1)
                )
            )
        ]

        self.ios.add(self.leds)
        self.ios.add(self.reset_n)

if __name__ == "__main__":
    water_led = WaterLed(width=8)
    print(verilog.convert(water_led, ios=water_led.ios))



