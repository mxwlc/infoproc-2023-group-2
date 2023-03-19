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
		alt_printf("Text: %s\n\n", text);
		switch (text[0]){

		case 'r':
			alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
			alt_printf("%x|%x|%x", *(BTN_ptr), *(SW_ptr), x_read);
			break;

		case 's':
			alt_printf("Score");
			break;

		case 'l':
			switch(text[2]){
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
			default:
				lives = 0b0;
				break;
			}
			alt_printf("Lives %s", &text[2]);
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
