<# :
@echo off
:: Check for Admin rights
cd /d "%~dp0"
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: Run the PowerShell portion of this file
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-Expression (Get-Content '%~f0' -Raw)"
exit /b
#>

# Idle Start

# Variables
$TaskName = "Idle Start"
$TaskFolder = "\OpenRGB"
$Description = "Triggers idle.pyw when System enters Low Power Idle (Kernel-Power Event 566, Reason 12)."

# Get the directory this script is running in
$ScriptDir = Split-Path -Parent $PWD.Path
$ActionPath = Join-Path $ParentDir "idle.pyw"

# Check if the python file exists
if (-not (Test-Path $ActionPath)) {
    Write-Host "Error: Could not find 'idle.pyw' in $ScriptDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

# Define Trigger XML
$CustomTriggerXML = @"
<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">
      *[System[Provider[@Name='Microsoft-Windows-Kernel-Power'] and (EventID=566)]]
      and
      *[EventData[Data[@Name='Reason']='12']]
    </Select>
  </Query>
</QueryList>
"@

# Define the Task XML
$TaskXML = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>$Description</Description>
    <Author>$env:USERNAME</Author>
  </RegistrationInfo>
  <Triggers>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>$([System.Security.SecurityElement]::Escape($CustomTriggerXML))</Subscription>
    </EventTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <ExecutionTimeLimit>PT5M</ExecutionTimeLimit>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$ActionPath</Command>
      <Arguments>start</Arguments>
    </Exec>
  </Actions>
</Task>
"@

# Register Task
Write-Host "Creating Scheduled Task '$TaskName'..." -ForegroundColor Cyan

try {
    # -Force overwrites if it already exists
    Register-ScheduledTask -Xml $TaskXML -TaskName $TaskName -TaskPath $TaskFolder -Force | Out-Null
    Write-Host "Task created." -ForegroundColor Green
}
catch {
    Write-Host "Failed to create task." -ForegroundColor Red
    Write-Error $_
}


# Idle Stop

# Variables
$TaskName = "Idle Stop"
$Description = "Triggers idle.pyw when System exits Low Power Idle (Kernel-Power Event 566, Reason 31 or 32)."

# Define Trigger XML
$CustomTriggerXML = @"
<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">
      *[System[Provider[@Name='Microsoft-Windows-Kernel-Power'] and (EventID=566)]]
      and
      *[EventData[Data[@Name='Reason']='31' or Data[@Name='Reason']='32']]
    </Select>
  </Query>
</QueryList>
"@

# Define Task XML
$TaskXML = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>$Description</Description>
    <Author>$env:USERNAME</Author>
  </RegistrationInfo>
  <Triggers>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>$([System.Security.SecurityElement]::Escape($CustomTriggerXML))</Subscription>
    </EventTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <ExecutionTimeLimit>PT5M</ExecutionTimeLimit>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$ActionPath</Command>
      <Arguments>stop</Arguments>
    </Exec>
  </Actions>
</Task>
"@

# Register Task
Write-Host "Creating Scheduled Task '$TaskName'..." -ForegroundColor Cyan

try {
    Register-ScheduledTask -Xml $TaskXML -TaskName $TaskName -TaskPath $TaskFolder -Force | Out-Null
    Write-Host "Task created." -ForegroundColor Green
}
catch {
    Write-Host "Failed to create task." -ForegroundColor Red
    Write-Error $_
}

Write-Host "Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")