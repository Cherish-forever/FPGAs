#!/usr/bin/env python3

from uart import UART

from amaranth import *

from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class UARTTop(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        m.submodules.uart = uart = UART(divisor=234)

        uart_interface = platform.request("uart", 0)
        m.d.comb += [
            uart_interface.tx.o.eq(uart.tx_o),
            uart.rx_i.eq(uart_interface.rx.i),
            uart.tx_data.eq(uart.rx_data),
        ]

        can_forward = uart.rx_rdy & uart.tx_ack
        m.d.comb += [
            uart.tx_rdy.eq(can_forward),
            uart.rx_ack.eq(can_forward)
        ]

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(UARTTop(), do_program=True)
