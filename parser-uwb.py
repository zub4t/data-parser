import os
import csv

def read_csv_file(file_path):
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        data = [row for row in csv_reader]
    return data

def write_to_csv_file(file_path, data):
    with open(file_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        for row in data:
            csv_writer.writerow(row)
def find_string_position(array, target):
    try:
        position = array.index(target)
    except ValueError:
        position = -1
    return position

def main():
    # Create the "parsed" directory if it doesn't exist
    os.makedirs("parsed", exist_ok=True)

    for i in range(56):
        file_name = f"EXP_{i}"
        print(f"working in {file_name}");
        # Check if the file exists, then process it
        if os.path.exists(file_name):
            data = read_csv_file(file_name)

            # Create a directory for the current EXP_X file
            parsed_directory = os.path.join("parsed", file_name)  # Remove .csv extension
            os.makedirs(parsed_directory, exist_ok=True)

            anchor_data = {}

            # Parse the CSV data
            for row in data:
                try:
                    arr = row[0].split()
                    anchor_info = row[1:]
                    #print((arr[1]=="DIST"))
                    if(arr[1]=="DIST"):
                        # Process each anchor's data
                        for i in range(0, int(anchor_info[0])):
                            pos = find_string_position(anchor_info,f"AN{i}")
                            anchor_id = anchor_info[pos+1]
                            measurement = anchor_info[pos+5]
                            print(f"{anchor_id} {measurement}")
                            if anchor_id not in anchor_data:
                                anchor_data[anchor_id] = []

                            anchor_data[anchor_id].append([arr[0]] + [anchor_id,measurement])
                except:
                    print(f"skiping row {row}")
            # Write the parsed data to separate CSV files
            for anchor_id, anchor_rows in anchor_data.items():
                output_file_path = os.path.join(parsed_directory, f"{anchor_id}.csv")
