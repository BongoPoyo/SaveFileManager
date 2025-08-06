use colored::Colorize;
use std::ffi::OsString;
use std::fs::OpenOptions;
use std::path::{Path, PathBuf};
mod steam_vdf;
//static LOGGED_IN_USERS_VDF: &str = ".local/share/Steam/config/loginusers.vdf";
//static CUSTOM_GAMES_VDF: &str = ".steam/steam/userdata/[USER_ID]/config/shortcuts.vdf";
macro_rules! logln {
    ($($arg:tt)*) => {
        println!(
            "{} {}",
            "[Main]".bold().red(),
            format!($($arg)*)
        )
    };
}

fn main() {
    let home = std::env::var("HOME").expect("HOME not set");
    let libraryfolders_path = PathBuf::from(format!(
        "{}/.local/share/Steam/config/libraryfolders.vdf",
        home
    ));

    logln!("Path: {:?}", libraryfolders_path);
    let mut file = OpenOptions::new()
        .read(true)
        .open(libraryfolders_path)
        .expect("Couldnt open file");

    if let Ok(data) = steam_vdf::read_data(&mut file) {
        if let Some(mut base_valve_data) = data {
            match &mut base_valve_data {
                &mut steam_vdf::ValveData::List(ref base_name, ref mut base_contents) => {
                    assert_eq!(*base_name, OsString::from("libraryfolders"));
                    for shortcut in base_contents.iter() {
                        if let &steam_vdf::ValveData::List(
                            ref shortcut_name,
                            ref shortcut_contents,
                        ) = shortcut
                        {
                            logln!("Shortcut: {:?}", shortcut_name);
                            for content in shortcut_contents {
                                match content {
                                    &steam_vdf::ValveData::List(ref prop_name, _) => {
                                        logln!("Name: {:?}; Value: [List]", prop_name);
                                    }
                                    &steam_vdf::ValveData::String(
                                        ref prop_name,
                                        ref prop_content,
                                    ) => {
                                        logln!("Name: {:?}; Value: {:?}", prop_name, prop_content);
                                    }
                                    &steam_vdf::ValveData::Bytes4(
                                        ref prop_name,
                                        ref prop_content,
                                    ) => {
                                        logln!(
                                            "Name: {:?}; Value: {:02X}{:02X}{:02X}{:02X}",
                                            prop_name,
                                            prop_content[0],
                                            prop_content[1],
                                            prop_content[2],
                                            prop_content[3]
                                        );
                                    }
                                    &steam_vdf::ValveData::EndOfList => {
                                        logln!("EndOfList");
                                    }
                                }
                            }
                        }
                    }
                    base_contents.pop();
                }
                _ => logln!("base data was not a list."),
            }
        }
    }
    // for entry in fs::read_dir(Path::new(LIBRARY_FOLDERS_VDF))
    //     .expect("Can't find ~/.steam/steam/config/libraryfolders.vdf")
    // {
    //     let entry: DirEntry = entry.expect("DirEntry doesnt exist");
    //     logln!("Entry: {:?}", entry);
    // }
}
