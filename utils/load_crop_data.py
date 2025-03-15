def load_crop_data(filename):
    crop_data = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()  
                if line:  
                    parts = line.split(", ")
                    crop_name = parts[0].split(": ")[1]
                    crop_id = parts[1].split(": ")[1]
                    crop_data[crop_name] = crop_id
        return crop_data
    except Exception as e:
        print(f"Error loading crop data: {e}")
        return {}


