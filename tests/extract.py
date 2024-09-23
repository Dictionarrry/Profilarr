import json

def get_custom_format(format_name, arr_type, debug_level=0):
    # Convert the format_name to lowercase for case-insensitive comparison
    format_name = format_name.lower()

    # Determine the file path based on arr_type
    if arr_type.lower() == "sonarr":
        file_path = 'imports/custom_formats/sonarr/custom formats (sonarr - master).json'
    elif arr_type.lower() == "radarr":
        file_path = 'imports/custom_formats/radarr/custom formats (radarr - master).json'
    else:
        raise ValueError("Unsupported arr type: choose 'sonarr' or 'radarr'")

    try:
        with open(file_path, 'r') as f:
            custom_formats = json.load(f)
        # Search for the custom format by name, case-insensitively
        for custom_format in custom_formats:
            if custom_format['name'].lower() == format_name:
                # Debugging output if level is set to 1
                if debug_level > 1:
                    print("Found custom format:", json.dumps(custom_format, indent=4))
                return custom_format
        if debug_level > 1:
            print(f"{format_name} not found in {arr_type}!")      
    except FileNotFoundError:
        if debug_level > 1:
            print(f"Warning: File {file_path} not found.")
        return None

    # Return None if the format is not found
    return None

def get_regex(custom_format, specification_name, debug_level=0):
    if not custom_format:
        if debug_level > 1:
            print("Custom format not found.")
        return "Custom format not found."
    # Convert the specification_name to lowercase for case-insensitive comparison
    specification_name = specification_name.lower()
    
    for spec in custom_format.get("specifications", []):
        if spec.get("name").lower() == specification_name:
            for field in spec.get("fields", []):
                if field.get("name").lower() == "value":
                    if debug_level > 1:
                        print(f"Found value for specification '{specification_name}': {field.get('value')}")
                    return field.get("value")
            if debug_level > 1:
                print(f"Specification '{specification_name}' found, but 'value' field not found.")
    if debug_level > 1:
        print(f"Specification '{specification_name}' not found.")
    return "Specification or value field not found."
