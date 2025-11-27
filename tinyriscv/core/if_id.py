from amaranth import *
from amaranth.lib.wiring import *

from isa import INST_NOP, HoldFlag

class InstructionSignature(Signature):
    def __init__(self, addr_width=32, inst_width=32):
        self.addr_width = addr_width
        self.inst_width = inst_width

    def fetch(self):
        return Signature({
            "addr": Out(self.addr_width),
            "inst": In(self.inst_width)
        })

    def output(self):
        return Signature({
            "addr": Out(self.addr_width),
            "inst": Out(self.inst_width)
        })

class InstructionFetch(Component):
    def __init__(self, addr_width=32, inst_width=32):

        super().__init__(Signature({
            "from_memory": In(InstructionSignature(addr_width, inst_width).fetch()),
            "to_decode": Out(InstructionSignature(addr_width, inst_width).output()),
            "hold": In(HoldFlag),
        }))

    def elaborate(self, platform):
        m = Module()

        hold_en = Signal()

        m.d.comb += hold_en.eq(self.hold >= HoldFlag.HOLD_IF)

        m.d.sync += [
            self.to_decode.inst.eq(Mux(hold_en, INST_NOP, self.from_memory.inst)),
            self.to_decode.addr.eq(Mux(hold_en, 0, self.from_memory.addr)),
        ]

        return m
