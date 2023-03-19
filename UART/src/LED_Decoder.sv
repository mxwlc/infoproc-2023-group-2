module LED_Decoder (
	input		logic	[3:0] in,
	output	logic	[9:0]	out
);

	always_comb
		case(in)
			4'd0: out = 10'b0000000000;
			4'd1: out = 10'b0000000001;
			4'd2: out = 10'b0000000011;
			4'd3: out = 10'b0000000111;
			4'd4: out = 10'b0000001111;
			4'd5: out = 10'b0000011111;
			4'd6: out = 10'b0000111111;
			4'd7: out = 10'b0001111111;
			4'd8: out = 10'b0011111111;
			4'd9: out = 10'b0111111111;
			default: out = 10'b1111111111;
		endcase
	
endmodule