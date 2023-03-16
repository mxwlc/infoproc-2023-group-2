#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include "system.h"
#include <stdlib.h>

#define PWM_PERIOD 16



int main() {

	volatile int * KEY_ptr = (int *)BUTTON_BASE;
	volatile int * SW_ptr = (int *)SWITCH_BASE;
	int SW_value;
	int KEY_value;
	int KEY_one;
	int KEY_two;
	int i = 0;

    alt_32 x_read;
    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }

    while (1) {
		alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
		KEY_value = *(KEY_ptr);
		SW_value = *(SW_ptr);
		KEY_one = (KEY_value & 0x1);
		KEY_two = ((KEY_value >> 1) & 0x1);
		alt_printf("%x|%x|%x|%x\n", x_read, KEY_one, KEY_two, SW_value);
		for (i=0; i<1000000; i++);
    }

    return 0;
}

