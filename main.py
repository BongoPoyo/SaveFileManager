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




# Necessary as there can be multiple compatdatas
def get_pfx_paths(file, u_appid):
    pfx_paths = ""
    for file in library_folders:
        path = os.path.join(file, f"steamapps/compatdata/{u_appid}")
        # print("Path: ", path)
        if os.path.exists(path):
            pfx_paths = pfx_paths + " file://" + path

    return pfx_paths

# MAIN


      


library_data = read_vdf("~/.local/share/Steam/config/libraryfolders.vdf")
loginusers_data = read_vdf("~/.local/share/Steam/config/loginusers.vdf")

print(green("------------- Steam Libraries -------------"))
for key, value in library_data['libraryfolders'].items():
    library_folders.append(value.get('path'))
    print(f"Library {key}: file://{value.get('path')}")



# print("LibraryDATA: ", library_data)
# print("LoginUsers: ", loginusers_data)

print(green("------------- Steam Games -------------"))


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
            
            

            
            pfx_path = get_pfx_paths(file, appid) 

           

                
            print(red("Name: "), f"{game_name} | {appid}", blue("pfx_path: "), pfx_path)
print(green("------------- Non Steam Games -------------"))
get_shortcuts_path("~/.local/share/Steam/userdata/")

for file in shortcuts_folders:
    #shortcut_data = read_binary_vdf(file)
    #print("NonSteamGames: ", vdf.dumps(shortcut_data, pretty=True))
    with open(file, "rb") as sf:
     shortcuts = vdf.binary_load(sf)
    root = shortcuts['shortcuts']
    for key,entry in root.items():
        # Uncomment to see everything in each shortcut:
        # print(entry)

        exe = entry.get('Exe')
        name = entry.get('AppName')
        appid = entry.get('appid') # signed
        u_appid = appid & 0xFFFFFFFF #unsigned
        

        pfx_path = get_pfx_paths(file, u_appid) 


        print(red("Name: "), f"{name} | {u_appid}", blue("pfx_path: "), pfx_path)

   
    

