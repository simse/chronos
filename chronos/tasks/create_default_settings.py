from chronos.settings import get_setting, set_setting


def run(arguments, event):
    set_default_setting("appearance", "dark")
    set_default_setting("authentication", False)

    return


def set_default_setting(key, value):
    if get_setting(key) is None:
        set_setting(key, value)
