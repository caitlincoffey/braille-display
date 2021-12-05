"""
GUI for Braille Display
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

def send(event=None):
    global uploadedFile
    global filename
    if uploadedFile == True:
        with open(filename, 'r') as f:
            text = f.read() # reads the whole file, does not read by line. will result in one giant string. also converts chars to lowercase.
            print(text)
            reader = txt.textReader(text)

        time.sleep(2)
        reader.convert(2)
        print(reader.all_maps)

        for ind in range(0, len(reader.all_maps)):
            print("In %s character of loop" % str(ind))

            reader.send_to_arduino(reader.all_maps, ind) # send it to arduino
            print("Sent to arduino")
            while "1" not in reader.recvFromArduino():
                pass

        print("File selected:", filename)
        print("All sent to Arduino")

    else:
        text = textExample.get("1.0", "end-1c")
        reader = txt.textReader(text)
        time.sleep(2)
        reader.convert(2)
        print(reader.all_maps)

        for ind in range(0, len(reader.all_maps)):
            print("In %s character of loop" % str(ind))
        
            reader.send_to_arduino(reader.all_maps, ind) # send it to arduino
            print("Sent to arduino")
            while "1" not in reader.recvFromArduino():
                pass

        print("All sent to Arduino")

    pass

def uploadFile(event=None):
    global uploadedFile 
    global filename
    filename = filedialog.askopenfilename() 
    uploadedFile = True

# def sendText(content):
#     print("This is the content: %s" % content)
#     reader = txt.textReader(content)
#     time.sleep(2)
#     reader.convert(2)
#     print(reader.all_maps)

#     for ind in range(0, len(reader.all_maps)):
#         print("In %s character of loop" % str(ind))
    
#         reader.send_to_arduino(reader.all_maps, ind) # send it to arduino
#         print("Sent to arduino")
#         while "1" not in reader.recvFromArduino():
#             pass

#     print("All sent to Arduino")

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
