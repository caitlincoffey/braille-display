# Go from letter/number/character to combination of braille dots
# Format: codes are in dictionary with character:braille 
# braille is a list of tuples where it is dot [(1,4), (2,5), (3,6)] with each being 0 (low) or 1 (raised)
# Each tuple represents a row of braille cell (controlled by each cam)
# mappings from: https://www.pharmabraille.com/pharmaceutical-braille/the-braille-alphabet/
mappings_alpha_num = {'a': [(1,0), (0,0), (0,0)], 'b': [(1,0), (1,0), (0,0)], 'c': [(1,1), (0,0), (0,0)], 
'd': [(1,1), (0,1), (0,0)], 'e': [(1,0), (0,1), (0,0)], 'f': [(1,1), (1,0), (0,0)],
'g': [(1,1), (1,1), (0,0)], 'h': [(1,0), (1,1), (0,0)], 'i': [(0,1), (1,0), (0,0)],
'j': [(0,1), (1,1), (0,0)], 'k': [(1,0), (0,0), (1,0)], 'l': [(1,0), (1,0), (1,0)],
'm': [(1,1), (0,0), (1,0)], 'n': [(1,1), (0,1), (1,0)], 'o': [(1,0), (0,1), (1,0)],
'p': [(1,1), (1,0), (1,0)], 'q': [(1,1), (1,1), (1,0)], 'r': [(1,0), (1,1), (1,0)],
's': [(0,1), (1,0), (1,0)], 't': [(0,1), (1,1), (1,0)], 'u': [(1,0), (0,0), (1,1)],
'v': [(1,0), (1,0), (1,1)], 'w': [(0,1), (1,1), (0,1)], 'x': [(1,1), (0,0), (1,1)],
'y': [(1,1), (0,1), (1,1)], 'z': [(1,0), (0,1), (1,1)], 'num': [(0,1), (0,1), (1,1)],
1: [(1,0), (0,0), (0,0)], 2: [(1,0), (1,0), (0,0)], 3: [(1,1), (0,0), (0,0)],
4: [(1,1), (0,1), (0,0)], 5: [(1,0), (0,1), (0,0)], 6: [(1,1), (1,0), (0,0)],
7: [(1,1), (1,1), (0,0)], 8: [(1,0), (1,1), (0,0)], 9: [(0,1), (1,0), (0,0)],
0: [(0,1), (1,1), (0,0)], 'cap': [(0,0), (0,0), (0,1)], ' ': [(0,0), (0,0), (0,0)]}

mappings_punct = {',': [(0,0), (1,0), (0,0)],
';': [(0,0), (1,0), (1,0)], ':': [(0,0), (1,1), (0,0)], '.': [(0,0), (1,1), (0,1)],
'?': [(0,0), (1,0), (1,1)], '!': [(0,0), (1,1), (1,0)], "'": [(0,0), (0,0), (1,0)],
'-': [(0,0), (0,0), (1,1)]}

#TODO some of these take 2 cells - how to represent in dictionary?
mappings_punct2 = {'"': [(0,0), (0,0), (1,0), (0,0), (1,1), (1,1)], 
'(': [(0,0), (0,1), (0,0), (1,0), (1,0), (0,1)], ')': [(0,0), (0,1), (0,0), (0,1), (0,1), (1,0)],
'/': [(0,1), (0,1), (0,1), (0,1), (0,0), (1,0)], "\\": [(0,1), (0,1), (0,1), (1,0), (0,0), (0,1)]}

b_to_ard = {(0,0): 'A', (1,1): 'B', (0,1): 'C', (1,0): 'D'}

mappings_braille2 = {'and': [(1,1), (1,0), (1,1)], 'for': [(1,1), (1,1), (1,1)],
'of': [(0, 1), (1, 1), (1,1)], 'the': [(0, 1), (1, 0), (1, 1)], 'with': [(0, 1), (1, 1), (1, 1)],
'ch': [(1, 0), (0, 0), (0, 1)], 'gh': [(1, 0), (1, 0), (0, 1)], 'sh': [(1, 1), (0, 0), (0, 1)],
'th': [(1, 1), (0, 1), (0, 1)], 'wh': [(1, 0), (0, 1), (0, 1)], 
'ed': [(1, 1), (1, 0), (0, 1)], 'er': [(1, 1), (1, 1), (0, 1)], 
'ou': [(1, 0), (1, 1), (0, 1)], 'ow': [(0, 1), (1, 0), (0, 1)]}

mappings_words = {'and': [(1,1), (1,0), (1,1)], 'for': [(1,1), (1,1), (1,1)], 'of': [(0, 1), (1, 1), (1,1)], 
'the': [(0, 1), (1, 0), (1, 1)], 'with': [(0, 1), (1, 1), (1, 1)]}