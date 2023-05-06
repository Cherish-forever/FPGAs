`timescale 1ns/1ps

module tb;
   reg clk;
   reg rst_n;

   wire [3:0] led_out;

   initial
     begin
	clk=0;
	rst_n=0;
	#1000.1 rst_n=1;
	#10000;
	$finish;
     end
   always #10 clk=~clk;
   cyclic_shift shift(
		.clk(clk),
		.rst_n(rst_n),
		.led_out(led_out)
		);
   initial
     begin
	$dumpfile("shift_tp.vcd");
	$dumpvars(0, shift);
     end
endmodule
