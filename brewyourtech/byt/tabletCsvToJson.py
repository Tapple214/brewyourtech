import csv
import json

# Input and output file paths
input_file = '/Users/tapple/Desktop/UOL Y3/Sem 1/Advanced Web Development/Midterm/BYT/brewyourtech/byt/static/byt/csv/Tablets.csv'
output_file = 'Tablets.json'  # The fixture file to be created

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
        
        # Safeguard: Remove the 'index' column if it exists
        row.pop('index', None)

        try:
            # Append a JSON object for each row
            data.append({
                "model": "byt.Tablet",  # Replace `your_app_name` with the name of your app
                "pk": None,  # Optionally set this to a unique value if needed
                "fields": {
                    "name": row['name'],
                    "brand": row['brand'],
                    "rating": float(row['rating']) if row['rating'] else 0.0,
                    "price": row['price'],  # Keep as string
                    "processor_brand": row['processor_brand'],
                    "num_processor": int(float(row['num_processor'])) if row['num_processor'] else 0,
                    "processor_speed": float(row['processor_speed']) if row['processor_speed'] else 0.0,
                    "ram": row['ram'],  # Keep as string
                    "memory_inbuilt": row['memory_inbuilt'],  # Keep as string
                    "battery_capacity": row['battery_capacity'],  # Keep as string
                    "charger": row['charger'],
                    "charging": row['charging'],
                    "display_size_inches": float(row['display_size_inches']) if row['display_size_inches'] else 0.0,
                    "pixel": row['pixel'],
                    "resolution_width": int(float(row['resolution_width'])) if row['resolution_width'] else 0,
                    "resolution_height": int(float(row['resolution_height'])) if row['resolution_height'] else 0,
                    "ppi": float(row['ppi']) if row['ppi'] else 0.0,
                    "frequency_display_hz": float(row['frequency_display_hz']) if row['frequency_display_hz'] else None,
                    "primary_front_camera": float(row['primary_front_camera']) if row['primary_front_camera'] else None,
                    "secondary_front_camera": float(row['secondry_front_camera']) if row['secondry_front_camera'] else None,
                    "primary_rear_camera": float(row['primary_rear_camera']) if row['primary_rear_camera'] else None,
                    "secondary_rear_camera": float(row['secondry_rear_camera']) if row['secondry_rear_camera'] else None,
                    "os_brand": row['os_brand'],
                    "version": row['version'],
                    "memory_card_upto": row['memory_card_upto'],  # Keep as string
                    "sim": row['sim'],
                    "is_5G": row['is_5G'].lower() == 'true',
                    "is_wifi": row['is_wifi'].lower() == 'true',
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

# Total rows processed: 390
# Rows that passed the checks: 390
# Fixture file Tablets.json created successfully!