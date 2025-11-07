#!/usr/bin/env python3

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io
from amaranth_boards.tang_nano_9k import TangNano9kPlatform

class DivideBy12Array(Elaboratable):
    def __init__(self):
        self.number = Signal(6)
        self.quotient = Signal(3)
        self.remain = Signal(4)

    def elaborate(self, platform):
        m = Module()

        quotient_lut = Array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5])
        remain_lut   = Array([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0])

        high_bits = self.number[2:6]

        m.d.comb += [
            self.quotient.eq(quotient_lut[high_bits]),
            self.remain.eq(Cat(remain_lut[high_bits], self.number[0:2]))
        ]

        return m

class DivideBy12Math(Elaboratable):
    def __init__(self):
        self.number = Signal(6)
        self.quotient = Signal(3)
        self.remain = Signal(4)

    def elaborate(self, platform):
        m = Module()

        high_bits = self.number[2:6]

        m.d.comb += [
            self.quotient.eq(high_bits // 3),
            self.remain.eq(Cat(high_bits % 3, self.number[0:2]))
        ]

        return m

class DivideBy12Switch(Elaboratable):
    def __init__(self):
        self.number = Signal(6)
        self.quotient = Signal(3)
        self.remain = Signal(4)

    def elaborate(self, platform):
        m = Module()

        remain_bit3_bit2 = Signal(2)
        m.d.comb += self.remain.eq(Cat(remain_bit3_bit2, self.number[0:2]))

        with m.Switch(self.number[2:6]):
            with m.Case(0):
                m.d.comb += self.quotient.eq(0)
                m.d.comb += remain_bit3_bit2.eq(0)
            with m.Case(1):
                m.d.comb += self.quotient.eq(0)
                m.d.comb += remain_bit3_bit2.eq(1)
            with m.Case(2):
                m.d.comb += self.quotient.eq(0)
                m.d.comb += remain_bit3_bit2.eq(2)
            with m.Case(3):
                m.d.comb += self.quotient.eq(1)
                m.d.comb += remain_bit3_bit2.eq(0)
            with m.Case(4):
                m.d.comb += self.quotient.eq(1)
                m.d.comb += remain_bit3_bit2.eq(1)
            with m.Case(5):
                m.d.comb += self.quotient.eq(1)
                m.d.comb += remain_bit3_bit2.eq(2)
            with m.Case(6):
                m.d.comb += self.quotient.eq(2)
                m.d.comb += remain_bit3_bit2.eq(0)
            with m.Case(7):
                m.d.comb += self.quotient.eq(2)
                m.d.comb += remain_bit3_bit2.eq(1)
            with m.Case(8):
                m.d.comb += self.quotient.eq(2)
                m.d.comb += remain_bit3_bit2.eq(2)
            with m.Case(9):
                m.d.comb += self.quotient.eq(3)
                m.d.comb += remain_bit3_bit2.eq(0)
            with m.Case(10):
                m.d.comb += self.quotient.eq(3)
                m.d.comb += remain_bit3_bit2.eq(1)
            with m.Case(11):
                m.d.comb += self.quotient.eq(3)
                m.d.comb += remain_bit3_bit2.eq(2)
            with m.Case(12):
                m.d.comb += self.quotient.eq(4)
                m.d.comb += remain_bit3_bit2.eq(0)
            with m.Case(13):
                m.d.comb += self.quotient.eq(4)
                m.d.comb += remain_bit3_bit2.eq(1)
            with m.Case(14):
                m.d.comb += self.quotient.eq(4)
                m.d.comb += remain_bit3_bit2.eq(2)
            with m.Case(15):
                m.d.comb += self.quotient.eq(5)
                m.d.comb += remain_bit3_bit2.eq(0)
            with m.Case():
                m.d.comb += self.quotient.eq(0)
                m.d.comb += remain_bit3_bit2.eq(0)

        return m

class PlayingNotes(Elaboratable):
    def __init__(self):
        self.speaker = Signal()

    def elaborate(self, platform):
        m = Module()

        tone = Signal(28)
        m.d.sync += tone.eq(tone + 1)

        fullnote = tone[22:28]

        octave = Signal(3)
        note = Signal(4)

        m.submodules.divby12 = divby12 = DivideBy12Array()
        m.d.comb += [
            divby12.number.eq(fullnote),
            octave.eq(divby12.quotient),
            note.eq(divby12.remain),
        ]

        clkdivider = Signal(9)

        with m.Switch(note):
            with m.Case(0):
                m.d.comb += clkdivider.eq(512-1)
            with m.Case(1):
                m.d.comb += clkdivider.eq(483-1)
            with m.Case(2):
                m.d.comb += clkdivider.eq(456-1)
            with m.Case(3):
                m.d.comb += clkdivider.eq(431-1)
            with m.Case(4):
                m.d.comb += clkdivider.eq(406-1)
            with m.Case(5):
                m.d.comb += clkdivider.eq(384-1)
            with m.Case(6):
                m.d.comb += clkdivider.eq(362-1)
            with m.Case(7):
                m.d.comb += clkdivider.eq(342-1)
            with m.Case(8):
                m.d.comb += clkdivider.eq(323-1)
            with m.Case(9):
                m.d.comb += clkdivider.eq(304-1)
            with m.Case(10):
                m.d.comb += clkdivider.eq(287-1)
            with m.Case(11):
                m.d.comb += clkdivider.eq(271-1)
            with m.Case():
                m.d.comb += clkdivider.eq(0)

        counter_note = Signal(9)

        with m.If(counter_note == 0):
            m.d.sync += counter_note.eq(clkdivider)
        with m.Else():
            m.d.sync += counter_note.eq(counter_note - 1)

        counter_octave = Signal(8)
        octave_values = Array([255, 127, 63, 31, 15, 7, 7, 7])

        with m.If(counter_note == 0):
            with m.If(counter_octave == 0):
                m.d.sync += counter_octave.eq(octave_values[octave])
            with m.Else():
                m.d.sync += counter_octave.eq(counter_octave - 1)

        with m.If((counter_note==0) & (counter_octave==0)):
            m.d.sync += self.speaker.eq(~self.speaker)

        return m

class PlayingNotesTop(Elaboratable):
    """Measure the output frequency of pin 10 using an oscilloscope to be 27M / 65536 = 410.9873KHZ """
    def elaborate(self, platform):
        m = Module()

        m.submodules.playing_notes = playing_notes = PlayingNotes()

        playing_notes_pin = platform.request("led", 0)

        m.d.comb += playing_notes_pin.o.eq(playing_notes.speaker)

        return m

if __name__ == "__main__":
    TangNano9kPlatform().build(PlayingNotesTop(), do_program=True)
