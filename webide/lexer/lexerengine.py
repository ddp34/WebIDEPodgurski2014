import re
import regextable

# lexerengine.py
# EECS 393 webide

# Specification from SDD for reference:
# LexerEngine - Text Editor’s syntax coloration depends on our custom Java lexical analysis engine. As
# input, the Lexer will periodically check source code that is currently open in a client’s Text Editor. 
# The resulting output will be a stream of tokens: each term in the source code will be mapped to a Java language element. 
# A term’s respective token will determine its syntax coloring.


class LexerEngine:



    def tokenize(string filename):

        # Open the text file representing the program

        # Scan the text file and map

    # Take a string and return the matching token from regextable
    def string_to_token(string expression):

        # If the input string matches a regular expression in the regextable








    def map_tokens_to_colors(list token_list):



# def0: scan the document, assign tokens, color text

# def1: (helper) assign a token to a lexeme.

# def2: (helper) color the text of a lexeme according to its token assignment.

