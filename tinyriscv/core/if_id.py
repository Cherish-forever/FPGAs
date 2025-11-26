from amaranth import *
from amaranth.lib.wiring import *

from pc_reg import HoldFlag
from isa import INST_NOP

class FetchInstructionSignature(Signature):
    def __init__(self, addr_width=32, inst_width=32):
        super().__init__({
            "addr": Out(addr_width),
            "inst": In(inst_width)
        })

class OutputInstructionSignature(Signature):
  def __init__(self, addr_width=32, inst_width=32):
      super().__init__({
            "addr": Out(addr_width),
            "inst": Out(inst_width)
        })

class InstructionFetch(Component):
    def __init__(self, addr_width=32, inst_width=32):

        super().__init__(Signature({
            "fetch": In(FetchInstructionSignature(addr_width, inst_width)),
            "output": In(OutputInstructionSignature(addr_width, inst_width)),
            "hold": In(HoldFlag),
        }))

    def elaborate(self, platform):
        m = Module()

        hold_en = Signal()

        m.d.comb += hold_en.eq(self.hold >= HoldFlag.HOLD_IF)

        m.d.sync += [
            self.output.inst.eq(Mux(hold_en, INST_NOP, self.fetch.inst)),
            self.output.addr.eq(Mux(hold_en, 0, self.fetch.addr)),
        ]

        return m
