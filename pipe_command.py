# For pipe
import os
import sys

# For various sleeps
import time

# For parallel execution of functions regarding recording
import threading

# Used to set Audacity as the top window
import win32gui

# Used to stop recording and select "No" on Audacity save dialog
import keyboard

# Modules to restore audacity.cfg backup
import shutil

# For filename
from datetime import datetime

# Custom module to allow user to input BPM for metronome
import get_bpm

# Get cfg file location
import autoconfig

# Import custom module to read autorecord config file and bring in stored variables
from read_config import *

# Modified mod-script-pipe template
# Create Class to allow passing the pipe from function to function
class Runinfo:
    def __init__(self, TOFILE, FROMFILE, err1, EOL):
        self.TOFILE = TOFILE
        self.FROMFILE = FROMFILE
        self.err1 = err1
        self.EOL = EOL

# Read variables from config.ini
desiredSampleRate = read_config("desiredSampleRate")
desiredChannel = read_config("desiredChannel")

# Perform default checks from pipe_test.py and pass variables back to class
# (https://github.com/audacity/audacity/blob/master/scripts/piped-work/pipe_test.py)
def checks(err1, lg, R1):
    time.sleep(3)

    lg.info("Write to  \"" + R1.TONAME +"\"")
    if not os.path.exists(R1.TONAME):
        lg.info(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
        err1 = True
        return(err1)
        sys.exit()

    lg.info("Read from \"" + R1.FROMNAME +"\"")
    if not os.path.exists(R1.FROMNAME):
        lg.info(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
        err1 = True
        return(err1)
        sys.exit()
        
    lg.info("-- Both pipes exist.  Good.")

    TOFILE = open(R1.TONAME, 'w')
    R1.TOFILE = TOFILE
    lg.info("-- File to write to has been opened")
    FROMFILE = open(R1.FROMNAME, 'rt')
    R1.FROMFILE = FROMFILE
    lg.info("-- File to read from has now been opened too\r\n")
    err1 = False
    R1.err1 = err1
    print("end-checks" + str(err1))

    return(err1, R1)


# Slightly modified send, get, do and "quick_test" functions, tied back to class
def send_command(command, lg, R1):
    """Send a single command."""
    lg.info("Send: >>> \n"+command)
    R1.TOFILE.write(command + R1.EOL)
    R1.TOFILE.flush()

def get_response(R1):
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = R1.FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command, lg, R1):
    """Send one command, and return the response."""
    send_command(command, lg, R1)
    response = get_response(R1)
    lg.info("Rcvd: <<< \n" + response)
    return response

def exec_command(command,lg,R1):
    do_command(command,lg,R1)

# Function to perform checks and send pipe commands
def main(lg):
    # Initiate pipe Class
    R1 = Runinfo('','', True,'')

    # Check if windows or linux, based on some template, can't remember which
    # The rest of the scripted modules are meant for Windows
    # Perhaps in the future, they can be updated for Linux
    if sys.platform == 'win32':
        lg.info("Running on windows")
        R1.TONAME = '\\\\.\\pipe\\ToSrvPipe'
        R1.FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
        R1.EOL = '\r\n\0'
    else:
        lg.info("Running on linux or mac")
        TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        EOL = '\n'

    # Perform checks
    lg.info("pre-checks success = " + str(R1.err1))
    R1.err1 = checks(R1.err1,lg,R1)

    while R1.err1 == True:
        lg.info("while-pre-checks: " + str(R1.err1))
        checks(R1.err1,lg,R1)
        lg.info("while-post-checks: " + str(R1.err1))
        if R1.err1 == False:
            break

    # Set Audacity window at the forefront
    window_title = "Audacity"
    hwnd = win32gui.FindWindow(None, window_title)
    win32gui.SetForegroundWindow(hwnd)
    
    # Run function to execute pipe commands at the end of this function
    main2(lg,R1)

# Function to execute pipe commands
def main2(lg,R1):

    # Prompt user for BPM
    tempo = str(get_bpm.get_bpm())
    # 35 seconds duration, to allow some slack time at the start of the recording
    # and allow for 30 seconds of recording
    dur = "35"
    # 200 bars seems reasonable for playable tempos to cut back down to 1 minute
    # Adjust if necessary
    bars = str(int(dur)*2)
    # Variable used for testing to cut the recording step short
    cut_short = 0
    # Calc recording duration
    rec_dur = str(int(dur)-cut_short)

    # SetProject:Rate and NewMonoTrack are not related to the variables 
    # in the autoconfig module
    # See https://alphamanual.audacityteam.org/man/Scripting_Reference 
    # to choose alternates
    # Set low bitrate and mono for small file size
    if desiredSampleRate == 22050:
        exec_command("SetProject:Rate:22050",lg,R1)
    elif desiredSampleRate == 44100:
        exec_command("SetProject:Rate:44100",lg,R1)
    # exec_command("SetProject:Rate:22050",lg,R1)
    if desiredChannel == 1:
        exec_command("NewMonoTrack",lg,R1)
    elif desiredChannel == 2:
        exec_command("NewStereoTrack",lg,R1)
    # exec_command("NewMonoTrack",lg,R1)
    # Zoom out for effective CursorLongJumpRight commands
    exec_command("ZoomOut",lg,R1)
    exec_command("ZoomOut",lg,R1)
    exec_command("SelectAll",lg,R1)
    exec_command("CursorLongJumpRight",lg,R1)
    exec_command("CursorLongJumpRight",lg,R1)
    exec_command("CursorLongJumpRight",lg,R1)
    exec_command("CursorLongJumpRight",lg,R1)
    # Jump to start
    exec_command("SelStart",lg,R1)
    
    # Create metronome
    exec_command(f"RhythmTrack:tempo={tempo} bars={bars}",lg,R1)
    exec_command(f"SelectTime:Start=0 End={dur}",lg,R1)
    exec_command("Trim",lg,R1)

    # Set Audacity window at the forefront again
    window_title = "Audacity"
    hwnd = win32gui.FindWindow(None, window_title)
    win32gui.SetForegroundWindow(hwnd)

    # start_recording, stop_recording and dont_save functions defined for threading
    # These have to happen in parallel
    # start_recording and stop_recording actually start in parallel
    # stop_recording is just delayed by the recording duration
    # at the end of stop_recording, dont_save is started in parallel
    # This is done since the Exit pipe command stops execution
    # and we need to choose "No" on the save confirmation dialog that 
    # Audacity prompts with when we issue the Exit pipe command
    def start_recording():
        # Start recording on a new track
        exec_command("Record2ndChoice",lg,R1)
    
    # Function to stop recording
    def stop_recording():
        # Wait for duration of recording
        time.sleep(int(rec_dur))
        # Escape key stops recording
        keyboard.press_and_release('esc')
        # Select recorded track
        exec_command("SelectTracks:Track=1 Mode=Set",lg,R1)
        # Apply compressor to recorded track
        exec_command("Compressor",lg,R1)
        exec_command("Compressor:UsePeak=True",lg,R1)
        # Select metronome track
        exec_command("SelectTracks:Track=0 Mode=Add",lg,R1)
        # Prepare filename - XX-BPM_YYYY-MM-DD_HH-MM-SS.mp3
        now = datetime.now()
        formatted_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = "C:\\Users\\flips\Documents\\Guitar_Practice\\Autorecord_exercises\\"\
            + tempo + "-BPM_" + formatted_string + ".mp3"
        lg.info("Saving recording...")
        # Export to Mono MP3 - this is also independent of the autoconfig file
        # See https://alphamanual.audacityteam.org/man/Scripting_Reference 
        exec_command(f"Export2:Filename={filename} NumChannels=1",lg,R1)
        # Wait to allow export
        time.sleep(2)
        lg.info(f"Recording saved to {filename}")
        # Initiate thread to select "No" on Audacity save dialog 
        # after Exit command is issued
        lg.info("Exiting Audacity without saving as Audacity Project")
        save_thread.start()
        lg.info("Restoring audacity.cfg backup...")
        restore_thread.start()
        lg.info("Exiting...")
        exec_command("Exit",lg,R1)

    # Function to not save recording as an Audacity project file        
    def dont_save():
        # Wait for dialog
        time.sleep(1)
        # Select "No"
        keyboard.press_and_release('n')

    # Function to restore audacity.cfg backup        
    def restore_backup():
        time.sleep(2)
        # Get audacity.cfg location from autoconfig
        cfg_loc = autoconfig.send_cfg_loc()
        # Restore backup file
        time.sleep(2)
        shutil.copyfile("./audacity.cfg.bak", cfg_loc)

    # Initiate save_thread and restore_thread, but don't start them, 
    # the stop_recording function will start them
    save_thread = threading.Thread(target=dont_save)
    restore_thread = threading.Thread(target=restore_backup)

    # Initiate and start start_recording thread
    recording_thread = threading.Thread(target=start_recording)
    lg.info("Recording...")
    recording_thread.start()

    # Initiate and start stop_recording thread
    stop_thread = threading.Thread(target=stop_recording)
    lg.info("Stopping")
    stop_thread.start()

# For testing
while __name__ == "__main__":
    import logging_mod
    main(lg = logging_mod.setup_custom_logger("autorecorder"))