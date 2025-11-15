#!/usr/bin/env python3

from seven_segment import SevenSegment

from amaranth.sim import *

async def testbench(ctx):
    test_list = [
        0b1111110, 0b0110000, 0b1101101, 0b1111001,
        0b1011011, 0b1011011, 0b1011111, 0b1110000,
        0b1111111, 0b1110011, 0b1110111, 0b0011111,
        0b1001110, 0b0111101, 0b1001111, 0b1000111
    ]

    for idx, expected in enumerate(test_list):
        ctx.set(dut.number_in, idx)
        await ctx.delay(1e-6)
        output = ctx.get(dut.output)
        expected_inverted = expected ^ 0b1111111
        assert output == expected_inverted, (f"Input({idx}): Got {output:07b}, excepted {expected_inverted}")
        print(f"Test Pass: Input({idx}) -> Output: {output:07b}")

if __name__ == "__main__":
    dut = SevenSegment()

    sim = Simulator(dut)
    sim.add_testbench(testbench)
    with sim.write_vcd("SevenSegment.vcd"):
        sim.run()
