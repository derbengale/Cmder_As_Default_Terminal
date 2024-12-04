import json
import os
import shutil
import subprocess
from glob import glob


def set_environment_variables():
    # Get the folder where the script is located
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Define the environment variables
    conemu_dir = os.path.join(current_folder, "vendor", "conemu-maximus5")
    cmd_root = current_folder

    # Use setx to set the environment variables permanently
    subprocess.run(["setx", "ConEmuDir", conemu_dir], shell=True, check=True)
    subprocess.run(["setx", "CMDER_ROOT", cmd_root], shell=True, check=True)

    print("Environment variables have been set permanently:")
    print(f"ConEmuDir={conemu_dir}")
    print(f"CMDER_ROOT={cmd_root}")

def add_cmder_profile_and_set_default():
    # Locate the settings.json file
    base_path = os.path.expanduser(r"~\AppData\Local\Packages")
    terminal_folder = next((folder for folder in glob(os.path.join(base_path, "Microsoft.WindowsTerminal*"))), None)
    
    if not terminal_folder:
        raise FileNotFoundError("Microsoft.WindowsTerminal folder not found in Packages.")

    settings_path = os.path.join(terminal_folder, "LocalState", "settings.json")
    
    if not os.path.exists(settings_path):
        raise FileNotFoundError(f"settings.json not found at {settings_path}")
    
    # Back up settings.json
    current_folder = os.path.dirname(os.path.abspath(__file__))
    backup_path = os.path.join(current_folder, "settings.json.bak")
    
    shutil.copy2(settings_path, backup_path)
    print(f"Backup of settings.json created at {backup_path}")

    # Define the new profile
    new_profile_guid = "{6d953325-a939-475d-a151-940cbd0302fb}"
    new_profile = {
        "guid": new_profile_guid,
        "name": "Cmder",
        "commandline": "cmd.exe /k %CMDER_ROOT%\\vendor\\init.bat",
        "startingDirectory": "%USERPROFILE%",
        "icon": "%CMDER_ROOT%\\icons\\cmder.ico",
        "background": "#2e3436",
        "padding": "15",
        "fontFace": "Cascadia Code",
        "fontSize": 10
    }
    
    # Load the existing settings.json
    with open(settings_path, 'r', encoding='utf-8') as file:
        settings_data = json.load(file)
    
    # Add the new profile if not already present
    profiles = settings_data.get("profiles", {}).get("list", [])
    if not any(profile.get("guid") == new_profile["guid"] for profile in profiles):
        profiles.append(new_profile)
        settings_data["profiles"]["list"] = profiles
    
    # Set the defaultProfile to the new profile's GUID
    settings_data["defaultProfile"] = new_profile_guid
    
    # Save the updated settings.json
    with open(settings_path, 'w', encoding='utf-8') as file:
        json.dump(settings_data, file, indent=4)
    
    print(f"Cmder profile added and set as the default profile in {settings_path}")

if __name__ == "__main__":
    set_environment_variables()
    add_cmder_profile_and_set_default()
