import ast
import json
import os
import shutil

from paths import Assets, Data


def load_config() -> dict:
    if not os.path.exists(Data.CONFIG):
        Data.ROOT.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Assets.DEFAULT_CONFIG, Data.CONFIG)

    with open(Data.CONFIG) as f:
        config = json.loads(f.read())

    return config


def load_default_config() -> dict:
    with open(Assets.DEFAULT_CONFIG) as f:
        default_config = json.loads(f.read())

    return default_config


class Settings:
    def __init__(self):
        config = load_config()

        # Impacts other settings
        lowkey_mode = bool(config["lkToggle"])

        # General
        self.theme = config["themeType"]
        self.startup_splash = bool(config["showLoadingFlair"])
        self.panic_key = config["panicButton"]

        # Popups
        self.delay = int(config["delay"])  # Milliseconds
        self.image_chance = int(config["popupMod"])  # 0 to 100
        self.opacity = int(config["lkScaling"]) / 100  # Float between 0 and 1
        self.timeout_enabled = bool(config["timeoutPopups"]) or lowkey_mode
        self.timeout = int(config["popupTimeout"]) * 1000 if not lowkey_mode else self.delay  # Milliseconds
        self.buttonless = bool(config["buttonless"])
        self.single_mode = bool(config["singleMode"])

        # Overlays
        self.denial_chance = int(config["denialChance"]) if bool(config["denialMode"]) else 0  # 0 to 100
        self.subliminal_chance = int(config["subliminalsChance"]) if bool(config["popupSubliminals"]) else 0  # 0 to 100
        self.max_subliminals = int(config["maxSubliminals"])
        self.subliminal_opacity = int(config["subliminalsAlpha"]) / 100  # Float between 0 and 1

        # Web
        self.web_chance = int(config["webMod"])  # 0 to 100
        self.web_on_popup_close = bool(config["webPopup"]) and not lowkey_mode

        # Prompt
        self.prompt_chance = int(config["promptMod"])  # 0 to 1000
        self.prompt_max_mistakes = int(config["promptMistakes"])

        # Audio
        self.audio_chance = int(config["audioMod"])  # 0 to 100
        self.max_audio = int(config["maxAudio"]) if bool(config["maxAudioBool"]) else float("inf")

        # Video
        self.video_chance = int(config["vidMod"])  # 0 to 100
        self.video_volume = int(config["videoVolume"])  # 0 to 100
        self.max_video = int(config["maxVideos"]) if bool(config["maxVideoBool"]) else float("inf")
        self.vlc_mode = bool(config["vlcMode"])

        # Captions
        self.captions_in_popups = bool(config["showCaptions"])
        self.caption_popup_chance = int(config["capPopChance"])  # 0 to 100
        self.caption_popup_opacity = int(config["capPopOpacity"]) / 100  # Float between 0 and 1
        self.caption_popup_timeout = int(config["capPopTimer"])  # Milliseconds

        # Wallpaper
        self.rotate_wallpaper = bool(config["rotateWallpaper"])
        self.wallpaper_timer = int(config["wallpaperTimer"]) * 1000  # Milliseconds
        self.wallpaper_variance = int(config["wallpaperVariance"]) * 1000  # Milliseconds
        self.wallpapers = list(ast.literal_eval(config["wallpaperDat"]).values())  # TODO: Can fail, store in a better way

        # Dangerous
        self.drive_avoid_list = config["avoidList"].split(">")  # TODO: Can fail, store in a better way
        self.fill_drive = bool(config["fill"])
        self.drive_path = config["drivePath"]
        self.fill_delay = int(config["fill_delay"]) * 10  # Milliseconds
        self.replace_images = bool(config["replace"])
        self.replace_threshold = int(config["replaceThresh"])
        self.panic_disabled = bool(config["panicDisabled"])
        self.show_on_discord = bool(config["showDiscord"])

        # Basic modes
        self.lowkey_mode = lowkey_mode
        self.lowkey_corner = int(config["lkCorner"])
        self.moving_chance = int(config["movingChance"])  # 0 to 100
        self.moving_speed = int(config["movingSpeed"])
        self.moving_random = bool(config["movingRandom"])

        # Dangerous modes
        self.timer_mode = bool(config["timerMode"])
        self.timer_time = int(config["timerSetupTime"]) * 60 * 1000  # Milliseconds
        self.timer_password = config["safeword"]
        self.mitosis_mode = bool(config["mitosisMode"]) or self.lowkey_mode
        self.mitosis_strength = int(config["mitosisStrength"]) if not self.lowkey_mode else 1

        # Hibernate mode
        self.hibernate_mode = bool(config["hibernateMode"])
        self.hibernate_fix_wallpaper = bool(config["fixWallpaper"]) and self.hibernate_mode
        self.hibernate_type = config["hibernateType"]
        self.hibernate_delay_min = int(config["hibernateMin"]) * 1000  # Milliseconds
        self.hibernate_delay_max = int(config["hibernateMax"]) * 1000  # Milliseconds
        self.hibernate_activity = int(config["wakeupActivity"])
        self.hibernate_activity_length = int(config["hibernateLength"]) * 1000  # Milliseconds
        # TODO: Pump-scare audio
        # self.pump_scare_offset = int(config["pumpScareOffset"])  # Seconds
