from pathlib import Path
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
from helpers.common import change_working_dir, load_previous_state, save_current_state

# Configuration
TIME_FILE = "data/notification"
TEMP_PROFILE = "notification"
COOLDOWN = 300  # 5 minutes in seconds
FLASH_COLOR_1 = RGBColor(255, 0, 0) # Red
FLASH_COLOR_2 = RGBColor(0, 0, 0) # Black

def on_cooldown() -> bool:
    """
    Checks if the notification is on cooldown.
    Returns True if on cooldown, False otherwise.
    """
    current_time = time.time()
    time_file = Path(TIME_FILE)
    time_file.parent.mkdir(parents=True, exist_ok=True)

    if time_file.exists():
        try:
            last_run = float(time_file.read_text())
            if current_time - last_run < COOLDOWN:
                return True
        except ValueError as e:
            print(f"Error: {e}")
    
    # Update the file with the new timestamp
    time_file.write_text(str(current_time))

    return False

def flash():
    """
    Flashes the lights to notify the user.
    """
    client = OpenRGBClient()
    try:
        mode = save_current_state(client, TEMP_PROFILE)
        for i in range(2):
            client.set_color(FLASH_COLOR_1)
            time.sleep(0.2)
            client.set_color(FLASH_COLOR_2)
            time.sleep(0.2)
        load_previous_state(client, mode, TEMP_PROFILE)
    except Exception as e:
        print(f"Error: {e}")

def main():
    change_working_dir()
    if not on_cooldown():
        flash()

if __name__ == "__main__":
    main()