module led_flow(
		clk,
		rst_n,
		pio_led
		);
   input clk;
   input rst_n;

   output [3:0] pio_led;

   wire 	clock_slow;

   freq freq(
	     .clk(clk),
	     .rst_n(rst_n),
	     .clk_slow(clock_slow)
	     );

   led led(
	   .clk(clock_slow),
	   .rst_n(rst_n),
	   .pio_led(pio_led)
	   );
endmodule
