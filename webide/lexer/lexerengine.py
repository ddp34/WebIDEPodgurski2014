# lexerengine.py
# EECS 393 webide

# Specification from SDD for reference:
# LexerEngine - Text Editor’s syntax coloration depends on our custom Java lexical analysis engine. As
# input, the Lexer will periodically check source code that is currently open in a client’s Text Editor. 
# The resulting output will be a stream of tokens: each term in the source code will be mapped to a Java language element. 
# A term’s respective token will determine its syntax coloring.


#elementRegexes: HashMap<String, String>
# An associative array of key-value pairs key:regex -> value:token
# Each text element is scanned and assigned a token based on which regex it matches

#Method: tokensToElements(String[]) : String[]
#Using regexes, parse the stream of tokens and and convert each to a Java language element. 
