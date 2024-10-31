from tkinter import Button, Label, Text, Toplevel

from features.theme import get_theme
from pack import Pack
from screeninfo import get_monitors
from settings import Settings
from state import State
from utils import utils

if utils.is_mac():
    from tkmacosx import Button # Override tkinter's on Mac

class Prompt(Toplevel):
    def __init__(self, settings: Settings, pack: Pack, state: State):
        self.state = state
        if not self.should_init(pack):
            return
        super().__init__()

        self.theme = get_theme(settings)

        self.attributes("-topmost", True)
        utils.set_borderless(self)
        self.configure(background=self.theme.bg)

        monitor = next(m for m in get_monitors() if m.is_primary)
        width = monitor.width // 4
        height = monitor.height // 2
        x = monitor.x + (monitor.width - width) // 2
        y = monitor.y + (monitor.height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        Label(self, text="\n" + pack.prompts.command_text + "\n", fg=self.theme.fg, bg=self.theme.bg).pack()

        prompt = pack.random_prompt()
        Label(self, text=prompt, wraplength=width, fg=self.theme.fg, bg=self.theme.bg).pack()

        input = Text(self, fg=self.theme.text_fg, bg=self.theme.text_bg)
        input.pack()
        button = Button(
            self,
            text=pack.prompts.submit_text,
            command=lambda: self.submit(settings.prompt_max_mistakes, prompt, input.get(1.0, "end-1c")),
            fg=self.theme.fg,
            bg=self.theme.bg,
            activeforeground=self.theme.fg,
            activebackground=self.theme.bg,
        )
        button.place(x=-10, y=-10, relx=1, rely=1, anchor="se")

    def should_init(self, pack: Pack) -> bool:
        if not self.state.prompt_active and pack.has_prompts():
            self.state.prompt_active = True
            return True
        return False

    # Checks that the number of mistakes is at most max_mistakes and if so,
    # closes the prompt window. The number of mistakes is computed as the edit
    # (Levenshtein) distance between a and b.
    # https://en.wikipedia.org/wiki/Levenshtein_distance
    def submit(self, max_mistakes: int, a: str, b: str) -> None:
        d = [[j for j in range(0, len(b) + 1)]] + [[i] for i in range(1, len(a) + 1)]

        for j in range(1, len(b) + 1):
            for i in range(1, len(a) + 1):
                d[i].append(
                    min(
                        d[i - 1][j] + 1,
                        d[i][j - 1] + 1,
                        d[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1)
                    )
                )  # fmt: skip

        if d[len(a)][len(b)] <= max_mistakes:
            self.destroy()
            self.state.prompt_active = False
