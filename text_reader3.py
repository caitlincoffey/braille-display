"""
Contains the text reader object
"""
import letterToDots as conversions
import serial
import serial.tools.list_ports as list_ports
import time
import pybrl as brl

startMarker = '<'
endMarker = '>'
dataStarted = False
dataBuf = ""
messageComplete = False

class textReader:
    Arduino_IDs = ((0x2341, 0x0043), (0x2341, 0x0001), 
                   (0x2A03, 0x0043), (0x2341, 0x0243), 
                   (0x0403, 0x6001), (0x1A86, 0x7523))

    def __init__(self, port=''):
        """
        Connects to Arduino, listens on Serial 115200 by default
        """
        self.all_maps = []
        # Taken from example code provided by PIE Teaching Team
        # https://github.com/bminch/PIE/blob/main/Serial_cmd.py
        if port == '':
            self.dev = None
            self.connected = False
            devices = list_ports.comports()
            for device in devices:
                if (device.vid, device.pid) in textReader.Arduino_IDs:
                    try:
                        self.dev = serial.Serial(device.device, 115200)
                        self.connected = True
                        print('Connected to {!s}...'.format(device.device))
                    except:
                        pass
                if self.connected:
                    break
        else:
            try:
                self.dev = serial.Serial(port, 115200)
                self.connected = True
            except:
                self.edev = None
                self.connected = False
    
    def add_raw_text(self, text):
        self.text = text

    def convert(self, grade=1):
        """
        Convert text to braille (grade 1 or grade 2)
        """
        if grade == 2:
            raw_maps = brl.translate(self.text)
            for list in raw_maps:
                self.all_maps.append([(0, 0), (0, 0), (0, 0)])
                for char in list:
                    self.all_maps.append(self.char_to_tuple(char))
            # removing first space
            self.all_maps.pop(0)
        else:
            self.convert_grade1()

    def char_to_tuple(self, ch):
        return [(int(ch[0]), int(ch[3])), (int(ch[1]), int(ch[4])), (int(ch[2]), int(ch[5]))]
        
    def convert_grade1(self):
        """
        Reads text and converts text to braille.
        Adds mappings to a list, mapping is a length-6 tuple.
        """
        for char in self.text: 
            if char.isupper(): # if character is uppercase
                mapping = conversions.mappings_alpha_num['cap']
                self.all_maps.append(mapping)

            if char.isnumeric(): # if character is a number
                mapping = conversions.mappings_alpha_num['num']
                self.all_maps.append(mapping)
                
            if char.lower() in conversions.mappings_punct:
                mapping = conversions.mappings_punct[char.lower()]

            elif char.lower() in conversions.mappings_alpha_num:
                mapping = conversions.mappings_alpha_num[char.lower()]

            elif char.lower() in conversions.mappings_punct2:
                mapping = conversions.mappings_punct2[char.lower()]
            
            self.all_maps.append(mapping)

    def send_to_arduino(self, mapping, ind):
        """
        Procedure for sending information to Arduino
        """
        global startMarker, endMarker

        cmd = "".join((conversions.b_to_ard[mapping[ind][0]], conversions.b_to_ard[mapping[ind][1]], conversions.b_to_ard[mapping[ind][2]])).encode()
        stringWithMarkers = (startMarker)
        cmd = cmd.decode("utf-8")
        stringWithMarkers += cmd
        stringWithMarkers += (endMarker)
        self.dev.write(stringWithMarkers.encode('utf-8'))
    
    def recvFromArduino(self):
        """
        Procedure for receiving information from Arduino
        """
        global startMarker, endMarker, dataStarted, dataBuf, messageComplete

        msg = self.dev.read_until() # read until a new line
        return msg.decode()