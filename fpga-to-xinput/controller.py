from pynput.keyboard import Key, Controller


class fpga_controller:

    def __init__(self):
        self.keyboard = Controller()

    def shoot(self):
        # TODO: implement space
        return

    def moveleft(self):
        # TODO: implement move left
        return

    def moveright(self):
        # TODO: implement move right
        return


def uhex_to_shex(uhex):
    if uhex & 0x80000000:
        return - (uhex & 0x79999999)
    else:
        return uhex & 0x79999999


def left_or_right(controller, accel_input):
    if uhex_to_shex(accel_input) < -100:
        controller.moveleft()
    elif uhex_to_shex(accel_input) > 100:
        controller.moveright()


input_num = 0x00000001

print(int(input_num))
print(uhex_to_shex(input_num))
