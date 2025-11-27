from amaranth import *
from amaranth.lib.wiring import *

from isa import *
from regs import RegSignature
from if_id import InstructionSignature

class ExecuteSignature(Signature):
    def __init__(self, addr_width=32):
        super().__init__({
            "i": Out(InstructionSignature().output()),
            "rd":  Out(RegsSignature(id_width, data_width).write()),
            "rs1": In(RegsSignature(id_width, data_width).read()),
            "rs2": In(RegsSignature(id_width, data_width).read()),
        })

class RegsSignature(Signature):
    def __init__(self, addr_width=32):
        super().__init__({
            "rd":  Out(RegsSignature(id_width, data_width).write()),
            "rs1": In(RegsSignature(id_width, data_width).read()),
            "rs2": In(RegsSignature(id_width, data_width).read()),
        }

class InstructionDecode(Component):
    def __init__(self, id_width=5, data_width=32):

        super().__init__(Signature({
            "from_fetch": In(InstructionSignature().output()),
            "to_execute": Out(ExecuteSignature()),
        }))

    def elaborate(self, platform):
        m = Module()

        inst = self.from_fetch.inst

        rd, rs1, rs2 = inst[7:12], inst[15:20], inst[20:25]
        opcode, funct3, rs2, funct7 = inst[0:7], inst[12:15], inst[25:32]

        is_ecall  = (inst == INST_ECALL)
        is_ebreak = (inst == INST_EBREAK)
        is_mret   = (inst == INST_MRET)
        is_sret   = (inst == INST_SRET)
        is_uret   = (inst == INST_URET)
        has_urgent_special_inst = (is_ecall | is_ebreak | is_mret | is_sret | is_uret)

        is_nop     = (inst == INST_NOP)
        is_fence   = (inst == INST_FENCE)
        is_fence_i = (inst == INST_FENCE_I)
        is_wft     = (inst == INST_WFT)
        is_ret     = (inst == INST_RET)
        has_special_inst = (is_nop | is_fence | is_fence_i | is_wft | is_ret)

        with m.If(has_urgent_special_inst):
            pass
        with m.Elif(has_special_inst):
            pass
        with m.Else():
            with m.Switch(opcode):
                with m.Case(Opcode.OP_IMM):
                    with m.Switch(funct3):
                        with m.Case([Funct3.ADDI, Funct3.SLTI, Funct3.SLTIU, Funct3.XORI,
                                     Funct3.ORI, Funct3.ANDI, Funct3.SLLI, Funct3.SRI]):
                            m.d.sync += [
                                self.rd.enable.eq(1),
                                self.rd.id.eq(rd),
                                self.rs1.id.eq(rs1),
                                self.rs2.id.eq(0),
                            ]
                with m.Case(Opcode.OP):
                    with m.If((funct7 == Funct7.ADD) | (funct7 == Funct7.SUB)):
                        with m.Switch(funct3):
                            with Case([Funct3.ADD_SUB, Funct3.SLL, Funct3.SLT, Funct3.SLTU,
                                       Funct3.XOR, Funct3.SR, Funct3.OR, Funct3.AND]):
                                m.d.comb += [
                                    self.rd.enable.eq(1),
                                    self.rd.id.eq(rd),
                                    self.rs1.id.eq(rs1),
                                    self.rs2.id.eq(rs2),
                                ]
                            with m.Default():
                                m.d.comb += [
                                    self.rd.enable.eq(0),
                                    self.rd.id.eq(0),
                                    self.rs1.id.eq(0),
                                    self.rs2.id.eq(0),
                                ]
                    with m.Elif(funct7 == Funct7.MUL):
                        with m.Switch(funct3):
                            with m.Case([Funct3.MUL, Funct3.MULHU, Funct3.MULH, Funct3.MULHSU,]):
                                m.d.comb += [
                                    self.rd.enable.eq(1),
                                    self.rd.id.eq(rd),
                                    self.rs1.id.eq(rs1),
                                    self.rs2.id.eq(rs2),
                                ]
                            with m.Case([Funct3.DIV, Funct3.DIVU, Funct3.REM, Funct3.REMU]):
                                m.d.comb += [
                                    self.rd.enable.eq(0),
                                    self.rd.id.eq(rd),
                                    self.rs1.id.eq(rs1),
                                    self.rs2.id.eq(rs2),
                                ]
                            with m.Default():
                                m.d.comb += [
                                    self.rd.enable.eq(0),
                                    self.rd.id.eq(0),
                                    self.rs1.id.eq(0),
                                    self.rs2.id.eq(0),
                                ]
                    with m.Else():
                        m.d.comb += [
                            self.rd.enable.eq(0),
                            self.rd.id.eq(0),
                            self.rs1.id.eq(0),
                            self.rs2.id.eq(0),
                        ]
                with m.Case(Opcode.LOAD):
                    pass
                with m.Case(Opcode.STORE):
                    pass
                with m.Case(Opcode.BRANCH):
                    pass
                with m.Case(Opcode.JAL):
                    pass
                with m.Case(Opcode.JALR):
                    pass
                with m.Case(Opcode.LUI):
                    pass
                with m.Case(Opcode.AUIPC):
                    pass


        # from_fetch -> to_execute
        m.d.comb += [
            self.to_execute.addr.eq(self.from_fetch.addr),
            self.to_execute.inst.eq(inst),
        ]

        return m
