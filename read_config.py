import configparser

def read_config(var):

    var_lower = var.lower()
    config = configparser.ConfigParser()
    config.read('config.ini')
    var = config['DEFAULT'][var_lower]
    return(var)

#print(read_config("recordingDevice"))



"""
if the config file does not exist then prompt the user to use 
either default values or run the config app
if any individual var does not exist in config,
silently replace with default value
consider dictionary for default values
"""