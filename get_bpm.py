# tkinter to display dialog to select BPM for metronome
import tkinter as tk
from tkinter import simpledialog

def get_bpm():
    ROOT = tk.Tk()
    ROOT.withdraw()
    USER_INP = simpledialog.askinteger(title="Metronome", prompt="Select BPM (integer):")
    return(USER_INP)

# For testing
if __name__ == "__main__":
    get_bpm()