# Module to check if process exists
import psutil

# tkinter for dialog box to exit any open projects, just in case
import tkinter as tk
from tkinter import messagebox

# For sleep to slow down looping
import time

# Check if Audacity process exists based on launch path in autoconfig module
# Future update might see this just look for "Audacity.exe", without a specific path
def check_process_exists(process_path, lg):
    lg.info("Checking for Audacity.exe process from " + process_path)
    for proc in psutil.process_iter(['name', 'exe']):
        if proc.info['exe'] == process_path:
            return True
    return False

# Prompt to close Audacity if a project is open
def show_dialog_box(lg):
    root = tk.Tk()
    root.withdraw()
    lg.info("Audacity detected, showing messagebox to ask user to save and exit, then try script again.")
    result = messagebox.askokcancel("Audacity Detected", "A running instance of Audacity has been detected,\
    please save your work and exit before running this script again.")
    root.destroy()
    return(result)

    

# Check and loop to keep checking for Audacity after prompting
def main(lg):
    process_path = ["C:\\Program Files\\Audacity\\Audacity.exe"]
    for p in process_path:
        while True:
            if check_process_exists(p, lg):
                check=show_dialog_box(lg)
                if not check:
                    exit()
            else:
                break
            time.sleep(1)  # Adjust the sleep duration as needed

# For testing
if __name__ == "__main__":
    import logging_mod
    main(lg = logging_mod.setup_custom_logger("autorecorder"))