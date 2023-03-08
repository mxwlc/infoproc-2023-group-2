# Class handling the controller
# TODO: Tune the thresholds for the fpga controller -> may work

from pynput.keyboard import Key, Controller
import time


class fpga_controller:

    def __init__(self):
        self.keyboard = Controller()

    def shoot(self):
        # TODO: implement space
        self.keyboard.press(Key.space)
        time.sleep(0.1)
        self.keyboard.release(Key.space)

    def moveleft(self):
        # TODO: implement move left
        self.keyboard.press(Key.left)

    def moveright(self):
        # TODO: implement move right
        self.keyboard.press(Key.right)

    def stop(self):
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.right)

    def left_or_right(self, accel_input):
        accel_input = int(self.uhex_to_shex(accel_input))
        if accel_input < -100:
            self.moveleft()
        elif accel_input > 100:
            self.moveright()
        else:
            self.stop()

    def uhex_to_shex(uhex):
        if uhex & 0x80000000:
            return - (uhex & 0x79999999)
        else:
            return uhex & 0x79999999
