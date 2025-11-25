from amaranth import *
from amaranth.lib.enum import Enum

class HoldFlag(Enum, shape=unsigned(3)):
    """Hold flag"""
    HOLD_NONE=0
    HOLD_PC = 1
    HOLD_IF = 2
    HOLD_ID = 3
