`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company:
// Engineer:
//
// Create Date: 08/13/2023 04:19:47 PM
// Design Name:
// Module Name: water_led
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


module water_led(
    input clk,
    input rst_n,
    output reg [7:0] led_o
    );

    reg [31:0] c0;

    always @(posedge clk or negedge rst_n) begin
        if (rst_n == 1'b0) begin
            led_o <= 8'b0000_0001;
            c0 <= 32'h0;
        end
        else begin
            if (c0 == 32'd50_000_000) begin
                c0 <= 32'h0;
                if (led_o == 8'b1000_0000) begin
                    led_o <= 8'b0000_0001;
                end
                else begin
                    led_o <= led_o << 1;
                end
            end
            else begin
                c0 <= c0 + 1'b1;
                led_o <= led_o;
            end
        end
    end
endmodule
