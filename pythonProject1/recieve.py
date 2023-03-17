import controller
import host
"""
This recieves the inputs from the fpga and turns it into keyboard outputs.
"""
def main():
    fpga = host.FPGAController()
    keyboard = controller.keyboard_controller()
    
    ## name
    
    
    while True:
        current = fpga.read_inputs()
        keyboard.left_or_right(int(current.accelerometer,16))
        if current.buttons == (True,True) or current.buttons == (False, True):
            keyboard.shoot()
        
if __name__ == "__main__":
    main()