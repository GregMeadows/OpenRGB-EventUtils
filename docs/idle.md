# Idle Event

Turn off all lights when the screen turns off. Then resume light state when the screen turns back on.

- [Manual Setup: Start Event](#manual-setup-start-event)
- [Manual Setup: Stop Event](#manual-setup-start-event)
- [Troubleshooting](#troubleshooting)

## Manual Setup: Start Event

Follow these steps to manually create the idle start event in Windows Task Scheduler.

### Create a Task

1. Press `Win + R`, type **taskschd.msc**, and press **Enter**.
2. In the left-hand pane, right-click **Task Scheduler Library** and select **New Folder**.
3. Name the folder **OpenRGB** (or whatever you want).
4. Navigate to the new **OpenRGB** folder.
5. Right-click in the center pane and select **Create New Task...** (not "Basic Task").

### General Tab

1. **Name:** `Idle Start` (This can be anything you want to signify the start event)

### Triggers Tab

1. Click **New...**.
2. **Begin the task:** Select **On an event**.
3. Under **Settings**, select **Custom** and click **New Event Filter...**.
4. Navigate to the **XML** tab and check **Edit query manually**.
5. Paste the following XML:

```xml
<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">
      *[System[Provider[@Name='Microsoft-Windows-Kernel-Power'] and (EventID=566)]]
      and
      *[EventData[Data[@Name='Reason']='12']]
    </Select>
  </Query>
</QueryList>

```

6. Click **OK** on both windows.

### Actions Tab

1. Click **New...**.
2. **Action:** Start a program.
3. **Program/script:** Browse and select the `idle.pyw` script (e.g., `"C:\Path\To\idle.pyw"`).
4. **Add arguments:** `start`
5. Click **OK**.


## Manual Setup: Stop Event

Follow these steps to manually create the idle stop in Windows Task Scheduler.  

> [!NOTE]  
> This is identical to the previous task setup, with only the XML and start argument changing.

### Create a Task

1. Press `Win + R`, type **taskschd.msc**, and press **Enter**.
2. In the left-hand pane, right-click **Task Scheduler Library** and select **New Folder**.
3. Name the folder **OpenRGB** (or whatever you want).
4. Navigate to the new **OpenRGB** folder.
5. Right-click in the center pane and select **Create New Task...** (not "Basic Task").

### General Tab

1. **Name:** `Idle Stop` (This can be anything you want to signify the stop event)

### Triggers Tab

1. Click **New...**.
2. **Begin the task:** Select **On an event**.
3. Under **Settings**, select **Custom** and click **New Event Filter...**.
4. Navigate to the **XML** tab and check **Edit query manually**.
5. Paste the following XML:

```xml
<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">
      *[System[Provider[@Name='Microsoft-Windows-Kernel-Power'] and (EventID=566)]]
      and
      *[EventData[Data[@Name='Reason']='31' or Data[@Name='Reason']='32']]
    </Select>
  </Query>
</QueryList>

```

6. Click **OK** on both windows.

### Actions Tab

1. Click **New...**.
2. **Action:** Start a program.
3. **Program/script:** Browse and select the `idle.pyw` script (e.g., `"C:\Path\To\idle.pyw"`).
4. **Add arguments:** `stop`
5. Click **OK**.

<br />

# Troubleshooting

Follow these steps to diagnose why the idle script might not be triggering.  
Some steps only refer to the start script as they are identical to troubleshooting the stop script.

## Test the Task Manually

The first thing to do is work out what went wrong.  
We can do this by checking if the task works.

1. Open **Task Scheduler** and navigate to the **OpenRGB** folder.
2. Right-click the **Idle Start** task and select **Run**.

If the lights go out, it means the script is working, and it is an [issue with the event hook](#verify-the-event-in-event-viewer).  
If the lights stay on, it means the [script is not running](#check-the-script).  

 If this works you can try the **Idle Stop** task to see if the lights turn back on.

## Check the Script

If running the task does nothing, it means the script is either not running, or there is an error.

1. First, verify that the task action properly points to `idle.pyw` (this should be a full path).
2. Check that the start argument is correct, `start` or `stop` depending on the event.
3. Open a console in the script directory and run `python idle.pyw start` to see the output. 
4. If this works, run `python idle.pyw stop` to stop idle mode. 

#### Common Issues
  - Ensure that you have installed `openrgb-python`.
  - Ensure that the Server SDK is running.

## Verify the Event in Event Viewer

If the task runs manually but won't trigger automatically, the `EventID` might be different on your system.

1. Press `Win + X` and select **Event Viewer**.
2. In the left sidebar, navigate to:
**Windows Logs** > **Microsoft** > **System**.
3. Wait for your screen to turn off (set a low timeout), wake it back up, then refresh this list (`F5`).

There should be at least 2 events with `Kernel-Power` as the source. Though they will not have any real helpful information.

- If the ID is different (not `566`), go back to the [Triggers Tab step](#triggers-tab) for both **start**, and **stop**, and change the `EventID` in the XML to the new ID.
- If this is matching, the, go in into **Details** on both events and check the `Reason`.
  - This should be `12` for screen off, and `31` or `32` for screen on.
  - If they are different, change the `Data[@Name='Reason']='XX'` in the XML and try again.
- On the off chance that this is drastically different to what you see, you can use any identifier on the details tab, not just `Reason`. Just change `Data[@Name='XX']='XX'` to a value that is unique to the screen off and screen on event.
