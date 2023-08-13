`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company:
// Engineer:
//
// Create Date: 08/13/2023 07:38:55 PM
// Design Name:
// Module Name: key_shake
// Project Name:
// Target Devices:
// Tool Versions:
// Description:
//
// Dependencies:
//
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
//
//////////////////////////////////////////////////////////////////////////////////


module key_shake(
    input clk,
    input rst_n,
    input key_i,
    output [3:0] led_o
    );
    
localparam DELAY_Param=19'd499_999;
reg[3:0] led_o_r;
reg [18:0] div_cnt;

always @ (posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        div_cnt <= 19'd0;
    end
    else if ( div_cnt < DELAY_Param) begin
        div_cnt <= div_cnt + 1'b1;
    end
    else begin
        div_cnt <= 0;
    end
end    

wire delay_10ms = (div_cnt == DELAY_Param) ? 1'b1 : 1'b0;

localparam DETECTER1 = 3'b000;
localparam DETECTER2 = 3'b001;
localparam DETECTER3 = 3'b010;
localparam DETECTER4 = 3'b011;
localparam LED_DIS   = 3'b100;

reg low_flag;
reg high_flag;
reg [2:0] key_state;

always @ (posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        key_state <= DETECTER1;
        low_flag <= 0;
        high_flag <= 0;
        led_o_r <= 4'b1111;
    end
    else if (delay_10ms) begin
        case(key_state)
            DETECTER1: begin
                if (key_i != 1'b1) begin
                    key_state <= DETECTER2;
                end
                else begin
                    key_state <= DETECTER1;
                end
            end
            DETECTER2: begin
                if (key_i != 1'b1) begin
                    low_flag <= 1'b1;
                    key_state <= DETECTER3;
                end
                else begin
                    key_state <= DETECTER1;
                    low_flag <= low_flag;
                end
            end
            DETECTER3: begin
                if (key_i == 1'b1) begin
                    key_state <= DETECTER4;
                end
                else begin
                    key_state <= DETECTER3;
                end
            end
            DETECTER4: begin
                if (key_i == 1'b1) begin
                    high_flag <= 1'b1;
                    key_state <= LED_DIS;
                end
                else begin
                    high_flag <= high_flag;
                    key_state <= DETECTER3;
                end
            end
            LED_DIS: begin
                if (high_flag & low_flag) begin
                    key_state <= DETECTER1;
                    led_o_r <= ~led_o_r;
                    high_flag <= 1'b0;
                    low_flag <= 1'b0;
                end
                else begin
                    led_o_r <= led_o_r;
                    key_state <= key_state;
                    high_flag <= high_flag;
                    low_flag <= low_flag;
                end
            end
            default: begin
                key_state <= DETECTER1;
                led_o_r <= 0;
                high_flag <= 0;
                low_flag <= 0;
            end
        endcase
    end
    else begin
        key_state <= key_state;
        led_o_r <= led_o_r;
        high_flag <= high_flag;
        low_flag <= low_flag;
    end
end

assign led_o = led_o_r;

endmodule
