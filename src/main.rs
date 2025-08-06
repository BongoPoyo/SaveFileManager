use std::fs::{self, DirEntry, File};
use std::io;
use std::path::Path;
use colored::Colorize;

static LIBRARY_FOLDERS_VDF : &str = "~/.steam/steam/config/libraryfolders.vdf";
static LOGGED_IN_USERS_VDF : &str = "~/.steam/steam/config/loginusers.vdf.vdf";
macro_rules! logln {
    ($($arg:tt)*) => {
        println!(
            "{} {}",
            "[Main]".bold().red(),
            format!($($arg)*)
        );
    };
}

fn main() {
    for entry in fs::read_dir(Path::new("~/.steam/steam/userdata/[USER_ID]/config/shortcuts.vdf")) {
        logln!("Entry: {:?}", entry);
    }
}
