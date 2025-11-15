#!/usr/bin/env python3

from seven_segment import SevenSegment

from amaranth import *

from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class SevenSegmentTop(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        m.submodules.seven_segment = seven_segment = SevenSegment()

        count = Signal(27)

        m.d.sync += count.eq(count + 1)

        number_in = Signal(4)

        count_max = (1 << count.shape().width -1)
        m.d.sync += number_in.eq(Mux(count == count_max, number_in + 1, number_in))

        segments = [platform.request("led", i) for i in range(6)]

        for idx, seg in enumerate(segments):
            m.d.comb += seg.o.eq(seven_segment.output[idx])

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(SevenSegmentTop(), do_program=True)
