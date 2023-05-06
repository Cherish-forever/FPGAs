module freq(
	    clk,
	    rst_n,
	    clk_slow
	    );
   input clk;
   input rst_n;

   output reg clk_slow;
   reg [40:0] counter;

   always@(posedge clk or negedge rst_n) begin
      if (rst_n == 1'b0) begin
	 clk_slow <= 0;
	 counter <= 0;
      end
      else begin
	 if (counter < 12) begin
	    counter <= counter + 1;
	 end
	 else begin
	    counter <= 0;
	    clk_slow = ~clk_slow;
	 end
      end
   end
endmodule
