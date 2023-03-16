# import subprocess
#
# process = subprocess.Popen("nios2-terminal", stdout=subprocess.PIPE)
#
# while True:
#     output = process.stdout.readline()
#     if process.poll() is not None:
#         break
#     if output:
#         accel, key_one, key_two = output.strip().decode().split("|")
# rc = process.poll()

import sys
import time
import intel_jtag_uart

try:
    ju = intel_jtag_uart.intel_jtag_uart()

except Exception as e:
    print(e)
    sys.exit(0)

print("Initialised")

ju.write(b'r\n')
print("read: ", ju.read())
ju.write(b's\n')
print("read: ", ju.read())
ju.write(b'l\n')
print("read: ", ju.read())
ju.write(b'u\n')
print("read: ", ju.read())