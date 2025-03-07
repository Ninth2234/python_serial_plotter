import serial
import time

# Specify the serial port and baud rate
port = 'COM3'  # Change this to the correct port (e.g., '/dev/ttyUSB0' on Linux or 'COM3' on Windows)
baudrate = 115200
timeout = 1  # Timeout in seconds

# Set up the serial connection
ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

# Give the Pico some time to start sending data
time.sleep(2)

# Read data from the serial port in a loop
try:
    while True:
        # Check if there's data waiting in the buffer
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")
        time.sleep(0.1)  # Small delay to avoid high CPU usage

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # Close the serial connection when done
    ser.close()
