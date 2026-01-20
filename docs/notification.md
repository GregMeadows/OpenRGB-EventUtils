# Notification Event

Flash lights when a notification is received.

- [Manual Setup](#manual-setup)
- [Troubleshooting](#troubleshooting)

## Manual Setup

Follow these steps to manually create the notification event in Windows Task Scheduler.

### Create a Task

1. Press `Win + R`, type `taskschd.msc`, and press **Enter**.
2. In the left-hand pane, right-click **Task Scheduler Library** and select **New Folder**.
3. Name the folder **OpenRGB** (or whatever you want).
4. Navigate to the new **OpenRGB** folder.
5. Right-click in the center pane and select **Create New Task...** (not "Basic Task").

### General Tab

1. **Name:** `Notification` (This can be anything you want)

### Triggers Tab

1. Click **New...**.
2. **Begin the task:** Select **On an event**.
3. Under **Settings**, select **Custom** and click **New Event Filter...**.
4. Navigate to the **XML** tab and check **Edit query manually**.
5. Paste the following XML:

```xml
<QueryList>
  <Query Id="0" Path="Microsoft-Windows-PushNotification-Platform/Operational">
    <Select Path="Microsoft-Windows-PushNotification-Platform/Operational">
        *[System[Provider[@Name='Microsoft-Windows-PushNotifications-Platform'] and (EventID=3052)]]
    </Select>
  </Query>
</QueryList>

```

6. Click **OK** on both windows.

### Actions Tab

1. Click **New...**.
2. **Action:** Start a program.
3. **Program/script:** Browse and select the `notification.pyw` script (e.g., `"C:\Path\To\notification.pyw"`).
4. Click **OK**.

<br />
<br />

# Troubleshooting

Follow these steps in order to identify why the notification script might not be triggering.

## Test the Task Manually

The first thing to do is work out what went wrong.  
We can do this by checking if the task works.

1. Open **Task Scheduler** and navigate to the **OpenRGB** folder.
2. Right-click the **Notification** task and select **Run**.

If the lights flash, it means the script is working, and it is an [issue with the event hook.](#verify-the-event-in-event-viewer).  
If the lights do not flash, it means the [script is not running](#check-the-script).

> [!NOTE]  
> The notification script has a 5 minute cooldown by default, so it may flash the first time, but then do nothing on subsequent runs.

## Check the Script

If running the task does nothing, it means the script is either not running, or there is an error.

1. First, verify that the task action properly points to `notification.pyw` (this should be a full path).
2. Open a console in the script directory and run `python notification.pyw` to see the output. 

#### Common Issues
  - Ensure that you have installed `openrgb-python`.
  - Ensure that the Server SDK is running.

## Verify the Event in Event Viewer

If the task runs manually but won't trigger automatically, the `EventID` might be different on your system.

1. Press `Win + X` and select **Event Viewer**.
2. In the left sidebar, navigate to:
**Applications and Services Logs** > **Microsoft** > **Windows** > **PushNotifications-Platform** > **Operational**.
3. If there is nothing in the list, right-click the **Operational** log folder, and Select **Enable Log**.
4. The easiest way to test this is to wait for a notification, then refresh this list (`F5`).

Each notification will have several events attached to it, the description should shed some light on what they are.
Ideally you want to find the event that states `Toast with notification tracking id xxxx is being delivered `.

If the ID is different (e.g., `3051` or `3053`), go back to the [Triggers Tab step](#triggers-tab), and change the `EventID` in the XML to the new ID.
