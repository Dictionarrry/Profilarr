from helpers import *
import os
import fnmatch
import json

def get_custom_formats(app):
    config = load_config()
    import_path = f"{config['settings']['import_path']}/custom_formats/{app.lower()}"  # Adjusted path
    for file in os.listdir(import_path):
        if fnmatch.fnmatch(file, f'*{app}*'):
            return file
    return None


def process_format(format, existing_names_to_id, base_url, api_key):
    format_name = format['name']
    if format_name in existing_names_to_id:
        format_id = existing_names_to_id[format_name]
        response = make_request('put', base_url, api_key, f'customformat/{format_id}', format)
        if response is not None:
            print_message(f"Updating custom format '{format_name}'", "yellow", newline=False)
            print_message(" : SUCCESS", "green")
            return 0, 1
        else:
            print_message(f"Updating custom format '{format_name}'", "yellow", newline=False)
            print_message(" : FAIL", "red", newline=False)
    else:
        response = make_request('post', base_url, api_key, 'customformat', format)
        if response is not None:
            print_message(f"Adding custom format '{format_name}'", "blue", newline=False)
            print_message(" : SUCCESS", "green")
            return 1, 0
        else:
            print_message(f"Adding custom format '{format_name}'", "blue", newline=False)
            print_message(" : FAIL", "red", newline=False)
    return 0, 0

def import_custom_formats(app, instances):

    config = load_config()

    for instance in instances:
        api_key = instance['api_key']
        base_url = get_url(instance)

        existing_formats = make_request('get', base_url, api_key, 'customformat')
        existing_names_to_id = {format['name']: format['id'] for format in existing_formats}

        app_file = get_custom_formats(app)
        if app_file is None:
            print_message(f"No file found for app: {app}", "red")
            continue

        added_count, updated_count = 0, 0
        with open(f"{config['settings']['import_path']}/custom_formats/{app.lower()}/{app_file}", 'r') as import_file:
            import_formats = json.load(import_file)

        print_message(f"Importing custom formats to {app.capitalize()} : {instance['name']}", "purple")
        print()

        for format in import_formats:
            added, updated = process_format(format, existing_names_to_id, base_url, api_key)
            added_count += added
            updated_count += updated

        print()
        print_message(
            f"Successfully added {added_count} custom formats, "
            f"updated {updated_count} custom formats.", 
            "purple"
        )
        print()

def get_profiles(app):
    config = load_config()
    import_path = f"{config['settings']['import_path']}/quality_profiles/{app.lower()}"  # Adjusted path
    matching_files = []  # Create an empty list to hold matching files
    for file in os.listdir(import_path):
        if fnmatch.fnmatch(file, f'*{app}*'):
            matching_files.append(file)  # Add matching file to the list
    return matching_files  # Return the list of matching files

def get_existing_profiles(base_url, api_key):
    resource_type = 'qualityprofile'
    existing_profiles = make_request('get', base_url, api_key, resource_type)

    
    return {profile['name']: profile for profile in existing_profiles} if existing_profiles else {}

def cf_import_sync(instances):
    for instance in instances:
        api_key = instance['api_key']
        base_url = get_url(instance)
        resource_type = 'customformat'
        response = make_request('get', base_url, api_key, resource_type)
        
        if response:
            instance['custom_formats'] = {format['name']: format['id'] for format in response}
        else:
            print_message("No custom formats found for this instance.", "purple")
            print()

def user_select_profiles(profiles):
    print_message("Available profiles:", "purple")
    for idx, profile in enumerate(profiles, start=1):
        print(f"{idx}. {profile}")
    print()

    while True:
        # Display prompt message
        print_message("Enter the numbers of the profiles you want to import separated by commas, or type 'all' to import all profiles: ", "blue", newline=False)
        print()
        user_input = input().strip()

        if user_input.lower() == 'all':
            return profiles  # Return all profiles if 'all' is selected

        selected_profiles = []
        try:
            selected_indices = [int(index.strip()) for index in user_input.split(',')]
            for index in selected_indices:
                if 1 <= index <= len(profiles):
                    selected_profiles.append(profiles[index - 1])
                else:
                    raise ValueError(f"Invalid selection: {index}. Please enter valid numbers.")  # Raise an error to trigger except block
            return selected_profiles  # Return the selected profiles if all inputs are valid
        except ValueError as e:
            print_message(str(e), "red")  # Display error message in red



def process_profile(profile, base_url, api_key, custom_formats, existing_profiles):
    profile_name = profile.get('name')
    existing_profile = existing_profiles.get(profile_name)

    # Update or add custom format items as needed
    if 'formatItems' in profile:
        for format_item in profile['formatItems']:
            format_name = format_item.get('name')
            if format_name and format_name in custom_formats:
                format_item['format'] = custom_formats[format_name]

    for format_name, format_id in custom_formats.items():
        if format_name not in {item.get('name') for item in profile.get('formatItems', [])}:
            profile.setdefault('formatItems', []).append({
                "format": format_id,
                "name": format_name,
                "score": 0
            })

    if existing_profile:
        profile['id'] = existing_profile['id']
        action = "Updating"
        action_color = "yellow"
        resource_type = f"qualityprofile/{profile['id']}"
    else:
        action = "Adding"
        action_color = "blue"
        resource_type = "qualityprofile"

    response = make_request('put' if existing_profile else 'post', base_url, api_key, resource_type, profile)

    # Print the action statement in blue for Adding and yellow for Updating
    print_message(f"{action} '{profile_name}' quality profile", action_color, newline=False)

    # Determine the status and print the status in green (OK) or red (FAIL)
    if response:
        print_message(" : SUCCESS", "green")
    else:
        print_message(" : FAIL", "red")

def import_quality_profiles(app, instances):

    config = load_config()

    cf_import_sync(instances)

    all_profiles = get_profiles(app)
    selected_profiles_names = user_select_profiles(all_profiles)

    for instance in instances:
        base_url = get_url(instance)
        api_key = instance['api_key']
        custom_formats = instance.get('custom_formats', {})
        existing_profiles = get_existing_profiles(base_url, api_key)  # Retrieve existing profiles

        print_message(f"Importing Quality Profiles to {app} : {instance['name']}", "purple")
        print()

        for profile_file in selected_profiles_names:
            with open(f"{config['settings']['import_path']}/quality_profiles/{app.lower()}/{profile_file}", 'r') as file:
                try:
                    quality_profiles = json.load(file)
                except json.JSONDecodeError as e:
                    print_message(f"Error loading selected profile: {e}", "red")
                    continue

                for profile in quality_profiles:
                    process_profile(profile, base_url, api_key, custom_formats, existing_profiles)
        
        print()

def main():
    app = get_app_choice()
    instances = get_instance_choice(app)

    import_custom_formats(app, instances)
    import_quality_profiles(app, instances)

if __name__ == "__main__":
    main()