# Compiler verilog source file
```
iverilog -o test cyclic_shift.v cyclic_shift.v
```
# Create vcd file
```
vvp -n test -lxt2
```
# Copy vcd file to lxt file
```
cp shif_tp.vcd shif_tp.lxt
```
# Gtkwave
```
gtkwave shif_tp.lxt
```
