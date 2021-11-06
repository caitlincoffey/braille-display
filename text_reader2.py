"""
Contains the text reader object
"""
import letterToDots as conversions
import serial
import serial.tools.list_ports as list_ports
import time
#import binascii

startMarker = '<'
endMarker = '>'
dataStarted = False
dataBuf = ""
messageComplete = False

class textReader:
    Arduino_IDs = ((0x2341, 0x0043), (0x2341, 0x0001), 
                   (0x2A03, 0x0043), (0x2341, 0x0243), 
                   (0x0403, 0x6001), (0x1A86, 0x7523))

    def __init__(self, txt_file, port=''):
        """
        text
        """
        self.txt_file = txt_file # contains txt file name and path
        with open(self.txt_file, 'r') as f:
            self.text = f.read() # reads the whole file, does not read by line. will result in one giant string. also converts chars to lowercase.
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

    def read(self):
        """
        Reads text and converts text to braille
        """

        for char in self.text: 
            #bad way for now, add all mappings to a list. TODO make better way to read --> send
            if char.isupper(): # if character is uppercase
                #TODO deal with all caps edge case, if whole word is caps it's two dots
                mapping = conversions.mappings_alpha_num['cap']
                
            if char.isnumeric(): # if character is a number
                mapping = conversions.mappings_alpha_num['num']

            # we can do braille conversions here
            if char.lower() in conversions.mappings_punct:
                mapping = conversions.mappings_punct[char.lower()]

            elif char.lower() in conversions.mappings_alpha_num:
                mapping = conversions.mappings_alpha_num[char.lower()]
                # send things to arduino...

            elif char.lower() in conversions.mappings_punct2:
                # this will take up two cells, TODO
                mapping = conversions.mapping_punct2[char.lower()]
                # send things to arduino...
            else:
                print("Error: could not read char %s" % char)
                # TODO this is picking up new lines, should those be written in as just spaces?
            
            self.all_maps.append(mapping)

    def send_to_arduino(self, mapping, ind):

        global startMarker, endMarker

        cmd = "".join((conversions.b_to_ard[mapping[ind][0]], conversions.b_to_ard[mapping[ind][1]], conversions.b_to_ard[mapping[ind][2]])).encode()
        stringWithMarkers = (startMarker)
        cmd = cmd.decode("utf-8")
        stringWithMarkers += cmd
        stringWithMarkers += (endMarker)
        print("sending: ", stringWithMarkers.encode('utf-8'))
        self.dev.write(stringWithMarkers.encode('utf-8'))
    
    def recvFromArduino(self):
        global startMarker, endMarker, dataStarted, dataBuf, messageComplete

        msg = self.dev.read_until() # read until a new line
        #mystring = msg.decode()  # decode n return 
        return msg.decode()

        print("in waiting", self.dev.inWaiting())
        if self.dev.inWaiting() > 0 and messageComplete == False:
            x = self.dev.read()
            # x = str(x).replace('\\', '').replace("'", '').replace("bx", '')
            # print(x.encode("utf-8"))
            print('we made it!')
            #x = self.dev.read().decode()
            #if dataStarted == True:
                # if x != endMarker:
                #     dataBuf = dataBuf + x
                # else:
            dataStarted = False
            messageComplete = True
        
        if (messageComplete == True):
            messageComplete = False
            return dataBuf
        #else:
            #return "XXX"


if __name__ == "__main__":
    test_reader = textReader('test.txt')
    time.sleep(2)
    # reading text and converting to braille
    test_reader.read()

    # Sending data to arduino
    #letter1 = test_reader.send_to_arduino(test_reader.all_maps, 0)
    for ind in range(0, len(test_reader.all_maps)):
        #time.sleep(1)
        #print("We got here")
        test_reader.send_to_arduino(test_reader.all_maps, ind) # send it to arduino
        print("Sent to arduino")
        while "1" not in test_reader.recvFromArduino():
        #while test_reader.recvFromArduino() != "1\n":
            pass
        
        # while True:
        #     print("in while loop")
        #     var = test_reader.recvFromArduino()
        #     print(var)
        #     print(type(var))
        #     if var == "1\n": # TODO FIX 1? "1"?
        #         break # listen to arduino
        # print("Ready to send new message")
    #     print(test_reader.all_maps[ind])
    #     while True:
    #         #arduinoReply = test_reader.recvFromArduino()
    #         arduinoReply = 1
    #         #print("returning:", arduinoReply)
    #         if arduinoReply == "1" or arduinoReply == 1:
    #             time.sleep(2)
    #             test_reader.send_to_arduino(test_reader.all_maps, ind)
    #             print("SENT NEW THING")
    #             break # break out of while loop


    # # for ind in range(len(test_reader.all_maps)):
    # #     while True:
    # #         print("In While loop")
    # #         if (test_reader.dev.inWaiting() > 0):
    # #             print("In first if")
    # #             print(test_reader.dev.readline())
    # #             if (test_reader.dev.readline() == "1"):
    # #                 test_reader.send_to_arduino(test_reader.all_maps, ind)
    # #                 print("GOT A 1!!!")
    # #                 break

