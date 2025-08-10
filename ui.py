from textual.reactive import reactive
from time import monotonic
from textual.app import App, ComposeResult
import os
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Digits, Footer, Header, Label, Tab, TabbedContent
TABS = [
    "Default prefixes",
    "Steam Games",
    "NonSteam Games",
    "Lutris Games",
]


class TimeDisplay(Digits):
    """A widget to display elapsed time."""

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(
            1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.total = 0
        self.time = 0


class Stopwatch(HorizontalGroup):
    """A stopwatch widget."""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            time_display.start()
            self.add_class("started")
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay()


class DefaultPrefixesView(HorizontalGroup):
    """Default prefixes and steam libraries"""
    label_name: str
    path: str

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "open_pfx":
            self.add_class("started")

    def compose(self) -> ComposeResult:
        yield Button("", id="name")
        yield Button("Open Pfx", id="open_pfx", variant="success")

    def on_mount(self) -> None:
        self.query_one("#name").label = from_text(self.label_name)
        pass


class SteamGameView(HorizontalGroup):
    """A way to veiw steam games"""

    def compose(self) -> ComposeResult:
        yield Label("GameName")


class SaveManagerApp(App):
    CSS_PATH = "ui.css"
    # BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
    #            ("q", "quit", "Quit app")]
    BINDINGS = [("q", "quit", "Quit app"),
                ("a", "add_stopwatch", "Add stopwatch"),
                ("r", "remove_stopwatch", "Remove Stopwatch"),
                ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

        with TabbedContent(TABS[0], TABS[1], TABS[2], TABS[3]):
            yield VerticalScroll(id="default_prefixes")
            yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")
            yield Label()
            yield Label()

    #
    # def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
    #     """Handle TabActivated message sent by Tabs."""
    #     label = self.query_one(Label)
    #     if event.tab is None:
    #         # When the tabs are cleared, event.tab will be None
    #         label.visible = False
    #     else:
    #         label.visible = True
    #         label.update(event.tab.label)

    def action_add_stopwatch(self) -> None:
        """An action to add a timer."""
        new_stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        """Called to remove a timer."""
        timers = self.query("Stopwatch")
        if timers:
            timers.last().remove()

    def on_mount(self) -> None:
        # tabs = self.query_one(Tabs)
        # tabs.focus()

        self.title = "SaveManager"
        # spawn default_prefixes
        new_prefix = DefaultPrefixesView()
        new_prefix.label_name = "Wine Prefix"
        new_prefix.path = f"file://{os.path.expanduser("~/.wine")}"
        self.query_one("#default_prefixes").mount(new_prefix)


if __name__ == "__main__":
    app = SaveManagerApp()
    app.run()
