# Compiler verilog source file
```
iverilog -o test led.v led_sim.v
```
# Create vcd file
```
vvp -n test -lxt2
```
# Copy vcd file to lxt file
```
cp led_sim.vcd led_sim.lxt
```
# Gtkwave
```
gtkwave led_sim.lxt
```
