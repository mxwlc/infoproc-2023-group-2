import subprocess

process = subprocess.Popen("nios2-terminal", stdout=subprocess.PIPE)

while True:
    output = process.stdout.readline()
    if process.poll() is not None:
        break
    if output:
        accel, key_one, key_two = output.strip().decode().split("|")
rc = process.poll()
