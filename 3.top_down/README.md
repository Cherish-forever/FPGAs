# Compiler verilog source file
```
iverilog -o test led.v led_flow.v led_tb.v freq.v
```
# Create vcd file
```
vvp -n test -lxt2
```
# Copy vcd file to lxt file
```
cp led_tb.vcd led_tb.lxt
```
# Gtkwave
```
gtkwave led_tb.lxt
```
