"""
GUI for Braille Display

TODO: Have python read in what grade arduino sent
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
    takes reader object
    """
    global grade 

    #time.sleep(2) 
    # BEFORE THE REST OF THIS CODE, CHECK BRAILLE1 VS BRAILLE2
    # TODO figure out if recvFromArduino is smart, does it send this now or do we have to store that info

    # # tell arduino to send grade of braille by sending 'grade'


    # # read grade of braille from arduino
    # grade_read = reader.recvFromArduino()
    # if "2" in grade_read:
    #     grade = 1
    # elif "3" in grade_read:
    #     grade = 2

    reader.convert(grade)
    print(reader.all_maps)
    for ind in range(0, len(reader.all_maps)):
        #print("In %s character of loop" % str(ind))

        reader.send_to_arduino(reader.all_maps, ind) # send it to arduino
        #print("Sent to arduino")
        #print('Received from arduino', reader.recvFromArduino())
        while "1" not in reader.recvFromArduino():
            pass

    print("All sent to Arduino")

def send(event=None): #Hit button "Send to Braille Display"
    global uploadedFile
    global filename
    global grade
    global startMarker, endMarker

    reader = txt.textReader()
    time.sleep(2)
    # tell arduino to send grade of braille
    cmd = "grade".encode()
    stringWithMarkers = (startMarker)
    cmd = cmd.decode("utf-8")
    stringWithMarkers += cmd
    stringWithMarkers += (endMarker)
    #print("sending: ", stringWithMarkers.encode('utf-8'))
    reader.dev.write(stringWithMarkers.encode('utf-8'))
    gradeRaw = reader.recvFromArduino()
    if "3" in gradeRaw:
        grade = 2
        #print("Grade 2 braille")
    else:
        grade = 1
        #print("Grade 1 braille")

    # gradesFromArduno = {"2", "3"}
    # while True:
    #     grade_recv = reader.recvFromArduino()
    #     print(grade_recv)
    #     if grade_recv in gradesFromArduno:
    #         grade = grade_recv
    #         break

    if uploadedFile == True:
        with open(filename, 'r') as f:
            #print("File selected:", filename)
            text = f.read() # reads the whole file, does not read by line. will result in one giant string. also converts chars to lowercase.
            #print(text)
            #reader = txt.textReader(text)
            reader.add_raw_text(text)
            sendToArduino(reader)


    else:
        text = textExample.get("1.0", "end-1c")
        #reader = txt.textReader(text)
        reader.add_raw_text(text)
        sendToArduino(reader)
    

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
