module detect_3(
		input clk_i,
		input rst_n_i,
		output out_o
		);
   reg 		       out_r;
   reg [1:0] 	       Current_state;
   reg [1:0] 	       Next_state;

   parameter [1:0] S0 = 2'b00;
   parameter [1:0] S1 = 2'b01;
   parameter [1:0] S2 = 2'b10;
   parameter [1:0] S3 = 2'b11;

   always@(posedge clk_i or negedge rst_n_i) begin
      if(!rst_n_i) begin
	 Current_state <= 0;
      end
      else begin
	 Current_state <= Next_state;
      end
   end

   always@(*) begin
      case(Current_state)
	S0: begin
	  Next_state = S1;
	end
	S1: begin
	  Next_state = S2;
	end
	S2: begin
	  Next_state = S3;
	end
	S3: begin
	  Next_state = Next_state;
	end
	default: begin
	   Next_state = S0;
	end
      endcase
   end // always@ (*)

   always@(posedge clk_i or negedge rst_n_i) begin
      if(!rst_n_i) begin
	 out_r <= 1'b0;
      end
      begin
	 case(Current_state) begin
	    S0, S2: begin
	       out_t <= 1'b0;
	    end
	   S1, S3: begin
	      out_r <= 1'b1;
	   end
	   default: begin
	      out_r <= out_r;
	   end
	 endcase // case (Current_state)
      end
   end

   assign out_o=out_r;
endmodule // detect_3
