import intel_jtag_uart as _uart

_BUTTON_TRANSLATE = {
    "0": (True, True),
    "1": (False, True),
    "2": (True, False),
    "3": (False, False)
}

class Inputs:

    def __init__(self, accelerometer: str, buttons: str, switches: str):
        self.accelerometer: str = accelerometer
        self.buttons: tuple[bool] = _BUTTON_TRANSLATE.get(buttons, (False, False))
        self.switches: int = int(switches)
        

class FPGAController:

    def __init__(self, **kwargs):
        self._jtag_uart = _uart.intel_jtag_uart(**kwargs)

    def _send_command(self, command: str, argument: str = "") -> str:
        """
        Sends a command to the FPGA using the format specified
        :param command: Command to use
        :param argument: Argument to pass
        :return: Data returned from the FPGA
        """
        self._jtag_uart.write(f"{command} {argument}".encode())
        return self._jtag_uart.read().decode()
    
    def read_inputs(self) -> Inputs:
        """
        Reads inputs for the FPGA
        :return: Inputs class for the data
        """
        return Inputs(*self._send_command("r").split("|"))
    
    def update_leds(self, num: int) -> None:
        """
        Updates the LEDs to be lit up, to a maximum of 9
        :param num: Number of LEDs to light up
        """
        self._send_command("l", str(min(num, 9)))

    def update_hex(self, text: str) -> None:
        """
        Updates the HEX display to the text, up to 6 characters
        :param text: Text to display
        """
        self._send_command("s", text[0:6].lower())