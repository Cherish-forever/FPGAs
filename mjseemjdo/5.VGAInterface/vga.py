#!/usr/bin/env python3

from amaranth import *
from amaranth.lib import data
from amaranth.lib.wiring import *

class VGASyncPulses(Component):
    def __init__(self, total_cols=800, total_rows=525, active_clos=640, active_row=480):
        self.total_cols  = total_cols # 640 + 16(front) + 96(sync) + 48(back) = 800
        self.total_rows  = total_rows # 480 + 10(front) + 2(sync) + 33(back) = 525
        self.active_clos = active_clos
        self.active_row  = active_row

        super().__init__({
            "hsync_o": OUT(1),
            "vsync_o": OUT(1),
            "col_count_o": OUT(12),
            "row_count_o": OUT(12)
        })

    def elaborate(self, platform):
        m = Module()

        with m.If(self.col_count_o == self.total_cols - 1):
            m.d.sync += self.col_count_o.eq(0)
            with m.If(self.row_count.o == self.total_rows - 1):
                m.d.sync += self.row_count_o.eq(0)
            with m.Else():
                m.d.sync += self.row_count_o.eq(self.row_count_o + 1)
        with m.Else():
            m.d.sync += self.col_count_o.eq(self.col_count_o + 1)

        m.d.comb += [
            self.hsync_o.eq(Mux(self.col_count_o < self.active_clos, 1, 0)),
            self.vsync_o.eq(Mux(self.row_count_o < self.active_row,  1, 0))
        ]

        return m


class SyncToCount(Component):
    def __init__(self, total_cols=800, total_rows=525):
        self.total_cols  = total_cols # 640 + 16(front) + 96(sync) + 48(back) = 800
        self.total_rows  = total_rows # 480 + 10(front) + 2(sync) + 33(back) = 525

        super().__init__({
            "pattern_i": IN(4),
            "hsync_i": IN(1),
            "vsync_i": IN(1),
            "hync_o": OUT(1),
            "vsync_o": OUT(1),
            "col_count_o": OUT(10),
            "row_count_o": OUT(10),
        })

        def elaborate(self, platform):
            m = Module()

            w_frame_start = Signal()

            m.d.comb += [
                self.vsync_o.eq(self.vsync_i),
                self.hync_o.eq(self.hsync_i),
                self.w_fram_start.eq(~self.vsync_o & ~self.vsync_i)
            ]

            with m.If(w_frame_start):
                m.d.sync += [
                    self.col_count_o.eq(0),
                    self.raw_count_o.eq(0)
                ]
            with m.Else():
                with m.If(self.col_count == self.total_cols - 1):
                    with m.If(self.row_count == self.total_rows - 1):
                        m.d.sync += self.row_count_o.eq(0)
                    with m.Else():
                        m.d.sync += self.row_count.eq(self.row_count + 1)
                with m.Else():
                    m.d.sync += self.col_count.eq(self.col_count + 1)


            return m



class VGAPatternGen(Component):
    def __init__(self, video_width=3, total_cols=800, total_rows=525, active_clos=640, active_row=480):
        self.video_witdh = video_width
        self.total_cols  = total_cols # 640 + 16(front) + 96(sync) + 48(back) = 800
        self.total_rows  = total_rows # 480 + 10(front) + 2(sync) + 33(back) = 525
        self.active_clos = active_clos
        self.active_row  = active_row

        super().__init__({
            "pattern_i": IN(4),
            "hsync_i": IN(1),
            "vsync_i": IN(1),
            "hync_o": OUT(1),
            "vsync_o": OUT(1),
            "red_video_o": OUT(video_width),
            "green_video_o": OUT(video_width),
            "blue_video_o": OUT(video_width)
        })

        def elaborate(self, platform):
            m = Module()
            vga_layout = data.StructLayout({
                "red": self.video_witdh,
                "green": self.video_witdh,
                "blue": self.video_witdh
            })

            pattern = Array([
                Record(vga_layout, name=f"pattern_{i}") for i in range(16)
            ])

            w_col_count = Signal(10)
            w_row_count = Signal(10)

            m.submodules.uut = uut = SyncToCount(total_cols=total_cols, total_rows=total_rows)
            m.d.comb += [
                uut.hsync_i.eq(self.hsync_i),
                uut.vsync_i.eq(self.vsync_i),
                self.vsync_o.eq(uut.vsync_o),
                self.hsync_o.eq(uut.hsync_o),
                w_col_count.eq(uut.col_count_o),
                w_row_count.eq(uut.row_count_o)
            ]

            w_bar_width = Signal(7)
            w_bar_select = Signal(3)

            def p(idx, red=0, green=0, blue=0):
                return [pattern[idx].red.eq(red), pattern[idx].green.eq(green), pattern[idx].blue.eq(blue)]

            all_clos = Mux((w_col_count < self.active_clos) & (w_row_count < self.active_row),
                           Repl(1, self.video_witdh), 0)

            checkerboard = Mux(w_col_count[5] ^ w_row_count[5], Repl(1, self.video_witdh), 0)

            red_con = Mux((w_bar_select == 4) | (w_bar_select == 5) |
                          (w_bar_select == 6) | (w_bar_select == 7),
                          Repl(1, self.video_witdh), 0)
            green_con = Mux((w_bar_select == 2) | (w_bar_select == 3) |
                          (w_bar_select == 6) | (w_bar_select == 7),
                          Repl(1, self.video_witdh), 0)
            blue_con = Mux((w_bar_select == 1) | (w_bar_select == 3) |
                          (w_bar_select == 5) | (w_bar_select == 7),
                          Repl(1, self.video_witdh), 0)

            black_white_border = Mux((w_row_count <= 1) | (w_row_count == self.active_row-2) |
                                     (w_col_count <= 1) | (w_col_count >= self.active_clos-2),
                                     Repl(1, self.video_witdh), 0)

            m.d.comb += [
                *p(0),
                *p(1, red=all_clos),
                *p(2, green=all_clos),
                *p(3, blue=all_clos),
                *p(4, red=checkerboard, green=checkerboard, blue=checkerboard),
                *p(5, red=red_con, green=green_con, blue=blue_con),
                *p(6, red=black_white_border, green=black_white_border, blue=black_white_border),
            ]

            with m.If(self.pattern_i < 7):
                m.d.sync += [
                    self.red_video_o.eq(pattern[self.pattern_i].red),
                    self.green_video_o.eq(pattern[self.pattern_i].green),
                    self.blue_video_o.eq(pattern[self.pattern_i].blue)
                ]
            with m.Else():
                m.d.sync += [
                    self.red_video_o.eq(pattern[0].red),
                    self.green_video_o.eq(pattern[0].green),
                    self.blue_video_o.eq(pattern[0].blue)
                ]


            return m

class VGASyncPorch(Component):
    def __init__(self, video_width=3, total_cols=3, total_rows=3, active_clos=2, active_row=2):
        self.video_witdh = video_width
        self.total_cols  = total_cols # 640 + 16(front) + 96(sync) + 48(back) = 800
        self.total_rows  = total_rows # 480 + 10(front) + 2(sync) + 33(back) = 525
        self.active_clos = active_clos
        self.active_row  = active_row

        super().__init__({
            "hsync_i": IN(1),
            "vsync_i": IN(1),
            "red_video_i": IN(video_width),
            "green_video_i": IN(video_width),
            "blue_video_i": IN(video_width),
            "hync_o": OUT(1),
            "vsync_o": OUT(1),
            "red_video_o": OUT(video_width),
            "green_video_o": OUT(video_width),
            "blue_video_o": OUT(video_width)
        })

        def elaborate(self, platform):
            m = Module()

            w_hsync = Signal()
            w_vsync = Signal()

            w_clo_count = Signal(10)
            w_row_count = Signal(10)

            r_red_video = Signal(video_width)
            r_green_video = Signal(video_width)
            r_blue_video = Signal(video_width)

            m.submodules.uut = uut = SyncToCount(total_cols=total_cols, total_rows=total_rows)
            m.d.comb += [
                uut.hsync_i.eq(self.hsync_i),
                uut.vsync_i.eq(self.vsync_i),
                self.vsync_o.eq(uut.vsync_o),
                self.hsync_o.eq(uut.hsync_o),
                w_col_count.eq(uut.col_count_o),
                w_row_count.eq(uut.row_count_o)
            ]

            while m.If((w_clo_count < (18 + self.active_clos)) | (w_clo_count > (self.totoal_cols - 49))):
                m.d.sync += self.hsync_o.eq(w_hsync)
            with m.Else():
                m.d.sync += self.hsync_o.eq(w_hsync)

            with m.If((w_row_count < 10 + self.active_rows) | (w_row_count > self.totoal_rows - 32)):
                m.d.sync += self.vsync_o.eq(1)
            with m.Else():
                m.d.sync += self.vsync_o.eq(w_vsync)

            m.d.comb += [
                r_red_video.eq(self.red_video),
                r_green_video.eq(self.green_video),
                r_blue_video.eq(self.blue_video),

                self.red_video_o.eq(r_red_video),
                self.green_video_o.eq(r_green_video),
                self.blue_video_o.eq(r_blue_video),
            ]

            return m


class VGATop(Component):
    def __init__(self, video_width=3, total_cols=800, total_rows=525, active_clos=640, active_row=480):
        self.video_witdh = video_width
        self.total_cols  = total_cols # 640 + 16(front) + 96(sync) + 48(back) = 800
        self.total_rows  = total_rows # 480 + 10(front) + 2(sync) + 33(back) = 525
        self.active_clos = active_clos
        self.active_row  = active_row

        super().__init__({
            "r": OUT(self.video_witdh),
            "g": OUT(self.video_witdh),
            "b": OUT(self.video_witdh),
            "hync_o": OUT(1),
            "vsync_o": OUT(1),
        })

        def elaborate(self, platform):
            m = Module()

            w_red_video_tp   = Signal(self.video_witdh)
            w_green_video_tp = Signal(self.video_witdh)
            w_blue_video_tp  = Signal(self.video_witdh)

            w_red_video_porch   = Signal(self.video_witdh)
            w_green_video_porch = Signal(self.video_witdh)
            w_blue_video_porch  = Signal(self.video_witdh)

            w_hsync_start = Signal()
            w_vsync_start = Signal()

            m.submodule.vga_sync_pulses = vga_sync_pulses = VGASyncPulses(
                total_cols=self.total_cols,
                total_rows=self.total_rows,
                active_clos=self.active_clos,
                active_row=self.active_row)

            m.d.comb += [
                w_hsync_start.eq(vga_sync_pulses.hsync_o),
                w_vsync_start.eq(vga_sync_pulses.vsync_o)
            ]

            m.submodule.vga_pattern_gen = vga_pattern_gen = VGAPatternGen(
                total_cols=self.total_cols,
                total_rows=self.total_rows,
                active_clos=self.active_clos,
                active_row=self.active_row)

            m.d.comb += [
                vga_pattern_gen.eq(Const(1, 4)),
                vga_pattern_gen.hsync_i.eq(w_hsync_start),
                vga_pattern_gen.vsync_i.eq(w_vsync_start),
                w_hsync_tp.eq(vga_pattern_gen.hsync_o),
                w_vsync_tp.eq(vga_pattern_gen.vsync_o),
                w_red_video_tp.eq(vga_pattern_gen.red_video_o),
                w_green_video_tp.eq(vga_pattern_gen.green_video_o),
                w_blue_video_tp.eq(vga_pattern_gen.blue_video_o),
            ]

            m.submodule.vga_sync_porch = vga_sync_porch = VGASyncPorch(
                video_width=self.video_witdh,
                total_cols=self.total_cols,
                total_rows=self.total_rows,
                active_clos=self.active_clos,
                active_row=self.active_row)

            m.d.comb += [
                vga_sync_porch.hsync_i.eq(w_hsync_tp),
                vga_sync_porch.vsync_i.eq(w_vsync_tp),
                vga_sync_porch.red_video_i.eq(w_red_video_tp),
                vga_sync_porch.blue_video_i.eq(w_green_video_tp),
                vga_sync_porch.green_video_i.eq(w_blue_video_tp),
                w_hsync_porch.eq(vga_sync_porch.hsync_o),
                w_vsync_porch.eq(vga_sync_porch.vsync_o),
                w_red_video_porch.eq(vga_sync_porch.red_video_o),
                w_green_video_porch.eq(vga_sync_porch.green_video_o),
                w_blue_video_porch.eq(vga_sync_porch.blue_video_o),
            ]

            m.d.comb += [
                self.hync_o.eq(w_hsync_porch),
                self.vsync_o.eq(w_vsync_porch)
            ]

            m.d.comb += [

                self.r.eq(w_red_video_porch),
                self.g.eq(w_green_video_porch),
                self.b.eq(w_blue_video_porch),
            ]

            return m
