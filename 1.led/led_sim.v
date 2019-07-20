`timescale 1ns/1ps

module tb;
   reg clk;
   reg rst_n;
   wire [3:0] pio_led;
   initial begin
      clk = 0;
      rst_n = 0;
      #1000.1 rst_n = 1;
      #10000;
      $finish;
   end

   always #10 clk = ~clk;

   led led(
	   .clk(clk),
	   .rst_n(rst_n),
	   .pio_led(pio_led)
	   );
   initial
     $monitor("At time %t", $time);
   initial
     begin
	$dumpfile("led_sim.vcd");
	$dumpvars(0, led);
     end
endmodule
