from amaranth import *
from amaranth.lib.wiring import *

class UART(Component):
    """
    Parameters
    ----------
    divisor : int
        Set to ``round(clk-rate / baud-rate)``.
        E.g. ``27e6 / 115200`` = ``234```.
    """
    def __init__(self, divisor, data_bits=8):
        assert divisor >= 4

        self.data_bits = data_bits
        self.divisor = divisor

        super().__init__({
            "tx_o": Out(1),
            "rx_i": In(1),

            "tx_data": In(data_bits),
            "tx_rdy": In(1),
            "tx_ack": Out(1),

            "rx_data": Out(data_bits),
            "rx_err": Out(1),
            "rx_ovf": Out(1),
            "rx_rdy": Out(1),
            "rx_ack": In(1),
        })

    def elaborate(self, platform):
        m = Module()

        tx_phase = Signal(range(self.divisor)) # each divisor clk send one bit
        tx_shreg = Signal(1 + self.data_bits + 1, init=-1) # start bit + data bits + stop bit
        tx_count = Signal(range(len(tx_shreg) + 1))

        m.d.comb += self.tx_o.eq(tx_shreg[0])
        with m.If(tx_count == 0):             # no data send
            m.d.comb += self.tx_ack.eq(1)     # tx in idle mode
            with m.If(self.tx_rdy):           # need send data
                m.d.sync += [
                    tx_shreg.eq(Cat(C(0, 1), self.tx_data, C(1, 1))), # construct a frame
                    tx_count.eq(len(tx_shreg)),                       # frame bits count
                    tx_phase.eq(self.divisor - 1)                     # load tx_phase for each bit
                ]
        with m.Else(): # continue send
            with m.If(tx_phase != 0):
                m.d.sync += tx_phase.eq(tx_phase - 1) # bit time clk count
            with m.Else():
                m.d.sync += [
                    tx_shreg.eq(Cat(tx_shreg[1:], C(1, 1))),  # shift tx_shreg
                    tx_count.eq(tx_count - 1),                # tx bits count - 1
                    tx_phase.eq(self.divisor -1)              # reload tx_phase for next bit
                ]

        rx_phase = Signal(range(self.divisor))
        rx_shreg = Signal(1 + self.data_bits + 1, init=-1)
        rx_count = Signal(range(len(rx_shreg) + 1))

        m.d.comb += self.rx_data.eq(rx_shreg[1:-1]) # skip start and stop bits
        with m.If(rx_count == 0): # received done, then check rx_err
            m.d.comb += self.rx_err.eq(~(~rx_shreg[0] & rx_shreg[-1])) # only start bit is 0 and stop is 1
            with m.If(~self.rx_i): # new start bit detected
                with m.If(self.rx_ack | ~self.rx_rdy): # data has been take out
                    m.d.sync += [
                        self.rx_rdy.eq(0),             # clean rx ready
                        self.rx_ovf.eq(0),             # clean rx overflow
                        rx_count.eq(len(rx_shreg)),    # set rx_count
                        rx_phase.eq(self.divisor // 2) # middle point sampling, only in start bit
                    ]
                with m.Else():                    # data has not been take out
                    m.d.sync += self.rx_ovf.eq(1) # overflow
            with m.If(self.rx_ack):               # data has been take out
                m.d.sync += self.rx_rdy.eq(0)          # rx is not ready
        with m.Else():           # reveive continue
            with m.If(rx_phase != 0):
                m.d.sync += rx_phase.eq(rx_phase - 1)
            with m.Else():       # one bit receive done
                m.d.sync += [
                    rx_shreg.eq(Cat(rx_shreg[1:], self.rx_i)), # shift rx_shreg to next bit
                    rx_count.eq(rx_count - 1),                 # rx bits count -1
                    rx_phase.eq(self.divisor -1)               # reload rx_phase for next bit
                ]
                with m.If(rx_count == 1):                      # nex is stop bits
                    m.d.sync += self.rx_rdy.eq(1)              # rx ready

        return m
