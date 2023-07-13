# Module used to enumerate audio devices
import pyaudio

# Function to check for devices
def deviceCheck(device_name):
    # Instance of pyaudio module
    p = pyaudio.PyAudio()
    
    # Initial setup to false by default
    device_exists = False

    # Iteratively check for device
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info["name"] == device_name:
            device_exists = True
            break

    # Return True / False if devices exists / does not exist
    if device_exists:
        return(True)
    else:
        return(False)