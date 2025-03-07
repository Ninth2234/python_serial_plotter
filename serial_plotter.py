from numpy import var
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import logging
import time

# Specify the serial port and baud rate
port = 'COM3'  # Change this to the correct port (e.g., '/dev/ttyUSB0' on Linux or 'COM3' on Windows)
baudrate = 1_000_000
timeout = 1  # Timeout in seconds

# Set up the serial connection
ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

# Initialize lists to hold the data for plotting
x_data = []
y_data = []

data_log = dict()

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 100)  # x-axis range (last 100 points)
ax.set_ylim(0, 5)    # y-axis range (adjust based on your data)

# Label for the plot
ax.set_xlabel('Time')
ax.set_ylabel('Data Value')

# Set up the logger to write to a file
logging.basicConfig(filename='data/serial_data_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


start_time = time.time()
logging.info("LOGGING")
# This function will be used to update the plot with new data
def update(frame):
    try:
        # Read data from serial port
        data = ser.readline().decode('utf-8').strip()  # Read line and strip whitespace
        if data:
            # Log the incoming data to the file
            logging.info(data)

            current_time = time.time()-start_time

            ax.clear()  # Clear previous plot
            # Example input format: 'var_name:value var_name_value ...'
            parsed_data = data.split(",")
            for item in parsed_data:
                var_name, value = item.split(':')
                value = float(value)  # Convert to float for plotting
                
                
                if var_name in data_log:
                    data_log[var_name]['y'].append(value)
                    data_log[var_name]['x'].append(current_time)  # Use length of data as time or X axis
                else:
                    print("ok")
                    data_log[var_name] = dict()
                    data_log[var_name]['y'] = [value]
                    data_log[var_name]['x'] = [current_time]
                
                # # For this example, we plot the last var_name_value on the y-axis
                # y_data.append(value)
                # x_data.append(len(x_data))  # Use length of data as time or X axis
                
                # Keep the x_data length fixed (100 points in this case)
                if len(data_log[var_name]['y']) > 100_000:
                    data_log[var_name]['y'].pop(0)
                    data_log[var_name]['x'].pop(0)

            # Update the plot with new data
            for var_name in data_log:
                ax.plot(data_log[var_name]['x'], data_log[var_name]['y'],label=var_name)
            ax.legend()
            # ax.set_xlim(max(0, len(x_data) - 100), len(x_data))  # Keep last 100 points
            # ax.set_ylim(min(y_data) - 1, max(y_data) + 1)  # Adjust y-axis range dynamically
    except Exception as e:
        print(f"Error: {e}")

    return ax,

# Set up the animation for real-time plotting
ani = FuncAnimation(fig, update, blit=False, interval=100)

# Show the plot
plt.title('Real-time Serial Data Plot')
plt.show()

# Close the serial connection when done
ser.close()
