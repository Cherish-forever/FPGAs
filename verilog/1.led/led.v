module led(
	   clk,
	   rst_n,
	   pio_led,
	   );
   input clk;
   input rst_n;

   output reg [3:0] pio_led;
   reg [1:0] 	    state;

   always@(posedge clk or negedge rst_n) begin
      if(rst_n == 1'b0) begin
	 pio_led <= 4'b1111;
	 state <= 0;
      end
      else begin
	 case(state)
	   0: begin
	      pio_led <= 4'b0111;
	      state <= 1;
	   end
	   1: begin
	      pio_led <= 4'b1011;
	      state <= 2;
	   end
	   2: begin
	      pio_led <= 4'b1101;
	      state <= 3;
	   end
	   3: begin
	      pio_led <= 4'b1110;
	      state <= 0;
	   end
	   default: state <= 0;
	 endcase
      end
   end
endmodule
