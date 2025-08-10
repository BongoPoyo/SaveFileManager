from textual.reactive import reactive
from time import monotonic
from textual.app import App, ComposeResult
import os
import re
import variables
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup, Horizontal
from textual.widgets import Button, Placeholder, Footer, Header, Label, TabPane, TabbedContent
import subprocess


class DefaultPrefixesView(HorizontalGroup):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if not button_id:
            return

        if button_id == "def_wine_pfx":
            subprocess.run(
                ["xdg-open", os.path.expanduser("~/.wine")], check=False)
        elif button_id == "def_umu_pfx":
            subprocess.run(
                ["xdg-open", os.path.expanduser("~/Games/umu/umu-default/")], check=False)
        elif button_id == "def_lutris_pfx":
            subprocess.run(
                ["xdg-open", os.path.expanduser("~/Games/")], check=False)
        elif button_id.__contains__("library"):
            match = re.search(r'\d+$', button_id)  # find digits at end
            num = 0
            if match:
                num = int(match.group())  # → 0

            path = variables.library_folders[num]
            subprocess.run(
                ["xdg-open", os.path.expanduser(path)], check=False)

    def compose(self) -> ComposeResult:
        yield Button("Default Wine Prefix", id="def_wine_pfx")
        yield Button("Open Umu prefix", id="def_umu_pfx")
        yield Button("Open Lutris prefix", id="def_lutris_pfx")

        for key, value in variables.library_data['libraryfolders'].items():
            yield Button("Steam Library " + key, id=f"library{key}")


class SteamGameView(VerticalGroup):
    def compose(self) -> ComposeResult:
        for steam_game in variables.steam_games:
            with Horizontal():
                yield Button(steam_game.app_id)
                # yield Label(steam_game.app_id),
                yield Button(steam_game.game_name)

            # yield Button(steam_game.game_name)


class SaveManagerApp(App):
    CSS_PATH = "ui.css"

    BINDINGS = [("q", "quit", "Quit app"),
                ("1", "default_tab", "Default Tab"),
                ("2", "steam_tab", "Steam Tab"),
                ("3", "non_steam_tab", "Non Steam Tab"),
                ("4", "lutris_tab", "Lutris Tab"),
                ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with TabbedContent():
            with TabPane("Default", id="default_tab"):
                yield VerticalScroll(DefaultPrefixesView())
            with TabPane("SteamGames", id="steam_tab"):
                yield VerticalScroll(SteamGameView())
            with TabPane("NonSteamGames", id="non_steam_tab"):
                yield VerticalScroll()
            with TabPane("LutrisGames", id="lutris_tab"):
                yield VerticalScroll()

    # Tab Switching
    def action_default_tab(self) -> None:
        self.query_one(TabbedContent).active = "default_tab"

    def action_steam_tab(self) -> None:
        self.query_one(TabbedContent).active = "steam_tab"

    def action_non_steam_tab(self) -> None:
        self.query_one(TabbedContent).active = "non_steam_tab"

    def action_lutris_tab(self) -> None:
        self.query_one(TabbedContent).active = "lutris_tab"

    def on_mount(self) -> None:
        self.title = "SaveManager"


# if __name__ == "__main__":
#     app = SaveManagerApp()
#     app.run()
