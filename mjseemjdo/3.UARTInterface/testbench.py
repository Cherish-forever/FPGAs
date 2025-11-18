#!/usr/bin/env python3

from uart import UART

from amaranth.sim import *

uart = UART(divisor=5)

# changed return a tuple
async def testbench_loopback(ctx):            # construct a loopback
    async for val, in ctx.changed(uart.tx_o): # when uart.tx_o changed
        ctx.set(uart.rx_i, val)               # set to uart rx_i

async def testbench_transceiver(ctx):
    test_messages = [
        "Helloworld",
        "1234567890ABCDEFGHIGKLMNOPQRSTUVWXYZ",
        "UART Testing!\n"
    ]

    for message in test_messages:
        send_chars = []
        received_chars = []

        for char in message:
            while not ctx.get(uart.tx_ack):  # wait tx idle mode
                await ctx.tick()

            send_chars.append(char)
            ctx.set(uart.tx_data, ord(char)) # load char to tx_data
            ctx.set(uart.tx_rdy, 1)          # ready to send
            await ctx.tick()                 # pass one tick
            ctx.set(uart.tx_rdy, 0)          # clean ready to send

            while not ctx.get(uart.tx_ack):  # wait tx idle mode
                await ctx.tick()

            if (ctx.get(uart.rx_rdy)):       # received ready
                rx_data = ctx.get(uart.rx_data) # get rx_data
                rchar = chr(rx_data)
                received_chars.append(rchar)
                ctx.set(uart.rx_ack, 1)      # confim rx_ack
                await ctx.tick()
                ctx.set(uart.rx_ack, 0)      # clean rx_ack

                rx_err = ctx.get(uart.rx_err)
                rx_ovf = ctx.get(uart.rx_ovf)

                if (rx_err):
                    print(f"Receive {received_chars} rx 0x{rx_data:02x} error")

                if (rx_ovf):
                    print(f"Receive {received_chars} rx 0x{rx_data:02x} overflow")

        send_str = ''.join(send_chars)
        received_str = ''.join(received_chars)
        if send_str == received_str:
            print(f"Test Pass! Send: {send_str} Received: {received_str}")
        else:
            print(f"Test Failed! Send: {send_str} Received: {received_str}")
    return

if __name__ == "__main__":
    sim = Simulator(uart)
    sim.add_clock(Period(MHz=1))
    sim.add_testbench(testbench_loopback, background=True) # run in backround
    sim.add_testbench(testbench_transceiver)
    with sim.write_vcd("UART.vcd"):
        sim.run()
