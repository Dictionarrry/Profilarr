import yaml
import json
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sys
import re

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    ENDC = '\033[0m'

class Apps:
    APP_CHOICES = {
        "1": "radarr",
        "2": "sonarr",
        # Add more apps here as needed
    }

def get_url(instance):
    url = instance['base_url']
    normalized_url = re.sub(r'/$', '', url)
    return normalized_url

def print_message(message, message_type='', newline=True):
    config = load_config()
    ansi_colors = config['settings']['ansi_colors']
    
    if ansi_colors:
        # Initialize color as default.
        color = Colors.ENDC
        message_type = message_type.lower()

        # Assign color based on message type.
        if message_type == 'green':
            color = Colors.GREEN
        elif message_type == 'red':
            color = Colors.RED
        elif message_type == 'yellow':
            color = Colors.YELLOW
        elif message_type == 'blue':
            color = Colors.BLUE
        elif message_type == 'purple':
            color = Colors.PURPLE
        
        # Prepare the end color reset code.
        end_color = Colors.ENDC

        # Print the colored message.
        if newline:
            print(color + message + end_color)
        else:
            print(color + message + end_color, end='')
    else:
        # Print the message without color if ANSI colors are disabled.
        if newline:
            print(message)
        else:
            print(message, end='')



def load_config():
    with open('config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def get_app_choice():
    print_message("Select your app of choice", "blue")
    # Dynamically generate the app selection menu
    app_menu = "\n".join([f"{key}. {value}" for key, value in Apps.APP_CHOICES.items()])
    print_message(app_menu)
    print_message("Enter your choice: ", "blue")
    app_choice = input().strip()

    while app_choice not in Apps.APP_CHOICES.keys():
        print_message("Invalid input. Please enter a valid choice.", "red")
        app_choice = input().strip()

    app = Apps.APP_CHOICES[app_choice]

    return app

def get_instance_choice(app):
    config = load_config() 
    app_instances = config['instances'].get(app.lower(), [])

    print_message(f"Select your {app.capitalize()} instance", "blue")
    # Display instances and prompt for choice
    for i, instance in enumerate(app_instances, start=1):
        print_message(f"{i}. {app.capitalize()} ({instance['name']})")

    print_message("Choose an instance by number, multiple numbers separated by commas or type 'all' for all instances: ", "blue")
    choice = input().strip()
    print()
    selected_instances = []

    if choice.lower() == 'all':
        selected_instances = app_instances
    else:
        choices = choice.split(',')
        for choice in choices:
            choice = choice.strip()  # remove any leading/trailing whitespace
            while not choice.isdigit() or int(choice) < 1 or int(choice) > len(app_instances):
                print_message("Invalid input. Please select a valid number.", "warning")
                choice = input().strip()
            selected_instance = app_instances[int(choice) - 1]
            selected_instances.append(selected_instance)

    return selected_instances

def make_request(request_type, url, api_key, resource_type, json_payload=None):
    full_url = f"{url}/api/v3/{resource_type}"

    headers = {"X-Api-Key": api_key}
    
    try:
        # Make the appropriate request based on the request_type
        if request_type.lower() == 'get':
            response = requests.get(full_url, headers=headers, json=json_payload)
        elif request_type.lower() == 'post':
            response = requests.post(full_url, headers=headers, json=json_payload)
        elif request_type.lower() == 'put':
            response = requests.put(full_url, headers=headers, json=json_payload)
        elif request_type.lower() == 'delete':
            response = requests.delete(full_url, headers=headers)
            return response.status_code
        elif request_type.lower() == 'patch':
            response = requests.patch(full_url, headers=headers, json=json_payload)
        else:
            raise ValueError("Unsupported request type provided.")

        # Process response
        if response.status_code in [200, 201, 202]:
            try:
                return response.json()
            except json.JSONDecodeError:
                print_message("Failed to decode JSON response.", "red")
                return None
        elif response.status_code == 401:
            print_message("Unauthorized. Check your API key.", "red")
            sys.exit()
        elif response.status_code == 409:
            print_message("Conflict detected. The requested action could not be completed.", "red")
        else:
            print_message(f"HTTP Error {response.status_code}.", "red")
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        # Update the message here to suggest checking the application's accessibility
        print_message("Network error. Make sure the application is running and accessible.", "red")
        sys.exit()

    return None

