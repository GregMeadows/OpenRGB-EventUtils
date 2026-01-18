import time
from typing import List, Optional
from openrgb import OpenRGBClient, utils
from openrgb.plugins.effects import EffectsPlugin, Effect

def effects_stop(client: OpenRGBClient):
    """
    Iterates through all effects and stops them.
    """
    if effects_plugin := _effects_get_plugin(client):
        for effect in effects_plugin.effects:
            effects_plugin.stop_effect(effect)
        # The app needs a second to send out the stop signal before any other commands should be sent
        time.sleep(0.15)
        effects_plugin.update()

def effects_start(client: OpenRGBClient):
    """
    Iterates through all effects and starts them.
    """
    if effects_plugin := _effects_get_plugin(client):
        for effect in effects_plugin.effects:
            effects_plugin.start_effect(effect)
        # The app needs a second to send out the stop signal before any other commands should be sent
        time.sleep(0.15)
        effects_plugin.update()

def _effects_get_plugin(client: OpenRGBClient) -> Optional[EffectsPlugin]:
    """
    Returns the effects plugin
    """
    if effects_plugin := next((p for p in client.plugins if p.name == "OpenRGB Effects Plugin"), None):
        return EffectsPlugin(effects_plugin)
    return None

def effects_in_use(client: OpenRGBClient) -> bool:
    """
    Returns a boolean as to if there are currently any active effects.
    Returns None if no effects were found.
    """
    effects_plugin = _effects_get_plugin(client)
    # Only return true if there are effects and any are enabled
    if effects_plugin and effects_plugin.effects:
        effects: List[Effect] = effects_plugin.effects
        return any(effect.enabled for effect in effects)
    return False