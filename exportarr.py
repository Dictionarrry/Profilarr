from helpers import *
import os
import re

def prompt_export_choice():
    options = { "1": "Custom Formats", "2": "Quality Profiles" }

    print_message("Please select what you want to export:", "blue")
    for number, option in options.items():
        print_message(f"{number}. {option}", "green")
    print_message("Enter the number(s) of your choice, multiple separated by commas, or type 'all' for all options", "yellow")

    user_choice = input("Your choice: ")

    if user_choice.lower() == 'all':
        return list(options.values())
    else:
        return [options[choice] for choice in user_choice.split(',') if choice in options]

def create_export_path(export_path, app):
    # Convert app to lowercase
    app = app.lower()  # Ensure app is in lowercase
    # Create a directory path for the export in lowercase
    dir_path = os.path.join(export_path, 'custom_formats', app).lower()  # Convert entire path to lowercase

    # Create the directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)

    return dir_path

def export_custom_formats(app, instances, config):


    for instance in instances:
        print_message(f"Exporting Custom Formats for {app.capitalize()} : {instance['name']}", 'blue')
        
        url = get_url(instance)
        api_key = instance['api_key']

        # Get the export path from the config
        export_path = config['settings']['export_path']

        # Create the export directory
        dir_path = create_export_path(export_path, app)

        # Assuming 'export' is a valid resource_type for the API
        response = make_request('get', url, api_key, 'customformat')

        successful_exports = 0  # Counter for successful exports

        # Scrub the JSON data and save each custom format in its own file
        all_custom_formats = []
        for custom_format in response:
            # Remove the 'id' field
            custom_format.pop('id', None)

            all_custom_formats.append(custom_format)
            successful_exports += 1  # Increment the counter if the export was successful

        file_name = f"custom formats ({app.lower()} - {instance['name'].lower()}).json"

        # Save all custom formats to a single file in the export directory
        try:
            with open(os.path.join(dir_path, file_name), 'w') as f:
                json.dump(all_custom_formats, f, indent=4)
            status = 'SUCCESS'
            status_color = 'green'
        except Exception as e:
            status = 'FAILED'
            status_color = 'red'

        print_message(f"Exported {successful_exports} custom formats to {dir_path} for {instance['name']}", 'yellow')
        print()

def create_quality_profiles_export_path(app, config):
    # Get the export path from the config
    export_path = config['settings']['export_path']

    # Create a directory path for the export
    dir_path = os.path.join(export_path, 'quality_profiles', app)

    # Create the directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)

    return dir_path

def export_quality_profiles(app, instances, config):
    for instance in instances:
        print_message(f"Exporting Quality Profiles for {app.capitalize()} : {instance['name']}", 'blue')
        url = get_url(instance)
        api_key = instance['api_key']

        # Create the export directory
        dir_path = create_quality_profiles_export_path(app, config)

        # Assuming 'qualityprofile' is the valid resource_type for the API
        response = make_request('get', url, api_key, 'qualityprofile')

        successful_exports = 0  # Counter for successful exports

        # Scrub the JSON data and save each quality profile in its own file
        for quality_profile in response:
            # Remove the 'id' field
            quality_profile.pop('id', None)

            # Create a file name from the quality profile name and app
            file_name = f"{quality_profile['name']} ({app.lower()} - {instance['name'].lower()}).json"
            file_name = re.sub(r'[\\/*?:"<>|]', '', file_name)  # Remove invalid characters

            # Save the quality profile to a file in the export directory
            try:
                with open(os.path.join(dir_path, file_name), 'w') as f:
                    json.dump([quality_profile], f, indent=4)  # Wrap quality_profile in a list
                status = 'SUCCESS'
                status_color = 'green'
            except Exception as e:
                status = 'FAILED'
                status_color = 'red'
            if status == 'SUCCESS':
                successful_exports += 1  # Increment the counter if the export was successful

        print_message(f"Exported {successful_exports} quality profiles to {dir_path} for {instance['name']}", 'yellow')
        print()

def main():
    app = get_app_choice()
    instances = get_instance_choice(app)
    config = load_config()

    export_custom_formats(app, instances, config)
    export_quality_profiles(app, instances, config)

if __name__ == "__main__":
    main()