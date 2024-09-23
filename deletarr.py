from helpers import *

def user_select_items_to_delete(items):
    """
    Prompts the user to select items to delete from a given list of items.
    Each item in the list is expected to be a dictionary with at least an 'id' and 'name' key.
    """
    print_message("Available items to delete:", "purple")
    for index, item in enumerate(items, start=1):
        print_message(f"{index}. {item['name']}", "green")

    print_message("Enter the number(s) of the items you wish to delete, separated by commas, or type 'all' for all:", "yellow")
    user_input = input("Your choice: ").strip().lower()
    selected_items = []

    if user_input == 'all':
        return items
    else:
        indices = user_input.split(',')
        for index in indices:
            try:
                index = int(index.strip()) - 1
                if 0 <= index < len(items):
                    selected_items.append(items[index])
                else:
                    print_message("Invalid selection, ignoring.", "red")
            except ValueError:
                print_message("Invalid input, please enter numbers only.", "red")

    return selected_items


def prompt_export_choice():
    """
    Prompt user to choose between exporting Custom Formats, Quality Profiles, or both.
    Returns a list of choices.
    """
    print_message("Please select what you want to delete:", "blue")
    options = {"1": "Custom Formats", "2": "Quality Profiles", "3": "Both"}
    for key, value in options.items():
        print_message(f"{key}. {value}", "green")
    choice = input("Enter your choice: ").strip()

    # Validate choice
    while choice not in options:
        print_message("Invalid choice, please select a valid option:", "red")
        choice = input("Enter your choice: ").strip()

    if choice == "3":
        return ["Custom Formats", "Quality Profiles"]
    else:
        return [options[choice]]

def delete_custom_formats_or_profiles(app, instance, item_type, config):
    """
    Deletes either custom formats or quality profiles based on the item_type.
    """
    api_key = instance['api_key']
    base_url = get_url(instance)
    resource_type = item_type  # 'customformat' or 'qualityprofile'

    if item_type == 'customformat':
        type = 'Custom Format'
    elif item_type == 'qualityprofile':
        type = 'Quality Profile'

    # Fetch items to delete
    items = make_request('get', base_url, api_key, resource_type)
    if items is None or not isinstance(items, list):
        return

    # Assuming a function to select items to delete. It could list items and ask the user which to delete.
    items_to_delete = user_select_items_to_delete(items)  # This needs to be implemented or adapted

    # Proceed to delete selected items
    for item in items_to_delete:
        item_id = item['id']
        item_name = item['name']
        print_message(f"Deleting {type} ({item_name})", "blue", newline=False)
        response = make_request('delete', base_url, api_key, f"{resource_type}/{item_id}")
        if response in [200, 202, 204]:
            print_message(" : SUCCESS", "green")
        else:
            print_message(" : FAIL", "red")

def main():
    app = get_app_choice()
    instances = get_instance_choice(app)
    config = load_config()

    choices = prompt_export_choice()
    for instance in instances:
        for choice in choices:
            if choice == "Custom Formats":
                delete_custom_formats_or_profiles(app, instance, 'customformat', config)
            elif choice == "Quality Profiles":
                delete_custom_formats_or_profiles(app, instance, 'qualityprofile', config)


if __name__ == "__main__":
    main()
