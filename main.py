import vdf
import os
from simple_colors import *
# arrays
shortcuts_folders = []
library_folders = []
appmanifests = []

# functions
def get_shortcuts_path(path):
    path = os.path.expanduser(path) # expands ~/ to /home/<username>

    for child_folder in os.listdir(path):
        child_path = os.path.join(path, child_folder)
        if os.path.isdir(child_path) and any(os.scandir(child_path)):
            config_path = os.path.join(child_path, "config")
            if os.path.exists(config_path):
                shortcuts_path = os.path.join(config_path, "shortcuts.vdf")
                if os.path.exists(shortcuts_path):
                    # print(f"Found: {shortcuts_path}")
                    shortcuts_folders.append(shortcuts_path)


def read_vdf(path):
    path = os.path.expanduser(path) # expands ~/ to /home/<username>
    with open(path, encoding='utf-8') as file:
        return vdf.parse(file)

def read_binary_vdf(path):
    path = os.path.expanduser(path) # expands ~/ to /home/<username>
    with open(path, "rb") as file:
        return vdf.binary_load(file)


# MAIN

print(green("------------- Non Steam Games -------------"))
get_shortcuts_path("~/.local/share/Steam/userdata/")

for file in shortcuts_folders:
    shortcut_data = read_binary_vdf(file)

    print("NonSteamGames: ", vdf.dumps(shortcut_data, pretty=True))

library_data = read_vdf("~/.local/share/Steam/config/libraryfolders.vdf")
loginusers_data = read_vdf("~/.local/share/Steam/config/loginusers.vdf")


# print("LibraryDATA: ", library_data)
# print("LoginUsers: ", loginusers_data)

print(green("------------- Steam Games -------------"))
for key, value in library_data['libraryfolders'].items():
    library_folders.append(value.get('path'))
    print(f"Library {key}: file://{value.get('path')}")



# Search for app manifests in steamapps
for file in library_folders:
    path = os.path.join(file, "steamapps")
    for child_folder in os.listdir(path):
        if child_folder.__contains__("appmanifest"):
            #print("Children: ", child_folder)
            
            appmanifest_path = os.path.join(path, child_folder)
            
            appmanifest_data = read_vdf(appmanifest_path)
            
            appmanifests.append(appmanifest_data)

            appid = appmanifest_data["AppState"]["appid"]
            game_name = appmanifest_data["AppState"]["name"]
            pfx_path = os.path.join(path, f"compatdata/{appid}")

            # right now, it only checks for pfx in the same library folder
            # it should also scan other libraries
            if not (os.path.exists(pfx_path)):
                pfx_path = "NULL err" 
                
            print(red("Name: "), f"{game_name} | {appid}", blue("pfx_path: "), f"file://{pfx_path}")
    
    

