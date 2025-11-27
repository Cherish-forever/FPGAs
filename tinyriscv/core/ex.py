from amaranth import *
from amaranth.lib.wiring import *

class Execute(Component):
    def __init__(self, addr_width=32, cpu_reset_addr=0x00000000):
        self.addr_width = addr_width
        self.cpu_reset_addr = cpu_reset_addr

        super().__init__(Signature({
            "jump": In(JumpBusSignature(addr_width)),
            "hold": In(HoldFlag),
            "pc_o": Out(addr_width)
        }))

    def elaborate(self, platform):
        m = Module()



        return m
