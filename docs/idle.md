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


## Troubleshooting