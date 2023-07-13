# os and sys modules for restarting the script from within the script.
# This was required, instead of a loop, to work around audio devices
# not refreshing unless the script was restarted
import os
import sys

# tkinter for messagebox to notify that the target audio device is not present
import tkinter as tk
from tkinter import messagebox

# Backup existing audacity.cfg file to restore after
import shutil 

# Import custom module to read autorecord config file and bring in stored variables
from read_config import *

# Custom module for actually reading and writing the audacity.cfg file
import config_update

# Custom module to launch Audacity, meant for Windows installs
import launch

########################################################################################
# Configuration area - replace these variables with those you want/need
# Considering creating a separate configuration gui with an ini file or similar
# for future. This could even allow looping of sets - e.g. 
# Start at 80 BPM, rest(?), do 90 BPM, etc. until 120 BPM
# Probably get autorecord_master to read the ini file
# Variables would include:
# - Anything in searchReplace dict in this autoconfig module
# - Audacity config location (browse for audacity.cfg)
# - Audacity install location (browse for audacity.exe)
# - Starting BPM
# - Rest time between sets
# - Percentage or number increase in BPM each time
# - Ending BPM
# - Duration of each recording
# - Recording Save location (browse for folder)
# 
# Other notes:
# - Fix check_close to use the same exeName variable
# - Fix pipe_command to use the same samplerate and channels as autoconfig
#   - SetProject:Rate
#   - NewMonoTrack
#   - Export2:Filename={filename} NumChannels=1
# - In pipe command, make CursorLongJumpRight relative to duration 
# - (e.g.) for range (roundup(rec_dur/15)) do CursorLongJumpRight


# Your audio interface
recordingDevice = read_config("recordingDevice")
playbackDevice = read_config("playbackDevice")
desiredDevices = {"recording":recordingDevice,"playback":playbackDevice}

########################################################################################
# Note that the pipe_command module sets up tracks independently of desiredChannel
# and desiredSampleRate
# Those tracks are set in that module, default is Mono, 22050
# They are set by SetProject:Rate:22050 and NewMonoTrack
# Export2:Filename={filename} NumChannels=1 is responsible for exporting a Mono MP3
########################################################################################

# Set to Mono by default to help keep file size small
desiredChannel = read_config("desiredChannel")

# Lower than usual sample rate to help keep file size small
desiredSampleRate = read_config("desiredSampleRate")

# Lower than usual sample format to help keep file size small
desiredSampleFormatvar = read_config("desiredSampleFormat")
if desiredSampleFormatvar == 1:
    desiredSampleFormat = "Format16Bit"
elif desiredSampleFormatvar == 2:
    desiredSampleFormat = "Format32BitFloat"

# Location of Audacity, config file & exe - default here for typical Windows install
cfgLoc = "C:\\Users\\flips\AppData\\Roaming\\audacity\\"
exeLoc = "C:\\Program Files\\Audacity\\"
fileName = cfgLoc+"audacity.cfg"
exeName = exeLoc+"audacity.exe"

########################################################################################


# Schema for updating audacity.cfg file 
# with desired variables from configuration area above
searchReplace = {
    "RecordingDevice=":desiredDevices["recording"], 
    "PlaybackDevice=":desiredDevices["playback"],
    "RecordChannels=":desiredChannel,
    "DefaultProjectSampleRate=":desiredSampleRate,
    "DefaultProjectSampleFormatChoice=":desiredSampleFormat
    }

# Function to restart script when required    
def restart_script():
    python = sys.executable
    script = os.path.abspath(__file__)
    os.execl(python, python, script)

# Check if specified devices exist
def check(device, lg):
    # Module to enumerate devices, check for selected device and return True/False
    # Imported here to help with refreshing audio devices
    # This may not actually make a difference based on the latest code
    # and it could probably be placed at the top, will check in future
    import sd_pyaudio
    lg.info(f"Checking for device: {device}")
    deviceCheck = sd_pyaudio.deviceCheck(device)
    lg.info(f"Device \"{device}\" found?: {deviceCheck}")
    return(deviceCheck)

# If initial checks for devices fail, prompt then check again
def reCheck(device, lg):
    lg.info("Device not found, prompting to try again.")
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askokcancel(
        'Error', 
        f'Audio Device {device} not found!\nTry again?', 
        icon='warning', 
        type='okcancel')
    if result == True:
        lg.info('"Try again" selected, restarting script.')
        restart_script()
    else:
        lg.info("Exiting by user selection to not check for device again.")
        exit()

# Module to send the location of audacity.cfg to restore backup after recording
def send_cfg_loc():
    return(fileName)

# Loop check and re-check functions
def main(lg):
    for device in desiredDevices.values():
        deviceCheck = check(device, lg)
        while deviceCheck == False:
            deviceCheck = reCheck(device, lg)
            if deviceCheck == True:
                break

    # Backup existing audacity.cfg
    lg.info("Backing up audacity.cfg file")
    shutil.copyfile(fileName, "./audacity.cfg.bak")

    # Update audacity.cfg file with desired variables from configuration area above
    lg.info("Updating audacity.cfg file")
    for key, value in searchReplace.items():
        
        config_update.config_update(fileName, key, value)
    launch.main(exeName, lg)
    
    

# For testing
if __name__ == "__main__":
    import logging_mod
    main(lg = logging_mod.setup_custom_logger("autorecorder"))

