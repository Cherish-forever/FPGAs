#!/usr/bin/python3

from migen import *
from migen.fhdl import verilog

class TestSignal(Module):
    def __init__(self):
        self.a = Signal()        # create a 1bit signal
        self.b = Signal(2)       # create a 2bits signal
        self.c = Signal(max=23)  # create a 5bits signal with max value 23
        self.d = Signal(max=23, reset=10)# create a 5bit signal with default value 10
        self.e = Signal(4, reset_less=True) # create 4bits value without synchronous
        self.f = Signal.like(self.c) # create a Signal base on c, max value is 23, 5bits
        self.g = self.f.nbits        # get signal f bits

def testbench(ts):
    print("a len is: " + str(len(ts.a)))
    print("b len is: " + str(len(ts.b)))
    print("c len is: " + str(len(ts.c)))
    print("d val is: " + str((yield ts.d))) # notice: (yield ts.d) is int type
    print("e len is: " + str(len(ts.e)))
    print("f len is: " + str(len(ts.f)))
    print("g nbits is: " + str(ts.g))

if __name__ == "__main__":
    ts = TestSignal()
    run_simulation(ts, testbench(ts))
