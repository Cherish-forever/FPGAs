from amaranth import *
from amaranth.lib.wiring import *
from amaranth.lib.enum import Enum

class JumpBusSignature(Signature):
    def __init__(self, addr_width=32):
        super().__init__({
            "enable": In(1),
            "target": In(addr_width)
        })

class HoldFlag(Enum, shape=unsigned(3)):
    """Hold flag"""
    HOLD_NONE=0
    HOLD_PC = 1
    HOLD_IF = 2
    HOLD_ID = 3

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

        pc_reg = Signal(self.addr_width, reset=self.cpu_reset_addr)

        with m.If(self.jump.enable):
            m.d.sync += pc_reg.eq(self.jump.target)
        with m.Else():
            with m.If(self.hold >= HoldFlag.HOLD_PC):
                m.d.sync += pc_reg.eq(pc_reg)
            with m.Else():
                m.d.sync += pc_reg.eq(pc_reg + 4)

        m.d.comb += self.pc_o.eq(pc_reg)

        return m
