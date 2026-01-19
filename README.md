# OpenRGB-EventUtils
A collection of small Python scripts for OpenRGB that trigger based on Windows events.

## Features
- **Idle**: Turn off all lights when the screen turns off. Then resume light state when the screen turns back on.
- **Notification**: Flash lights when a notification is received.

## Requirements
- [Python](https://www.python.org/downloads/) >= 3.8
- An up to date [OpenRGB](https://openrgb.org/)
- An up to date [OpenRGB-Python](https://github.com/jath03/openrgb-python)

## Installation
1. Download the files.
    - Grab the latest release zip on the right, or clone this repo.
2. Place the directory somewhere you are happy for it to live.
    - The Windows events will point to these files, so if they move, it will break.
    - You can re-run the setup scripts to fix the paths should you want to relocate the files.
3. If you didn't already, install [OpenRGB-Python](https://github.com/jath03/openrgb-python)
    - Run `pip3 install openrgb-python` in the console.
4. Ensure the SDK Server in OpenRGB is running.
    - On the OpenRGB app, <kbd>SDK Server</kbd>, then <kbd>Start Server</kbd>.
    - By default these scripts use port `6742`.
    - You will need to start the server on start under `Settings > Start at Login > Start Server`.

## Usage
Run the setup script for the feature(s) you want.

### For lights off when idling
  - Run `scripts/create_idle_events.bat`.
  - You can also [create the Windows event manually](docs/idle) should you want to.

### For flash on Windows notification
- Run `scripts/create_notification_event.bat`.
- You can also [create the Windows event manually](docs/notification) should you want to.
