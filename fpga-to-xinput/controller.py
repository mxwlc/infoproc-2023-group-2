# Class handling the controller
# TODO: Tune the thresholds for the fpga controller -> may work

from pynput.keyboard import Key, Controller
import time
class keyboard_controller:
    """
    Controller Class used to control the movements of the player
        ...

        Attributes

        ----------

        keyboard : Controller Object
            Simulates key presses and releases to control the player

        Name : Array
            Array containing the name of the player

        Methods

        -------

        shoot()
            Shoots a projectile

        moveleft()
            moves the player left

        moveright()
            moves the player right

        stop()
            stops the player from moving
            
        set_name(name):
            sets the name of the player

        left_or_right(accel_input)
            decides whether the player should move left or right
            parameters:
                accel_input : raw hex output of the fpga accelerometer

        uhex_to_shex(uhex)
            converts the raw hex output from unsigned hex to signed decimal
            parameters:
                uhex : raw hex output from accelerometer
    """

    def __init__(self):
        """
        initialises the keyboard by creating a controller object
        """
        self.keyboard = Controller()
        self.name = []

    def shoot(self):
        """
        Player shoots
        """
        self.keyboard.press(Key.space)
        time.sleep(0.1)
        self.keyboard.release(Key.space)

    def moveleft(self):
        """
        Moves the player to the left by simulating the pressing of a left key
        """
        self.keyboard.press(Key.left)

    def moveright(self):
        """
        Moves the player to the right by simulating the pressing of a right key
        """
        self.keyboard.press(Key.right)

    def stop(self):
        """
        Stops the player from moving at all by "releasing" both buttons
        """
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.right)

    def left_or_right(self, accel_input):
        """
        Moves the player left or right based on the readings from the fpga
        TODO: Tune the thresholds so that the controller works as intended

        ...
         Parameters:
         -----------
            accel_input : raw hex readings from the fpga
        """
        accel_input = int(self.uhex_to_shex(accel_input))
        if accel_input < -10:
            self.moveleft()
        elif accel_input > 10:
            self.moveright()
        else:
            self.stop()

    def set_name(self, name):
        self.name = list(name)        
    
    def uhex_to_shex(uhex):
        """
        Converts the unsigned 32-bit hex data to signed 32-bit decimal
        ...
        Parameters
        ----------
            uhex : unsigned 32-bit Hexidecimal
        """
        if uhex & 0x80000000:
            return - (uhex & 0x79999999)
        else:
            return uhex & 0x79999999