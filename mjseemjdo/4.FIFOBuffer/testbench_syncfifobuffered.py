#!/usr/bin/env python3

from amaranth.sim import *
from amaranth.lib.fifo import *

async def testbench(ctx):
    test_data = [ 3, 2, 7, 6, 8, 1, 0, 2, 4, 0]

    ctx.set(dut.w_en, 1) # enable write

    for idx, data in enumerate(test_data):
        if ctx.get(dut.w_rdy):
            ctx.set(dut.w_data, data)
            await ctx.tick()

    ctx.set(dut.w_en, 0) # disable write

    assert ctx.get(dut.w_rdy) == 0, (f"Failed! Buffer is full but it`s not")
    assert ctx.get(dut.r_rdy) == 1, (f"Failed! Buffer could read but it`s not")

    read_buf = []

    ctx.set(dut.r_en, 1) # enable read

    for idx in range(len(test_data)):
        read_buf.append(ctx.get(dut.r_data))
        await ctx.tick()

    ctx.set(dut.r_en, 0) # disable read

    assert ctx.get(dut.w_rdy) == 1, (f"Failed! Buffer is empty could write but it`s not")
    assert ctx.get(dut.r_rdy) == 0, (f"Failed! Buffer is empty could`t read but it`s not")

    if read_buf == test_data:
        print(f"Test Pass! {read_buf}")


if __name__ == "__main__":
    dut = SyncFIFOBuffered(width=8, depth=10)

    sim = Simulator(dut)
    sim.add_clock(Period(MHz=1))
    sim.add_testbench(testbench)
    with sim.write_vcd("SyncFIFOBuffered.vcd"):
        sim.run()
