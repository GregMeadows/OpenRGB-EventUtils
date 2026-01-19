# Notification Event
Flash lights when a notification is received.

- [Manual Setup](#manual-setup)
- [Troubleshooting](#troubleshooting)

## Manual Setup

Follow these steps to manually create the notification event in Windows Task Scheduler.

### Create a Task

1. Press `Win + R`, type **taskschd.msc**, and press **Enter**.
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
  <Query Id="0" Path="Microsoft-Windows-PushNotifications-Platform/Operational">
    <Select Path="Microsoft-Windows-PushNotifications-Platform/Operational">
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


## Troubleshooting
