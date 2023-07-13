# Regex module for matching and replacing variables in audacity.cfg
import re

# Function to open file, enumerate lines, check for matching text
# for config file variables, then replace the rest of that line
# with the desired variables from autoconfig module
def config_update(fileName, searchText, yourText):
    with open(fileName, 'r+') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            # Create a regular expression pattern to match searchText followed by any unknown text
            pattern = re.compile(re.escape(searchText) + r'(.*?)\n')
            match = re.search(pattern, line)
            if match:
                # Replace the unknown text (group 1) with yourText
                new_line = line.replace(match.group(1), yourText)
                lines[i] = new_line
                break
        file.seek(0)
        file.writelines(lines)

# For testing
if __name__ == "__main__":
    fileName = "C:\\Users\\flips\AppData\\Roaming\\audacity\\audacity.cfg"
    searchText = ["RecordingDevice=","PlaybackDevice="]
    yourText = "Line (THR5)"
    for i in searchText:
        config_update(fileName, i, yourText)
