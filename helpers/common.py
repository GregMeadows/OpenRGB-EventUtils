
from enum import Enum
import os
from openrgb import OpenRGBClient
from effects import effects_in_use, effects_load, effects_start, effects_stop

class LightingMode(Enum):
    BASIC = 0
    EFFECTS = 1

def save_current_state(client: OpenRGBClient, temp_profile: str = "tmp"):
    """
    Will save the current state of lights.
    If using effects plugin it will stop all effects.
    An enum of the lighting mode is returned so we know what to resume when loading previous state.
    """
    # check if currently using the effects plugin
    if effects_in_use(client):
        effects_stop(client)
        return LightingMode.EFFECTS
    else:
        # Save a temp profile
        client.save_profile(temp_profile)
        return LightingMode.BASIC

def load_previous_state(client: OpenRGBClient, mode: LightingMode, temp_profile: str = "tmp"):
    """
    Loads the previous state of the lights based on the lighting mode.
    """
    if mode == LightingMode.EFFECTS:
         effects_start(client)
    elif mode == LightingMode.BASIC:
        client.load_profile(temp_profile)

def change_working_dir():
    """
    Change working directory to the location of the file
    """
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)