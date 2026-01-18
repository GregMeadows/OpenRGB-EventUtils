import time
from typing import List
from openrgb import OpenRGBClient, utils
from openrgb.plugins.effects import EffectsPlugin, Effect

def effects_load(client: OpenRGBClient, profile_name: str):
    """
    Sends a command to the OpenRGB Effects Plugin to load a specific profile.
    """
    effects_plugin = _effects_get_plugin(client)
    # ID 23 = NET_PACKET_ID_LOAD_EFFECTS_PROFILE
    data = utils.pack_string(profile_name)
    effects_plugin.send_packet(23, data)

def effects_stop(client: OpenRGBClient):
    """
    Iterates through all effects and stops them.
    """
    effects_plugin = _effects_get_plugin(client)
    for effect in effects_plugin.effects:
        effects_plugin.stop_effect(effect)
    # The app needs a second to send out the stop signal before any other commands should be sent
    time.sleep(0.15)
    effects_plugin.update()

def effects_start(client: OpenRGBClient):
    """
    Iterates through all effects and starts them.
    """
    effects_plugin = _effects_get_plugin(client)
    for effect in effects_plugin.effects:
        effects_plugin.start_effect(effect)
    # The app needs a second to send out the stop signal before any other commands should be sent
    time.sleep(0.15)
    effects_plugin.update()

def _effects_get_plugin(client: OpenRGBClient) -> EffectsPlugin:
    """
    Returns the effects plugin
    """
    effects_plugin = next((p for p in client.plugins if p.name == "OpenRGB Effects Plugin"), None)
    if not effects_plugin:
        raise RuntimeError("OpenRGB Effects Plugin not found or not enabled.")
    return EffectsPlugin(effects_plugin)

def effects_in_use(client: OpenRGBClient):
    """
    Returns a boolean as to if there are currently any active effects.
    Returns None if no effects were found.
    """
    effects_plugin = _effects_get_plugin(client)
    # Only send stop package if effects are present
    if len(effects_plugin.effects) > 0:
        effects: List[Effect] = effects_plugin.effects
        return any(effect.enabled for effect in effects)
    return None