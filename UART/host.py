import intel_jtag_uart as _uart

class FPGAController:

    def __init__(self, **kwargs):
        self._jtag_uart = _uart.intel_jtag_uart(**kwargs)

    def _send_command(self, command: str, argument: str = "") -> str:
        self._jtag_uart.write(f"{command} {argument}".encode())
        return self._jtag_uart.read().decode()
    
    def read_inputs(self) -> tuple:
        return self._send_command("r").split("|")
    
    def update_leds(self, num: int):
        self._send_command("l", str(min(num, 9)))

    def update_hex(self, text: str):
        self._send_command("s", text[0:6].lower())