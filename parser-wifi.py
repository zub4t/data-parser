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

def main():
    # Create the "parsed" directory if it doesn't exist
    os.makedirs("parsed", exist_ok=True)

    for i in range(68):
        file_name = f"EXP_{i}.csv"

        # Check if the file exists, then process it
        if os.path.exists(file_name):
            data = read_csv_file(file_name)

            # Create a directory for the current EXP_X file
            parsed_directory = os.path.join("parsed", file_name[:-4])  # Remove .csv extension
            os.makedirs(parsed_directory, exist_ok=True)

            bssid_data = {}

            # Parse the CSV data
            for row in data:
                timestamp, bssid, rssi, distance, deviation = row

                if bssid not in bssid_data:
                    bssid_data[bssid] = []

                bssid_data[bssid].append(row)

            # Write the parsed data to separate CSV files
            for bssid, bssid_rows in bssid_data.items():
                output_file_path = os.path.join(parsed_directory, f"{bssid}.csv")
                write_to_csv_file(output_file_path, bssid_rows)

if __name__ == "__main__":
    main()
