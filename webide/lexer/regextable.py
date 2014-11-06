"""
Java token types
Identifiers: names the programmer chooses
Keywords: names already in the programming language
Separators (also known as punctuators): punctuation characters and paired-delimiters
Operators: symbols that operate on arguments and produce results
Literals (specified by their type)
Numeric: int and double
Logical: boolean
Textual: char and String
Reference: null
Comments
Line
Block

EBNF: token <= identifier | keyword | separator | operator | literal | comment
"""

RegexTable = {

	# format for copy/pasting ( '', ''),

	# Identifier
	( '($\w+)|([a-zA-Z]w*)', 'IDENTIFIER'),
	
	# Keywords
	( 'abstract', 'ABSTRACT'),
	( 'assert', 'ASSERT'),
	( 'boolean', 'BOOLEAN'),
	( 'break', 'BREAK'),
	( 'byte', 'BYTE'),
	( 'case', 'CASE'),
	( 'catch', 'CATCH'),
	( 'char', 'CHAR'),
	( 'class', 'CLASS'),
	( 'const', 'CONST'),
	( 'continue', 'CONTINUE'),
	( 'default', 'DEFAULT'),
	( 'do', 'DO'),
	( 'double', 'DOUBLE'),
	( 'else', 'ELSE'),
	( 'extends', 'EXTENDS'),
	( 'final', 'FINAL'),
	( 'finally', 'FINALLY'),
	( 'float', 'FLOAT'),
	( 'for', 'FOR'),
	( 'goto', 'GOTO'),
	( 'if', 'IF'),
	( 'implements', 'IMPLEMENTS'),
	( 'import', 'IMPORTS'),
	( 'instanceof', 'INSTANCEOF'),
	( 'int', 'INT'),
	( 'interface', 'INTERFACE'),
	( 'long', 'LONG'),
	( 'native', 'NATIVE'),
	( 'new', 'NEW'),
	( 'package', 'PACKAGE'),
	( 'private', 'PRIVATE'),
	( 'protected', 'PROTECTED'),
	( 'public', 'PUBLIC'),
	( 'return', 'RETURN'),
	( 'short', 'SHORT'),
	( 'static', 'STATIC'),
	( 'strictfp', 'STRICTFP'),
	( 'super', 'SUPER'),
	( 'synchronized', 'SYNCHRONIZED'),
	( 'switch', 'SWITCH'),
	( 'this', 'THIS'),
	( 'throw', 'THROW'),
	( 'throws', 'THROWS'),
	( 'transient', 'TRANSIENT'),
	( 'try', 'TRY'),
	( 'void', 'VOID'),
	( 'volatile', 'VOLATILE'),
	( 'while', 'WHILE'),
	
	# Separators
    ( r';', 'SEMICOLON'),
    ( r',', 'COMMA'),
    ( r'.', 'PERIOD'),
    ( r'(', 'LEFT-PAREN'),
    ( r')', 'RIGHT-PAREN'),
    ( r'{', 'LEFT-BRACE'),
    ( r'}', 'RIGHT-BRACE'),
    ( r'[', 'LEFT-BRACKET'),
	( r']', 'RIGHT-BRACKET'),

	# Operators
	( '++', 'INCREMENT'),
	( '--', 'DECREMENT'), 
	( '~', 'BITWISE_COMPLEMENT'),
	( '!', 'LOGICAL_NOT'),
	#	Multiplicative
	( '*', 'MULTIPLY'),
	( '/', 'DIVIDE'),
	( '%', 'MODULO'),
	#	Additive
	( '+', 'PLUS'),
	( '-', 'MINUS'),
	#	Shift
	( '<<', 'LEFT_SHIFT'),
	( '>>', 'RIGHT_SHIFT'),
	( '>>>', 'UNSIGNED_RIGHT_SHIFT'),
	#	Relational
	( '<', 'LESS_THAN'),
	( '>', 'GREATER THAN'),
	( '<=', 'LT_OR_EQUAL_TO'),
	( '>=', 'GT_OR_EQUAL_TO'),
	#	Equality
	( '==', 'EQUAL_TO'),
	( '!=', 'NOT_EQUAL_TO'),
	#	Bitwise
	( '&', 'BITWISE_AND'),
	( '^', 'BITWISE_XOR'),
	( '|', 'BITWISE_OR'),
	#	Logical
	( '&&', 'LOGICAL_AND'),
	( '||', 'LOGICAL_OR'),
	#	Consider adding esoteric operators like ternary, >>=, <<=, &=, |=, ^=
	#	list at https://www.cs.cmu.edu/~pattis/15-1XX/15-200/lectures/tokens/lecture.html

	# Literals
	( '\d+|0[0-7]+|x[0-9a-fA-F]' , 'INT-LITERAL'),
    # decimal, octal, hexadecimal
    ( '\d\.\d', 'DOUBLE-LITERAL'),
    ( 'true|false', 'BOOLEAN-LITERAL'),
    ( '''[\s\S]?''', 'CHAR-LITERAL'),
    # a char in java is any single character in single quotes, or '', or ' '
    ( '''"[\s\S]*"''', 'STRING-LITERAL'), # Figure out how to color embedded string differently
    ( 'null', 'NULL-LITERAL'),
	
	# Comments
	( r'//[^\n]*\n', 'LINE-COMMENT'), # In a line comment, anything but a new line can be put after // (^\n = negate set: new line)
    ( r'/*[\s\S]*/', 'BLOCK-COMMENT'),

	# White space
    ( '\s', "WHITESPACE")

}
