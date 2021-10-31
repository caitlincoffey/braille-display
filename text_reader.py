"""
Contains the text reader object
"""
import letterToDots as conversions

class textReader:
    def __init__(self, txt_file):
        """
        text
        """
        self.txt_file = txt_file # contains txt file name and path

    def read(self):
        """
        text
        """
        with open(self.txt_file, 'r') as f:
            text = f.read() # reads the whole file, does not read by line. will result in one giant string. also converts chars to lowercase.

        for char in text: 
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


if __name__ == "__main__":
    test_reader = textReader('test.txt')
    test_reader.read()