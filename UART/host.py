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
        self._jtag_uart.write(f"{command} {argument}".encode())
        return self._jtag_uart.read().decode()
    
    def read_inputs(self) -> Inputs:
        return Inputs(*self._send_command("r").split("|"))
    
    def update_leds(self, num: int):
        self._send_command("l", str(min(num, 9)))

    def update_hex(self, text: str):
        self._send_command("s", text[0:6].lower())