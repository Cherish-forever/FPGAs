module detect_1(
		input clk_i,
		input rst_n_i,
		output out_o
		);
   reg 		       out_r;
   reg [1:0] 	       state;

   parameter [1:0] S0=2'b00;
   parameter [1:0] S1=2'b01;
   parameter [1:0] S2=2'b10;
   parameter [1:0] S3=2'b11;

   always@(posedge clk_i or negedge rst_n_i) begin
      if(!rst_n_i) begin
	 state <= 0;
	 ort_r <=1'b0;
      end
      else begin
	 case (state)
	   S0: begin
	      out_r <=1'b0;
	      state <= S1;
	   end
	   S1: begin
	      out_r <= 1'b1;
	      state <= S2;
	   end
	   S2: begin
	      out_r <= 1'b0;
	      state <= S3;
	   end
	   S3: begin
	      out_r <= 1'b1;
	      state <= S0;
	   end
	 endcase
      end
   end // always@ (posedge clk_i or negedge rst_n_i)
   assign out_o=out_r;
endmodule // detect_1
