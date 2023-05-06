`timescale 1ns/1ps

module tb;
   reg clk;
   reg rst_n;

   wire [3:0] pio_led;

   initial
     begin
	clk <= 0;
	rst_n <= 0;
	#1000.1 rst_n=1;
	#10000 $finish;
     end
   always #10 clk=~clk;
   led_flow led_flow(
		     .clk(clk),
		     .rst_n(rst_n),
		     .pio_led(pio_led)
		     );
   initial
     begin
	$dumpfile("led_tb.vcd");
	$dumpvars(0, led_flow);
     end
endmodule
