from amaranth import *
from amaranth.lib.wiring import *
from hold import HoldFlag

class ProgramCounter(Component):
    def __init__(self, inst_addr_bus=32, cpu_reset_addr=0x00000000):
        self.inst_addr_bus = inst_addr_bus
        self.cpu_reset_addr = cpu_reset_addr

        super().__init__(Signature({
            "jump_flag_i": In(1),
            "jump_addr_i": In(inst_addr_bus),
            "hold_flag_i": In(HoldFlag),
            "jtag_reset_flag_i": In(1),
            "pc_o": Out(inst_addr_bus)
        }))

    def elaborate(self, platform):
        m = Module()

        pc_reg = Signal(self.inst_addr_bus, reset=self.cpu_reset_addr)

        with m.If(self.jtag_reset_flag_i):
            m.d.sync += pc_reg.eq(self.cpu_reset_addr)
        with m.Else():
            with m.If(self.jump_flag_i):
                m.d.sync += pc_reg.eq(self.jump_addr_i)
            with m.Else():
                with m.If(self.hold_flag_i >= HoldFlag.HOLD_PC):
                    m.d.sync += pc_reg.eq(pc_reg)
                with m.Else():
                    m.d.sync += pc_reg.eq(pc_reg + 4)

        m.d.comb += self.pc_o.eq(pc_reg)

        return m
