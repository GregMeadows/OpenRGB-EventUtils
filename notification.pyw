import os
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
from common import change_working_dir, load_previous_state, save_current_state
from effects import effects_stop

# Configuration
LOG_FILE = "data/notification"
INTERVAL = 300  # 5 minutes in seconds

def check_cooldown():
    current_time = time.time()

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                last_run = float(f.read())
                if current_time - last_run < INTERVAL:
                    return False
            except ValueError as e:
                print(f"Error: {e}")
    
    # Update the file with the new timestamp
    with open(LOG_FILE, "w") as f:
        f.write(str(current_time))

    return True

def flash():
    client = OpenRGBClient()
    try:
        mode = save_current_state(client)
        effects_stop(client)
        client.set_color(RGBColor(255, 0, 0))
        time.sleep(0.2)
        client.set_color(RGBColor(0, 0, 0))
        time.sleep(0.2)
        client.set_color(RGBColor(255, 0, 0))
        time.sleep(0.2)
        client.set_color(RGBColor(0, 0, 0))
        time.sleep(0.1)
        load_previous_state(client, mode)
    except Exception as e:
        print(f"Error: {e}")

def main():
    change_working_dir()

    if check_cooldown():
        flash()

if __name__ == "__main__":
    main()