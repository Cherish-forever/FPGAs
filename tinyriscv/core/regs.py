from amaranth import *
from amaranth.lib.wiring import *

class WriteRegSignature(Signature):
    def __init__(self, id_width=5, data_width=32):
        super().__init__({
            "enable": In(1),
            "id": In(id_width),
            "data": In(data_width)
        })

class ReadRegSignature(Signature):
    def __init__(self, id_width=5, data_width=32):
        super().__init__({
            "id": In(id_width),
            "data": Out(data_width)
        })

class Regs(Component):
    def __init__(self, id_width=5, data_width=32):

        self.data_width = data_width
        self.id_width = id_width

        super().__init__(Signature({
            "rd": In(WriteRegSignature(id_width, data_width)),
            "rs1": In(ReadRegSignature(id_width, data_width)),
            "rs2": In(ReadRegSignature(id_width, data_width)),
        }))

    def elaborate(self, platform):
        m = Module()

        # create x0-x31 registers
        regs = Array([Signal(self.data_width, reset=0, name=f"x{i}") for i in range(32)])

        # write rd register
        with m.If(self.rd.enable & (self.rd.id != 0)):
            m.d.sync += regs[self.rd.id].eq(self.rd.data)

        # read rs1
        with m.If(self.rs1.id == 0):
            m.d.comb += self.rs1.data.eq(0)
        with m.Elif((self.rs1.id == self.rd.id) &  self.rd.enable):
            m.d.comb += self.rs1.data.eq(self.rd.data)
        with m.Else():
            m.d.comb += self.rs1.data.eq(regs[self.rs1.id])

        # read rs2
        with m.If(self.rs2.id == 0):
            m.d.comb += self.rs2.data.eq(0)
        with m.Elif((self.rs2.id == self.rd.id) & self.rd.enable):
            m.d.comb += self.rs2.data.eq(self.rd.data)
        with m.Else():
            m.d.comb += self.rs2.data.eq(regs[self.rs2.id])

        return m
