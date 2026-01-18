import argparse
import os
from openrgb import OpenRGBClient
from helpers.common import LightingMode, change_working_dir, load_previous_state, save_current_state
from helpers.effects import effects_stop

# Configuration
LOG_FILE = "data/idle"

def start_idle(client: OpenRGBClient):
    try:
        # Get current mode and save it
        mode = save_current_state(client, "idle")
        with open(LOG_FILE, 'w') as output:
            output.write(str(mode.name))

        # Stop all effects and turn off lights
        effects_stop(client)
        client.clear()

    except Exception as e:
        print(f"Error: {e}")

def stop_idle(client: OpenRGBClient):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                # Set the mode based on idle file
                stored_mode = f.read().strip()
                try:
                    mode = LightingMode[stored_mode]
                    load_previous_state(client, mode, "idle")
                except KeyError:
                    print(f"Error: '{stored_mode}' is not a valid key in LightingMode.")
            except ValueError as e:
                print(f"Error: {e}")

def main():
    # Arguments
    parser = argparse.ArgumentParser(description="Idle script")
    parser.add_argument("action", choices=["start", "stop"], help="Start or stop idle state")
    args = parser.parse_args()

    change_working_dir()

    client = OpenRGBClient()

    # Call method based on argument
    if args.action == "start":
        start_idle(client)
    elif args.action == "stop":
        stop_idle(client)

if __name__ == "__main__":
    main()