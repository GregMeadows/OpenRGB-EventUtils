import argparse
from pathlib import Path
from openrgb import OpenRGBClient
from helpers.common import LightingMode, change_working_dir, load_previous_state, save_current_state
from helpers.effects import effects_stop

# Configuration
MODE_FILE = "data/idle"
TEMP_PROFILE = "idle"

def start_idle(client: OpenRGBClient):
    try:
        # Get current mode and save it
        mode = save_current_state(client, TEMP_PROFILE)

        # Update the file with the new mode
        mode_file = Path(MODE_FILE)
        mode_file.parent.mkdir(parents=True, exist_ok=True)
        mode_file.write_text(str(mode.name))

        client.clear()
    except Exception as e:
        print(f"Error: {e}")

def stop_idle(client: OpenRGBClient):
    mode_file = Path(MODE_FILE)
    mode_file.parent.mkdir(parents=True, exist_ok=True)

    if mode_file.exists():
        try:
            # Read the stored mode
            stored_mode = mode_file.read_text().strip()
            try:
                mode = LightingMode[stored_mode]
                load_previous_state(client, mode, TEMP_PROFILE)
            except KeyError:
                print(f"Error: '{stored_mode}' is not a valid key in LightingMode.")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Error: Idle does not exist.")

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