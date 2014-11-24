'''
textconvert.py

This file contains utilities to translate from HTML display text in the editor
to valid Java source code. This is accomplished by translating between standard plaintext
tokens such as '\n' to their HTML equivalents, such as '<br />'.
'''

import re

class TextConvert:

    '''
    Adds in backslashes to plaintext newlines
    so they can be supported by Javascript.
    '''
    def newlinesToJS(self, plaintext):
        return plaintext.replace("\n", "\n\\")
