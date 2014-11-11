import re

# lexerengine.py
# EECS 393 webide

# Specification from SDD for reference:
# LexerEngine - Text Editor’s syntax coloration depends on our custom Java lexical analysis engine. As
# input, the Lexer will periodically check source code that is currently open in a client’s Text Editor. 
# The resulting output will be a stream of tokens: each term in the source code will be mapped to a Java language element. 
# A term’s respective token will determine its syntax coloring.


class LexerEngine:

    # Open the code file, read it into a string, split the string around white space
    # input: name of the code file as a string
    # output: list of strings representing
    # TO-DO!!: THE WAY IM DOING THIS RN WONT HANDLE COMMENTS CORRECTLY BUT I GOTTA GET SOMETHING DOWN
    def string_rep(string filename):
        # open the file and put it in a "file" object
        file = open(filename)
        # read the file into a string
        file_string = read(file)
        # split the big string representing the code around white space
        # it gets put in a string list
        return file_string.split(" ")

    # Matches a single expression to a token and returns the token
    def tokenize(string expression):
        for k, v in regextable.iterItems():
            if matches(expression, k): return v

        # Scan the expr_list

    # Take a string and return the matching token from regextable
    # input: expression, the code fragment to be matched to a token
    # input: pattern, the regular expression in the regextable
    # output:
    def matches(string expression, string pattern):

        # re.search(regex, string) looks if the string matches the regex.
        # it returns a "match object." if there was a match, the object's value is true.
        match = re.search(pattern, expression)
        if match: return true
        else: return false








    def map_tokens_to_colors(list token_list):



# def0: scan the document, assign tokens, color text

# def1: (helper) assign a token to a lexeme.

# def2: (helper) color the text of a lexeme according to its token assignment.

regextable = {

	# Identifier
	'($\w+)|([a-zA-Z]w*)' : 'IDENTIFIER',

	# Keywords
	'abstract' : 'ABSTRACT',
	'assert' : 'ASSERT',
	'boolean' : 'BOOLEAN',
	'break' : 'BREAK',
	'byte' : 'BYTE',
	'case' : 'CASE',
	'catch' : 'CATCH',
	'char' : 'CHAR',
	'class' : 'CLASS',
	'const' : 'CONST',
	'continue' : 'CONTINUE',
	'default' : 'DEFAULT',
	'do' : 'DO',
	'double' : 'DOUBLE',
	'else' : 'ELSE',
	'extends' : 'EXTENDS',
	'final' : 'FINAL',
	'finally' : 'FINALLY',
	'float' : 'FLOAT',
	'for' : 'FOR',
	'goto' : 'GOTO',
	'if' : 'IF',
	'implements' : 'IMPLEMENTS',
	'import' : 'IMPORTS',
	'instanceof' : 'INSTANCEOF',
	'int' : 'INT',
	'interface' : 'INTERFACE',
	'long' : 'LONG',
	'native' : 'NATIVE',
	'new' : 'NEW',
	'package' : 'PACKAGE',
	'private' : 'PRIVATE',
	'protected' : 'PROTECTED',
	'public' : 'PUBLIC',
	'return' : 'RETURN',
	'short' : 'SHORT',
	'static' : 'STATIC',
	'strictfp' : 'STRICTFP',
	'super' : 'SUPER',
	'synchronized' : 'SYNCHRONIZED',
	'switch' : 'SWITCH',
	'this' : 'THIS',
	'throw' : 'THROW',
	'throws' : 'THROWS',
	'transient' : 'TRANSIENT',
	'try' : 'TRY',
	'void' : 'VOID',
	'volatile' : 'VOLATILE',
	'while' : 'WHILE',

	# Separators
    r';' : 'SEMICOLON',
    r',' : 'COMMA',
    r'.' : 'PERIOD',
    r'(' : 'LEFT-PAREN',
    r')' : 'RIGHT-PAREN',
    r'{' : 'LEFT-BRACE',
    r'}' : 'RIGHT-BRACE',
    r'[' : 'LEFT-BRACKET',
	r']' : 'RIGHT-BRACKET',

	# Operators
	'++' : 'INCREMENT',
	'--' : 'DECREMENT',
	'~' : 'BITWISE_COMPLEMENT',
	'!' : 'LOGICAL_NOT',
	#	Multiplicative
	'*' : 'MULTIPLY',
	'/' : 'DIVIDE',
	'%' : 'MODULO',
	#	Additive
	'+' : 'PLUS',
	'-' : 'MINUS',
	#	Shift
	'<<' : 'LEFT_SHIFT',
	'>>' : 'RIGHT_SHIFT',
	'>>>' : 'UNSIGNED_RIGHT_SHIFT',
	#	Relational
	'<' : 'LESS_THAN',
	'>' : 'GREATER THAN',
	'<=' : 'LT_OR_EQUAL_TO',
	'>=' : 'GT_OR_EQUAL_TO',
	#	Equality
	'==' : 'EQUAL_TO',
	'!=' : 'NOT_EQUAL_TO',
	#	Bitwise
	'&' : 'BITWISE_AND',
	'^' : 'BITWISE_XOR',
	'|' : 'BITWISE_OR',
	#	Logical
	'&&' : 'LOGICAL_AND',
	'||' : 'LOGICAL_OR',
	#	Consider adding esoteric operators like ternary, >>=, <<=, &=, |=, ^=
	#	list at https://www.cs.cmu.edu/~pattis/15-1XX/15-200/lectures/tokens/lecture.html

	# Literals
	'\d+|0[0-7]+|x[0-9a-fA-F]' : 'INT-LITERAL',
    # decimal, octal, hexadecimal
    '\d\.\d' : 'DOUBLE-LITERAL',
    'true|false' : 'BOOLEAN-LITERAL',
    '''[\s\S]?''' : 'CHAR-LITERAL',
    # a char in java is any single character in single quotes, or '', or ' '
    '''"[\s\S]*"''' : 'STRING-LITERAL', # Figure out how to color embedded string differently
    'null' : 'NULL-LITERAL',

	# Comments
	r'//[^\n]*\n' : 'LINE-COMMENT', # In a line comment, anything but a new line can be put after // (^\n = negate set: new line)
    r'/*[\s\S]*/' : 'BLOCK-COMMENT',

	# White space
    #'\s' : "WHITESPACE"

}