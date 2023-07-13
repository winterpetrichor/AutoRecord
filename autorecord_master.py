# Orchestrating module

# General logging module
import logging_mod

# Import custom modules
import check_close
import autoconfig
import pipe_command

# Logging
lg = logging_mod.setup_custom_logger("autorecorder")

# Check if Audacity is closed
check_close.main(lg)

# Backup existing audacity.cfg
# Update variables in audacity.cfg with desired variables
# including selected devices and those to reduce recording file size
# Launch Audacity
autoconfig.main(lg)

# Issue commands to:
# - Create metronome track
# - Start recording
# - Stop recording
# - Save file
# - Exit Audacity
# - Restore backup of audacity.cfg
pipe_command.main(lg)

