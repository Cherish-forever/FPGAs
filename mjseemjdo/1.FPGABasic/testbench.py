#!/usr/bin/env python3

from logicgate import LogicGate

from amaranth.sim import *

async def testbench(ctx):
    test_vectors = [
        (0, 0, 0b101010),
        (0, 1, 0b010110),
        (1, 0, 0b010110),
        (1, 1, 0b100101)
    ]

    for sw1, sw2, excepted in test_vectors:
        ctx.set(dut.switch1, sw1)
        ctx.set(dut.switch2, sw2)
        await ctx.delay(1e-6)
        leds_val = ctx.get(dut.leds)
        assert leds_val == excepted, (f"Input({sw1}, {sw2}): Got {leds_val:06b}, excepted {excepted:06b}")
        print(f"Test Pass: Input({sw1}, {sw2}) -> Output: {leds_val:06b}")

if __name__ == "__main__":
    dut = LogicGate()

    sim = Simulator(dut)
    sim.add_testbench(testbench)
    with sim.write_vcd("LogicGate.vcd"):
        sim.run()
