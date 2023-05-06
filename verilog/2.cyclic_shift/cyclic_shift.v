module cyclic_shift(
		    clk,
		    rst_n,
		    led_out
		    );
   input clk;
   input rst_n;

   output reg [3:0] led_out;

   always@(posedge clk or negedge rst_n)
     begin
	if (!rst_n)
	  begin
	     led_out <= 4'b0111;
	  end
	else
	  begin
	     led_out <= {led_out[0], led_out[3:1]};
	  end
     end // always@ (posedge clk or negedge rst_n)
endmodule
