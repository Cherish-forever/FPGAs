## 1. install verilog compiler and gtkwave
$ sudo apt install iverilog
$ sudo apt install gtkwave

## 2. compile verilog source file
$ cd test_iverilog
$ iverilog hello.v -o hello
$ vvp hello
