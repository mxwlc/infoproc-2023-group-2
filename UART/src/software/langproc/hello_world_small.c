#include <stdio.h>
#include <string.h>
#include "sys/alt_stdio.h"
#include "altera_avalon_pio_regs.h"
#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#define CHARLIM 256		// Maximum character length of what the user places in memory.  Increase to allow longer sequences
#define QUITLETTER '~' 		// Letter to kill all processing

char get_input(char curr, int *length, char *text, int *running) {
	if(curr == '\n') return curr;								// If the line is empty, return nothing.
	int idx = 0;										// Keep track of how many characters have been sent down for later printing
	char newCurr = curr;

	while (newCurr != EOF && newCurr != '\n'){						// Keep reading characters until we get to the end of the line
		if (newCurr == QUITLETTER) { *running = 0; }					// If quitting letter is encountered, setting running to 0
		text[idx] = newCurr;								// Add the next letter to the text buffer
		idx++;										// Keep track of the number of characters read
		newCurr = alt_getchar();							// Get the next character
	}
	*length = idx;

	return newCurr;
}

const int SegmentCharacters[96] = {
	0b00000000, /* (space) */
	0b10000110, /* ! */
	0b00100010, /* " */
	0b01111110, /* # */
	0b01101101, /* $ */
	0b11010010, /* % */
	0b01000110, /* & */
	0b00100000, /* ' */
	0b00101001, /* ( */
	0b00001011, /* ) */
	0b00100001, /* * */
	0b01110000, /* + */
	0b00010000, /* , */
	0b01000000, /* - */
	0b10000000, /* . */
	0b01010010, /* / */
	0b00111111, /* 0 */
	0b00000110, /* 1 */
	0b01011011, /* 2 */
	0b01001111, /* 3 */
	0b01100110, /* 4 */
	0b01101101, /* 5 */
	0b01111101, /* 6 */
	0b00000111, /* 7 */
	0b01111111, /* 8 */
	0b01101111, /* 9 */
	0b00001001, /* : */
	0b00001101, /* ; */
	0b01100001, /* < */
	0b01001000, /* = */
	0b01000011, /* > */
	0b11010011, /* ? */
	0b01011111, /* @ */
	0b01110111, /* A */
	0b01111100, /* B */
	0b00111001, /* C */
	0b01011110, /* D */
	0b01111001, /* E */
	0b01110001, /* F */
	0b00111101, /* G */
	0b01110110, /* H */
	0b00110000, /* I */
	0b00011110, /* J */
	0b01110101, /* K */
	0b00111000, /* L */
	0b00010101, /* M */
	0b00110111, /* N */
	0b00111111, /* O */
	0b01110011, /* P */
	0b01101011, /* Q */
	0b00110011, /* R */
	0b01101101, /* S */
	0b01111000, /* T */
	0b00111110, /* U */
	0b00111110, /* V */
	0b00101010, /* W */
	0b01110110, /* X */
	0b01101110, /* Y */
	0b01011011, /* Z */
	0b00111001, /* [ */
	0b01100100, /* \ */
	0b00001111, /* ] */
	0b00100011, /* ^ */
	0b00001000, /* _ */
	0b00000010, /* ` */
	0b01011111, /* a */
	0b01111100, /* b */
	0b01011000, /* c */
	0b01011110, /* d */
	0b01111011, /* e */
	0b01110001, /* f */
	0b01101111, /* g */
	0b01110100, /* h */
	0b00010000, /* i */
	0b00001100, /* j */
	0b01110101, /* k */
	0b00110000, /* l */
	0b00010100, /* m */
	0b01010100, /* n */
	0b01011100, /* o */
	0b01110011, /* p */
	0b01100111, /* q */
	0b01010000, /* r */
	0b01101101, /* s */
	0b01111000, /* t */
	0b00011100, /* u */
	0b00011100, /* v */
	0b00010100, /* w */
	0b01110110, /* x */
	0b01101110, /* y */
	0b01011011, /* z */
	0b01000110, /* { */
	0b00110000, /* | */
	0b01110000, /* } */
	0b00000001, /* ~ */
	0b00000000, /* (del) */
};

int read_chars() {
	char text[2*CHARLIM];									// The buffer for the printing text
	char prevLetter = '!';
	int length = 0;
	int running = 1;

	int lives = 0;
	volatile int * BTN_ptr = (int *)BUTTON_BASE;
	volatile int * SW_ptr = (int *)SWITCH_BASE;
    alt_32 x_read;
    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }

	while (running) {									// Keep running until QUITLETTER is encountered
		prevLetter = alt_getchar();							// Extract the first character (and create a hold until one arrives)
		prevLetter = get_input(prevLetter, &length, text, &running);		// Process input text
		switch (text[0]){

		case 'r':
			alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
			alt_printf("%x|%x|%x", *(BTN_ptr), *(SW_ptr), x_read);
			break;

		case 'h':
			alt_printf("Hex Updated.");
			IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, ~SegmentCharacters[text[2] - ' ']);
			IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, ~SegmentCharacters[text[3] - ' ']);
			IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, ~SegmentCharacters[text[4] - ' ']);
			IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, ~SegmentCharacters[text[5] - ' ']);
			IOWR_ALTERA_AVALON_PIO_DATA(HEX1_BASE, ~SegmentCharacters[text[6] - ' ']);
			IOWR_ALTERA_AVALON_PIO_DATA(HEX0_BASE, ~SegmentCharacters[text[7] - ' ']);
			break;

		case 'l':
			switch(text[4]){
			case '1':
				lives = 0b1;
				break;
			case '2':
				lives = 0b11;
				break;
			case '3':
				lives = 0b111;
				break;
			case '4':
				lives = 0b1111;
				break;
			case '5':
				lives = 0b11111;
				break;
			case '6':
				lives = 0b111111;
				break;
			case '7':
				lives = 0b1111111;
				break;
			case '8':
				lives = 0b11111111;
				break;
			case '9':
				lives = 0b111111111;
				break;
			case 'a':
				lives = 0b1111111111;
				break;
			default:
				lives = 0b0;
				break;
			}
			alt_printf("Lives %s", &text[4]);
			IOWR_ALTERA_AVALON_PIO_DATA(LED_BASE, lives);
			break;

		default:
			alt_printf("Unrecognised Command");
			break;
		}
	}

	return 0;
}

int main() {
	return read_chars();
}
