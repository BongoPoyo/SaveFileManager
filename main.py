# import steam
import vdf

file_path = "/home/hashir/.local/share/Steam/userdata/0/config/compat.vdf"

with open(file_path, encoding='utf-8') as f:
    library_data = vdf.load(f)

print("LibraryDATA: ", library_data)
