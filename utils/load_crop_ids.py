# Function to extract and save crop IDs to a new file (crop_ids.txt)
def extract_and_save_crop_ids(input_filename, output_filename):
    crop_ids = set()
    try:
        with open(output_filename, 'r') as file:
            for line in file:
                crop_ids.add(line.strip())  
    except FileNotFoundError:
        pass

    try:
        with open(input_filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    if len(parts) == 2:
                        crop_id = parts[1].split(": ")[1]
                        crop_ids.add(crop_id)
    except Exception as e:
        print(f"Error reading crop_dict.txt: {e}")

    try:
        with open(output_filename, 'w') as file:
            for crop_id in crop_ids:
                file.write(crop_id + "\n")
        print(f"Updated crop IDs saved to {output_filename}")
    except Exception as e:
        print(f"Error saving crop IDs to {output_filename}: {e}")

