module detect_2(
		input clk_i,
		input rst_n_i,
		output out_o
		);
   reg 		       out_r;

   //state and parameter
   reg [1:0] 	       Current_state;
   reg [1:0] 	       Next_state;

   parameter [1:0] S0 = 2'b00;
   parameter [1:0] S1 = 2'b01;
   parameter [1:0] S2 = 2'b10;
   parameter [1:0] S3 = 2'b11;

   // sequential logic circuit
   always@(posedge clk_i or negedge rst_n_i) begin
      if(!rst_n_i) begin
	 Current_state <= 0;
      end
      else begin
	 Current_state <= Next_state;
      end
   end

   // combinational logic circuit
   always@(*) begin
      out_r = 1'b0;
      case(Currnet_state)
	S0: begin
	   out_t = 1'b0;
	   Next_state = S1;
	end
	S1: begin
	   out_t = 1'b1;
	   Next_state = S2;
	end
	S2: begin
	   out_t = 1'b0;
	   Next_state = S3;
	end
	S3: begin
	   out_t = 1'b1;
	   Next_state = Next_state;
	end
      endcase
   end // always@ (*)

  assign _out_o = out_r;
endmodule // detect_2

