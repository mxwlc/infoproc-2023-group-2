import controller
import host
"""
This recieves the inputs from the fpga and turns it into keyboard outputs.
"""
def main():
    fpga = host.FPGAController()
    keyboard = controller.keyboard_controller()
    fpga.update_hex("player")
    lives = open("life.txt", "r")
   
    
    while True:
        current_life = int(lives.read())
                
        fpga.update_leds(current_life)
        
        current = fpga.read_inputs()
        keyboard.left_or_right(int(current.accelerometer,16))
        if current.buttons == (True,True) or current.buttons == (False, True):
            keyboard.shoot()
    lives.close()
        

if __name__ == "__main__":
    main()