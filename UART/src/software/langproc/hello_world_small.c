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
		KEY_one = (KEY_value & 0x1);
		KEY_two = ((KEY_value >> 1) & 0x1);
		alt_printf("KEY_one: %x\n", KEY_one);
		alt_printf("KEY_two: %x\n", KEY_two);
		printf("X-Axis: %d\n", x_read);
		for (i=0; i<2000000; i++);
    }

    return 0;
}

