from amaranth import *
from amaranth.lib.wiring import *

from isa import HoldFlag


class JumpBusSignature(Signature):
    def __init__(self, addr_width=32):
        super().__init__({
            "enable": In(1),
            "target": In(addr_width)
        })

class ProgramCounter(Component):
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

        # create pc register
        pc_reg = Signal(self.addr_width, reset=self.cpu_reset_addr)

        with m.If(self.jump.enable): # jump
            m.d.sync += pc_reg.eq(self.jump.target)
        with m.Elif(self.hold >= HoldFlag.HOLD_PC): # hold
            m.d.sync += pc_reg.eq(pc_reg)
        with m.Else(): # output
            m.d.sync += pc_reg.eq(pc_reg + 4)

        m.d.comb += self.pc_o.eq(pc_reg)

        return m
