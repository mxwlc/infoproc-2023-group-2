import subprocess
import controller as c

def choose_name(controller,cycle,confirm):
    """
    Allows the player to choose a name
    ...
    Parameters 
    ----------
    controller : keyboard controller object
    cycle : allows the player to cycle the current letter
    confirm : confirms the current letter

    """
    index = 0;
    name = []
    while True:
        print(controller.alphabet[index])
        if cycle:
            index += 1
            if index == 26:
                index = 0
        if confirm:
            name.append(controller.alphabet[index])
        if len(name) == 5:
            return name

def main():
    process = subprocess.Popen("nios2-terminal", stdout=subprocess.PIPE)
    keyboard = c.fpga_controller()


    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            accel, key_one, key_two = output.strip().decode().split("|")
        
        ##key one shoot/confirm
        ##key two cycle

        ## send name to fpga


        ## Handles the movement and shooting
        keyboard.left_or_right(accel_input=accel)
        if key_one:
            keyboard.shoot()
        

        
    rc = process.poll()
    
    
if __name__ == "__main__":
    main()
