import json

def parse_csv_to_json(csv_data):
    # Initialize our JSON structure
    lines = [i.strip("\n") for i in csv_data[1:]]
    result = {}
    current_category = None
    current_state = None
    current_city = None
    
    for line in lines:
        parts = line.split(',')
        parts = [part.strip() for part in parts]
        
        # Count non-empty parts
        non_empty_parts = [p for p in parts if p]
        
        if len(non_empty_parts) == 1:
            # This could be a category, state, or city
            item = non_empty_parts[0]
            
            # Look ahead if possible to determine type
            next_idx = lines.index(line) + 1
            if next_idx < len(lines):
                next_line = lines[next_idx]
                next_parts = next_line.split(',')
                next_non_empty = [p for p in next_parts if p.strip()]
                
                if len(next_non_empty) == 1:
                    # Look ahead one more line if possible
                    next_next_idx = next_idx + 1
                    if next_next_idx < len(lines):
                        next_next_line = lines[next_next_idx]
                        next_next_parts = next_next_line.split(',')
                        next_next_non_empty = [p for p in next_next_parts if p.strip()]
                        
                        if len(next_next_non_empty) == 1:
                            # It's a category
                            current_category = item
                            result[current_category] = {}
                            current_state = None
                            current_city = None
                            continue
                    
                    # It's a state
                    current_state = item
                    if current_category not in result:
                        result[current_category] = {}
                    result[current_category][current_state] = {}
                    current_city = None
                    continue
            
            # It's a city
            current_city = item
            if current_category not in result:
                result[current_category] = {}
            if current_state not in result[current_category]:
                result[current_category][current_state] = {}
            result[current_category][current_state][current_city] = {}
        
        elif len(non_empty_parts) > 1:
            # It's a data point
            if current_category and current_state and current_city:
                area = parts[0]
                unit = parts[1]
                price = parts[5]
                
                # Structure as area: [unit, price]
                result[current_category][current_state][current_city][area] = {"Amt": unit, "Price": price}
    
    return result


def save_json(file):
    with open(f"{file}", "r") as f:
        sample_data = f.readlines()

    parsed_data = parse_csv_to_json(sample_data)

    json_result = json.dumps(parsed_data, indent=4)
    # If you want to save to a file:
    with open(f"{file.split(".")[0]}.json", 'w') as f:
        f.write(json_result)

