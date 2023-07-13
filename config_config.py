import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pyaudio
import configparser
import os


# Read ini file and set default values in window

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Input Form")
        self.master.geometry("460x400")
        self.config = configparser.ConfigParser()
        self.p = pyaudio.PyAudio()

        # List of config variables
        self.cfg_list = [
            "recordingDevice", 
            "playbackDevice",
            "desiredChannel",
            "desiredSampleRate",
            "desiredSampleFormat",
            "fileName",
            "exeName",
            "bpmStart",
            "restTimeSec",
            "bpmIncrType",
            "bpmIncr",
            "bpmEnd",
            "dur",
            "saveLoc"
            ]
        
        self.cfg_dict = {}

        # Read existing config
        self.config.read('config.ini')
        for var in self.cfg_list:
            try:
                self.cfg_dict[var] = (self.config['DEFAULT'][var])
            except:
                print("Variable " + var + "does  not exist in the config file.")
                print("Creating blank variable: " + var)
                self.cfg_dict[var] = ""
        print(self.cfg_dict)
        
        self.create()
            
        #########
        #Try if no config line exists, write blank config line
        """
        cfglist = [
        "recordingDevice = self.config['DEFAULT']['recordingdevice']", 
        "playbackDevice = self.config['DEFAULT']['playbackdevice']", 
        "desiredChannel = self.config['DEFAULT']['desiredchannel']", 
        "desiredSampleRate = self.config['DEFAULT']['desiredsamplerate']", 
        "desiredSampleFormat = self.config['DEFAULT']['desiredsampleformat']", 
        "fileName = self.config['DEFAULT']['filename']", 
        "exeName = self.config['DEFAULT']['exename']", 
        "bpmStart = self.config['DEFAULT']['bpmstart']", 
        "restTimeSec = self.config['DEFAULT']['resttimesec']", 
        "bpmIncrType = self.config['DEFAULT']['bpmincrtype']", 
        "bpmIncr = self.config['DEFAULT']['bpmincr']", 
        "bpmEnd = self.config['DEFAULT']['bpmend']", 
        "dur = self.config['DEFAULT']['dur']", 
        "saveLoc = self.config['DEFAULT']['saveloc']"
        ]

        def cfg_test_func(var):
            try:
                print(var)
                print(eval(var))
                return(eval(var))
            
            except:
                pass
        
        for var in cfglist:
            cfg_test_func(var)
        """
        """
        try:
            recordingDevice = self.config['DEFAULT']['recordingdevice']
            playbackDevice = self.config['DEFAULT']['playbackdevice']
            desiredChannel = self.config['DEFAULT']['desiredchannel']
            desiredSampleRate = self.config['DEFAULT']['desiredsamplerate']
            desiredSampleFormat = self.config['DEFAULT']['desiredsampleformat']
            fileName = self.config['DEFAULT']['filename']
            exeName = self.config['DEFAULT']['exename']
            bpmStart = self.config['DEFAULT']['bpmstart']
            restTimeSec = self.config['DEFAULT']['resttimesec']
            bpmIncrType = self.config['DEFAULT']['bpmincrtype']
            bpmIncr = self.config['DEFAULT']['bpmincr']
            bpmEnd = self.config['DEFAULT']['bpmend']
            dur = self.config['DEFAULT']['dur']
            saveLoc = self.config['DEFAULT']['saveloc']
        except:
            pass
        """
        
        """
        for key, value in cfglist.items():
            try:
                globals()[eval(key)] = eval(value)
                print(eval(key))
            except:
                print(eval(key))
                pass
        """
        
        # Create config window
        

        # Recording Device
        tk.Label(self.master, text="1) Recording Device:").grid(row=0, column=0, sticky="E")
        self.recordingDeviceVar = tk.StringVar(self.master)
        self.recordingDeviceVar.set(self.get_input_devices()[0])
        self.recordingDeviceMenu = tk.OptionMenu(self.master, self.recordingDeviceVar, *self.get_input_devices())
        print(self.input_devices)
        self.recordingDeviceMenu.grid(row=0, column=1, columnspan=3, sticky="EW")
        self.recordingDeviceOverrideVar = tk.IntVar()
        tk.Checkbutton(self.master, text="Override", variable=self.recordingDeviceOverrideVar,
                       command=self.toggle_recording_device_override).grid(row=0, column=4)
        self.recordingDeviceEntry = tk.Entry(self.master)
        self.recordingDeviceEntry.grid(row=0, column=1, columnspan=3, sticky="EW")
        self.recordingDeviceEntry.grid_remove()
        if self.cfg_dict["recordingDevice"] not in self.input_devices:
            response = messagebox.askyesno("Recording Device", "The saved device in the config file is either blank or not detected by the system. Would you like to override and continue using the saved device? Selecting 'No' will show the list of available devices for you to select.")
            if response:
                self.recordingDeviceOverrideVar.set(1)
                self.toggle_recording_device_override()
                self.recordingDeviceEntry.delete(0, 'end')
                self.recordingDeviceEntry.insert(0, self.cfg_dict["recordingDevice"])
            else:
                pass
        else:
            self.recordingDeviceVar.set(self.cfg_dict["recordingDevice"])

        # Playback Device
        tk.Label(self.master, text="2) Playback Device:").grid(row=1, column=0, sticky="E")
        self.playbackDeviceVar = tk.StringVar(self.master)
        self.playbackDeviceVar.set(self.get_output_devices()[0])
        self.playbackDeviceMenu = tk.OptionMenu(self.master, self.playbackDeviceVar, *self.get_output_devices())
        self.playbackDeviceMenu.grid(row=1, column=1, columnspan=3, sticky="EW")
        self.playbackDeviceOverrideVar = tk.IntVar()
        tk.Checkbutton(self.master, text="Override", variable=self.playbackDeviceOverrideVar,
                       command=self.toggle_playback_device_override).grid(row=1, column=4)
        self.playbackDeviceEntry = tk.Entry(self.master)
        self.playbackDeviceEntry.grid(row=1, column=1, columnspan=3, sticky="EW")
        self.playbackDeviceEntry.grid_remove()
        if self.cfg_dict["playbackDevice"] not in self.output_devices:
            response = messagebox.askyesno("Playback Device", "The saved device in the config file is either blank or not detected by the system. Would you like to override and continue using the saved device? Selecting 'No' will show the list of available devices for you to select.")
            if response:
                self.playbackDeviceOverrideVar.set(1)
                self.toggle_playback_device_override()
                self.playbackDeviceEntry.delete(0, 'end')
                self.playbackDeviceEntry.insert(0, self.cfg_dict["playbackDevice"])
            else:
                pass
        else:
            self.playbackDeviceVar.set(self.cfg_dict["playbackDevice"])

        # Recording Channels
        tk.Label(self.master, text="3) Recording Channels:").grid(row=2, column=0, sticky="E")
        self.desiredChannelVar = tk.IntVar(value=(self.cfg_dict["desiredChannel"]))
        tk.Radiobutton(self.master, text="Mono", variable=self.desiredChannelVar,
                       value=1).grid(row=2,column=1,columnspan=2, sticky="W")
        tk.Radiobutton(self.master, text="Stereo", variable=self.desiredChannelVar,
                       value=2).grid(row=2,column=3, sticky="W")
        
        # Sample Rate
        tk.Label(self.master, text="4) Sample Rate:").grid(row=3,column=0, sticky="E")
        self.desiredSampleRateVar = tk.IntVar(value=(self.cfg_dict["desiredSampleRate"]))
        tk.Radiobutton(self.master,text="22050Hz",variable=self.desiredSampleRateVar,value=22050).grid(row=3,column=1,columnspan=2,sticky="W")
        tk.Radiobutton(self.master,text="44100Hz",variable=self.desiredSampleRateVar,value=44100).grid(row=3,column=3,sticky="W")

        # Sample Format
        tk.Label(self.master, text="5) Sample Format:").grid(row=4,column=0, sticky="E")
        self.desiredSampleFormatVar = tk.IntVar(value=(self.cfg_dict["desiredSampleFormat"]))
        tk.Radiobutton(self.master,text="Format16Bit",variable=self.desiredSampleFormatVar,value=1).grid(row=4,column=1,columnspan=2,sticky="W")
        tk.Radiobutton(self.master,text="Format32BitFloat",variable=self.desiredSampleFormatVar,value=2).grid(row=4,column=3,sticky="W")

        # Audacity CFG Location
        tk.Label(self.master, text="6) Audacity CFG Location:").grid(row=5,column=0, sticky="E")
        self.fileNameVar = tk.StringVar(value=self.cfg_dict["fileName"])
        self.fileNameEntry = tk.Entry(self.master,textvariable=self.fileNameVar)
        self.fileNameEntry.grid(row=5,column=1,columnspan=3,sticky="EW")
        tk.Button(self.master,text="Browse",command=self.browse_cfg).grid(row=5,column=4)

        # Audacity EXE Location
        tk.Label(self.master, text="7) Audacity EXE Location:").grid(row=6,column=0, sticky="E")
        self.exeNameVar = tk.StringVar(value=self.cfg_dict["exeName"])
        self.exeNameEntry = tk.Entry(self.master,textvariable=self.exeNameVar)
        self.exeNameEntry.grid(row=6,column=1,columnspan=3,sticky="EW")
        tk.Button(self.master,text="Browse",command=self.browse_exe).grid(row=6,column=4)

        # Starting BPM
        tk.Label(self.master, text="8) Starting BPM:").grid(row=7,column=0,sticky="E")
        self.bpmStartVar = tk.IntVar(value=(self.cfg_dict["bpmStart"]))
        self.bpmStartEntry = tk.Spinbox(self.master,from_=30,to_=300,textvariable=self.bpmStartVar,width=4,validate="key", validatecommand=(self.master.register(self.validate_integer_input), '%P'))
        self.bpmStartEntry.grid(row=7,column=1,columnspan=2,sticky="W")

        # Rest Time
        tk.Label(self.master, text="9) Rest Time (seconds):").grid(row=8,column=0,sticky="E")
        self.restTimeSecVar = tk.IntVar(value=self.cfg_dict["restTimeSec"])
        self.restTimeSecSpinbox = tk.Spinbox(self.master,from_=0,to_=300,width=4,textvariable=self.restTimeSecVar,validate="key", validatecommand=(self.master.register(self.validate_integer_input), '%P'))
        self.restTimeSecSpinbox.grid(row=8,column=1,sticky="W")

        # BPM Increment
        tk.Label(self.master, text="10) BPM Increment:").grid(row=9,column=0, sticky="E")
        self.bpmIncrTypeVar = tk.StringVar(value=self.cfg_dict["bpmIncrType"])
        tk.Radiobutton(self.master,text="BPM",variable=self.bpmIncrTypeVar,value="BPM").grid(row=9,column=1)
        tk.Radiobutton(self.master,text="%",variable=self.bpmIncrTypeVar,value="pct",command=self.conv_pct_to_bpm).grid(row=9,column=2)
        self.bpmIncrVar = tk.IntVar(value=self.cfg_dict["bpmIncr"])
        self.bpmIncrEntry = tk.Spinbox(self.master,from_=0,to_=100,textvariable=self.bpmIncrVar,width=4,validate="key", validatecommand=(self.master.register(self.validate_integer_input), '%P'))
        self.bpmIncrEntry.grid(row=9,column=3,sticky="W")

        # Ending BPM
        tk.Label(self.master, text="11) Ending BPM:").grid(row=10,column=0, sticky="E")
        self.bpmEndVar = tk.IntVar(value=self.cfg_dict["bpmEnd"])
        self.bpmEndEntry = tk.Spinbox(self.master,from_=30,to_=300,textvariable=self.bpmEndVar,width=4,validate="key", validatecommand=(self.master.register(self.validate_integer_input), '%P'))
        self.bpmEndEntry.grid(row=10,column=1,columnspan=2,sticky="W")

        # Duration in seconds
        tk.Label(self.master, text="12) Duration in seconds:").grid(row=11,column=0, sticky="E")
        self.durVar = tk.IntVar(value=self.cfg_dict["dur"])
        self.durEntry = tk.Spinbox(self.master,from_=30,to_=300,textvariable=self.durVar,width=4,validate="key", validatecommand=(self.master.register(self.validate_integer_input), '%P'))
        self.durEntry.grid(row=11,column=1,columnspan=2,sticky="W")

        # Save Location
        tk.Label(self.master, text="13) Save Location:").grid(row=12,column=0, sticky="E")
        self.saveLocVar = tk.StringVar(value=self.cfg_dict["saveLoc"])
        self.saveLocEntry = tk.Entry(self.master,textvariable=self.saveLocVar)
        self.saveLocEntry.grid(row=12,column=1,columnspan=3,sticky="EW")
        tk.Button(self.master,text="Browse",command=self.browse_save_loc).grid(row=12,column=4)

        # Separator
        tk.Label(root, text=" ").grid(row=13, column=0)
        ttk.Separator(root, orient='horizontal').grid(row=13, column=1, columnspan=3, sticky='ew')
        tk.Label(root, text=" ").grid(row=15, column=0)

        # Save Button
        tk.Button(self.master,text="--- Save ---",command=self.save).grid(row=16,column=0,columnspan=5)

        # Title
        

    def validate_integer_input(self, new_value):
        if not new_value.isdigit():
            messagebox.showerror("Error", "Please enter an integer value")
            return False
        return True
    
    def toggle_recording_device_override(self):
        if self.recordingDeviceOverrideVar.get() == 1:
            self.recordingDeviceMenu.grid_remove()
            self.recordingDeviceEntry.grid()
        else:
            self.recordingDeviceMenu.grid()
            self.recordingDeviceEntry.grid_remove()

    def toggle_playback_device_override(self):
        if self.playbackDeviceOverrideVar.get() == 1:
            self.playbackDeviceMenu.grid_remove()
            self.playbackDeviceEntry.grid()
        else:
            self.playbackDeviceMenu.grid()
            self.playbackDeviceEntry.grid_remove()

    def get_input_devices(self):
        self.input_devices = []
        for i in range(self.p.get_device_count()):
            device = self.p.get_device_info_by_index(i)
            if device["maxInputChannels"] > 0:
                self.input_devices.append(device["name"])
        return self.input_devices

    def get_output_devices(self):
        self.output_devices = []
        for i in range(self.p.get_device_count()):
            device = self.p.get_device_info_by_index(i)
            if device["maxOutputChannels"] > 0:
                self.output_devices.append(device["name"])
        return self.output_devices
    
    def conv_pct_to_bpm(self):
        pass

    def browse_cfg(self):
        initial_dir = os.path.join(os.environ['APPDATA'], 'Audacity')
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("CFG File", "*.cfg")])
        if file_path:
            self.fileNameVar.set(file_path)

    def browse_exe(self):
        if os.environ['PROCESSOR_ARCHITECTURE'] == 'AMD64':
            initial_dir = os.path.join(os.environ['ProgramW6432'], 'Audacity')
        else:
            initial_dir = os.path.join(os.environ['ProgramFiles'], 'Audacity')
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("EXE File", "*.exe")])
        if file_path:
            self.exeNameVar.set(file_path)

    def browse_save_loc(self):
        initial_dir = os.path.expanduser('~/Documents')
        dir_path = filedialog.askdirectory(initialdir=initial_dir)
        if dir_path:
            self.saveLocVar.set(dir_path)

    def create(self):
        # Create inputs
        for key,value in self.cfg_dict.items():
            self.config.set("DEFAULT",key,value)
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def save(self):
        # Validate inputs
        error_messages = []
        if self.recordingDeviceOverrideVar.get() == 0 and self.recordingDeviceVar.get() not in self.get_input_devices():
            error_messages.append("Invalid recording device.")
        if self.playbackDeviceOverrideVar.get() == 0 and self.playbackDeviceVar.get() not in self.get_output_devices():
            error_messages.append("Invalid playback device.")
        try:
            self.desiredChannelVar.get()
        except:
            error_messages.append("Invalid Selection for Recording Channels.")
        try:
            self.desiredSampleRateVar.get()
        except:
            error_messages.append("Invalid Selection for Sample Rate.")
        try:
            self.desiredSampleFormatVar.get()
        except:
            error_messages.append("Invalid Selection for Sample Format.")
        if not os.path.isfile(self.fileNameVar.get()):
            error_messages.append("Invalid Audacity CFG location.")
        if not os.path.isfile(self.exeNameVar.get()):
            error_messages.append("Invalid Audacity EXE location.")
        if not (30 <= self.bpmStartVar.get() <= 300):
            error_messages.append("Starting BPM must be between 30 and 300.")
        if self.bpmEndVar.get() <= self.bpmStartVar.get():
            error_messages.append("Ending BPM must be higher than Starting BPM.")
        if not os.path.isdir(self.saveLocVar.get()):
            error_messages.append("Invalid save location.")

        # Show error messages
        if error_messages:
            tk.messagebox.showerror("Error", "\n".join(error_messages))
            return

        # Save inputs
        self.config["DEFAULT"] = {
            "recordingDevice": self.recordingDeviceEntry.get() if self.recordingDeviceOverrideVar.get() == 1 else self.recordingDeviceVar.get(),
            "playbackDevice": self.playbackDeviceEntry.get() if self.playbackDeviceOverrideVar.get() == 1 else self.playbackDeviceVar.get(),
            "desiredChannel": self.desiredChannelVar.get(),
            "desiredSampleRate": self.desiredSampleRateVar.get(),
            "desiredSampleFormat": self.desiredSampleFormatVar.get(),
            "fileName": self.fileNameVar.get(),
            "exeName": self.exeNameVar.get(),
            "bpmStart": self.bpmStartVar.get(),
            "restTimeSec": self.restTimeSecVar.get(),
            "bpmIncrType": self.bpmIncrTypeVar.get(),
            "bpmIncr": self.bpmIncrVar.get(),
            "bpmEnd": self.bpmEndVar.get(),
            "dur": self.durVar.get(),
            "saveLoc": self.saveLocVar.get()
        }
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
        tk.messagebox.showinfo("Success", "Inputs saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.master.title("Autorecord Config")
    root.mainloop()