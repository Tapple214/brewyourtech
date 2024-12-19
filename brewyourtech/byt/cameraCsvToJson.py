import csv
import json

# Input and output file paths
input_file = '/Users/tapple/Desktop/UOL Y3/Sem 1/Advanced Web Development/Midterm/BYT/brewyourtech/byt/static/byt/csv/Cameras.csv' 
output_file = 'Cameras.json'  # The fixture file to be created

# Initialize counters
total_rows = 0
passed_checks = 0

# Open the CSV file and read its contents
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)  # Automatically uses the header row for keys
    data = []

    # Process each row
    for row in reader:
        total_rows += 1  # Increment total row count

        try:
            # Append a JSON object for each row
            data.append({
                "model": "byt.Camera",  # Replace `your_app_name` with the name of your app
                "pk": None,  # Optionally set this to a unique value if needed
                "fields": {
                    "model": row['Model'],
                    "release_date": int(row['Release date']) if row['Release date'] else None,
                    "max_resolution": int(row['Max resolution']) if row['Max resolution'] else 0,
                    "low_resolution": int(row['Low resolution']) if row['Low resolution'] else 0,
                    "effective_pixels": float(row['Effective pixels']) if row['Effective pixels'] else 0.0,
                    "zoom_wide": int(row['Zoom wide (W)']) if row['Zoom wide (W)'] else 0,
                    "zoom_tele": int(row['Zoom tele (T)']) if row['Zoom tele (T)'] else 0,
                    "normal_focus_range": int(row['Normal focus range']) if row['Normal focus range'] else None,
                    "macro_focus_range": int(row['Macro focus range']) if row['Macro focus range'] else None,
                    "storage_included": int(row['Storage included']) if row['Storage included'] else 0,
                    "weight": int(row['Weight (inc. batteries)']) if row['Weight (inc. batteries)'] else 0,
                    "dimensions": row['Dimensions'] if row['Dimensions'] else "Unknown",
                    "price": float(row['Price']) if row['Price'] else 0.0,
                }
            })
            passed_checks += 1  # Increment passed checks count
        except (ValueError, KeyError) as e:
            print(f"Skipping row due to error: {e}")
            continue

# Save the processed data to a JSON file
with open(output_file, 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

# Print comparison results
print(f"Total rows processed: {total_rows}")
print(f"Rows that passed the checks: {passed_checks}")
print(f"Fixture file {output_file} created successfully!")

# Total rows processed: 1038
# Rows that passed the checks: 1038
# Fixture file Cameras.json created successfully!