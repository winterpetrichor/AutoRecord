# Modules to detect Audacity program
"""from pywinauto import Application"""
import subprocess
from os import path as osp

"""
# List of locations where Audacity might be installed
# 64 bit listed first, meant for Windows
# Any other locations can be appended to this list
inst_locs = ["C:\\Program Files\\Audacity\\audacity.exe"
             ,"C:\\Program Files (x86)\\Audacity\\audacity.exe"]
"""

# Function to launch Audacity
def main(exeName, lg):
    lg.info("Launching Audacity from " + exeName)
    process = subprocess.Popen([exeName])

    # There was going to be some more functionality here
    # but it was not necessary, and pywinauto was causing
    # compilation errors. May return to this later.
    """
    # Check each location and launch the first one found
    for loc in inst_locs:
        if(osp.isfile(loc)) is True:
            lg.info("Launching Audacity from " + loc)
            app = subprocess.Popen([loc])

            # Connect to the application using the executable path
            app = Application().connect(path=loc)

            # Get the main window of the application
            window = app.window()

            # Do something with the window
            win_title = window.window_text()
    """
# For testing
if __name__ == "__main__":
    import logging_mod
    main(lg = logging_mod.setup_custom_logger("autorecorder"))






