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
            text = f.read().lower() # reads the whole file, does not read by line. will result in one giant string. also converts chars to lowercase.

        for char in text: 
            # we can do braille conversions here
            if char in conversions.mappings_punct:
                mapping = conversions.mappings_punct[char]
                # send things to arduino...

            elif char in conversions.mappings_alpha_num:
                mapping = conversions.mappings_alpha_num[char]
                # send things to arduino...

            elif char in conversions.mappings_punct2:
                mapping = conversions.mapping_punct2[char]
                # send things to arduino...
            else:
                print("Error: could not read char %s" % char)
                # TODO this is picking up new lines, should those be written in as just spaces?


if __name__ == "__main__":
    test_reader = textReader('test.txt')
    test_reader.read()