import serial
import datetime
import os
import time
import sys

# Set the duration of the data capture in seconds
capture_duration = 10
folder = sys.argv[1]
port = sys.argv[2]

# Create the 'EXP_UWB' directory if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

# Find the number of existing files in the 'EXP_UWB' directory
file_count = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

# Open the serial connection to Minicom
ser = serial.Serial(port, 115200)

# Open the file for writing
filename = f'EXP_{file_count}'
filepath = os.path.join(folder, filename)
print("Delay Start")
# Add a 10-second delay before writing
time.sleep(2)
print("Delay end")
with open(filepath, "w") as file:
    # Get the start time of the capture
    start_time = time.monotonic()
    print(capture_duration)

    # Loop until the capture duration is reached
    while (time.monotonic() - start_time) < capture_duration:
        print((time.monotonic() - start_time))

        # Read the output from Minicom
        output_bytes = ser.readline()
        try:
            output = output_bytes.decode('ISO-8859-1', errors='ignore')
        except UnicodeDecodeError:
            # Skip over any invalid bytes
            continue

        # Add a timestamp to each line of output
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        curr_time = round(time.time()*1000)
        output_with_timestamp = f"{curr_time} {output}"

        # Write the output to the file
        file.write(output_with_timestamp)
        file.flush()  # Flush the output buffer to ensure data is written to the file immediately

# Print a message indicating where the data was saved
print(f"Data saved to {filepath}")

