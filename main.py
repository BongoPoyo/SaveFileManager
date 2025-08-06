import steam
import vdf



with open('~/.steam/steam/steamapps/libraryfolders.vdf', encoding='utf-8') as f:
    library_data = vdf.load(f)
