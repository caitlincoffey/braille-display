"""
Contains the text reader object
"""
import letterToDots as conversions
import serial
import serial.tools.list_ports as list_ports
import time

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
        text
        """
        # with open(self.txt_file, 'r') as f:
        #     text = f.read() # reads the whole file, does not read by line. will result in one giant string. also converts chars to lowercase.

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
            # send things to arduino...

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
        cmd = "".join((conversions.b_to_ard[mapping[ind][0]], conversions.b_to_ard[mapping[ind][1]], conversions.b_to_ard[mapping[ind][2]])).encode()
        self.dev.write(cmd)

if __name__ == "__main__":
    test_reader = textReader('test.txt')
    time.sleep(2)
    #char1 = test_reader.read()
    test_reader.read()
    letter1 = test_reader.send_to_arduino(test_reader.all_maps, 0)
    #print(letter1)
    #textReader.send_to_arduino(letter1)
    #print(test_reader.all_maps[0])
    #print(test_reader.send_to_arduino(test_reader.all_maps, 0))
    #print(char1)