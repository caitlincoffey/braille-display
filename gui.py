"""
GUI for Braille Display (Runs text_reader3.py)
"""

import tkinter as tk
import text_reader3 as txt
from tkinter import filedialog
import time

root = tk.Tk()
root.title("Braille Display GUI")
root.geometry("1000x800")

uploadedFile = False
filename = ""
grade = 1

startMarker = '<'
endMarker = '>'

def sendToArduino(reader):
    """
    Sends text to Arduino using text_reader3.py send_to_arduino()
        Args: Reader object
    """
    global grade 
    reader.convert(grade)

    for ind in range(0, len(reader.all_maps)):
        reader.send_to_arduino(reader.all_maps, ind) # send it to arduino
        while "1" not in reader.recvFromArduino():
            pass

    print("All sent to Arduino")

def send(event=None): #Hit button "Send to Braille Display"
    """
    Starts send process to Arduino
    """
    global uploadedFile
    global filename
    global grade
    global startMarker, endMarker

    reader = txt.textReader()
    time.sleep(2)

    # Tell arduino to send grade of braille
    cmd = "grade".encode()
    stringWithMarkers = (startMarker)
    cmd = cmd.decode("utf-8")
    stringWithMarkers += cmd
    stringWithMarkers += (endMarker)
    reader.dev.write(stringWithMarkers.encode('utf-8'))
    gradeRaw = reader.recvFromArduino()

    if "3" in gradeRaw:
        grade = 2
        # Grade 2 braille
    else:
        grade = 1
        # Grade 1 braille

    if uploadedFile == True:
        with open(filename, 'r') as f:
            text = f.read() # reads the whole file, does not read by line. will result in one giant string. also converts chars to lowercase.
            reader.add_raw_text(text)
            sendToArduino(reader)
    else:
        text = textExample.get("1.0", "end-1c")
        reader.add_raw_text(text)
        sendToArduino(reader)
    

def uploadFile(event=None):
    global uploadedFile 
    global filename
    filename = filedialog.askopenfilename() 
    uploadedFile = True

textLabel = tk.Label(root, text="Enter text in textbox below:", font=("Arial", 25), pady=10)
textLabel.pack()

textExample = tk.Text(root,
                      height=10, width=50, font=("Arial", 16))
textExample.pack()

space = tk.Label(root, text="", pady=5)
space.pack()

space = tk.Label(root, text="Or", font=("Arial", 20), pady=20)
space.pack()

btnFile = tk.Button(root,
                   height=2,
                   width=20, bg="black", fg="white",
                   text="Upload Text File", font=("Arial", 20),
                   command=lambda:uploadFile())
btnFile.pack()

space = tk.Label(root, text="", pady=20)
space.pack()

btnSet = tk.Button(root,
                   height=2,
                   width=20, bg="black", fg="white",
                   text="Send to Braille Display", font=("Arial", 20),
                   command=lambda:send())
btnSet.pack()

space = tk.Label(root, text="", pady=20)
space.pack()

quit = tk.Button(root, height=2,
                   width=10, bg="black", fg="white",
                   text="Quit", font=("Arial", 20),
                   command=root.destroy)
quit.pack()

root.mainloop()
