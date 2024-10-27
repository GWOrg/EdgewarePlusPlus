from pathlib import Path
from tkinter import Toplevel

import os
import shlex
import subprocess
import sys

try:
    import vlc
except FileNotFoundError:
    # Defined for type hints
    class vlc:
        MediaPlayer = None


def set_borderless(window: Toplevel) -> None:
    pass


def set_wallpaper(wallpaper: Path) -> None:
    if isinstance(wallpaper, Path):
        wallpaper_path = str(wallpaper.absolute())

    try:

        SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

        subprocess.Popen(SCRIPT % wallpaper_path, shell=True)
        return True
    except:
        sys.stderr.write("ERROR: Failed to set wallpaper. There might be a bug.\n")
        return False


def set_vlc_window(player: vlc.MediaPlayer, window_id: int) -> None:
    player.set_nsobject(window_id)


def open_directory(url: str) -> None:
    subprocess.run(["open", "-R", url])


def make_shortcut(
    title: str, process: Path, icon: Path, location: Path | None = None
) -> None:
    filename = f"{title}.command"
    file = (location if location else Path(os.path.expanduser("~/Desktop"))) / filename
    content = f"""#!/bin/zsh
    {shlex.join([str(sys.executable), str(process)])}
    """

    try:
        file.write_text(content)
        os.chmod(file, 0o755)  # Need to make sure the shortcut is executable
    except Exception as e:
        print(f"Shortcut error.\n\nReason: {e}")
        return False
    return True


def toggle_run_at_startup(state: bool) -> None:
    pass
