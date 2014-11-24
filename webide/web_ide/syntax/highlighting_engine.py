from webide.web_ide.syntax import plyj as plyj


class HighlightingEngine(object):

    color_table = {

        'NAME' : '#9966FF', # LIGHT-PURPLE

        # Keywords - BLUE
        'ABSTRACT' : '#0033CC',
        'ASSERT' : '#0033CC',
        'BOOLEAN' : '#0033CC',
        'BREAK' : '#0033CC',
        'BYTE' : '#0033CC',
        'CASE' : '#0033CC',
        'CATCH' : '#0033CC',
        'CHAR' : '#0033CC',
        'CLASS' : '#0033CC',
        'CONST' : '#0033CC',
        'CONTINUE' : '#0033CC',
        'DEFAULT' : '#0033CC',
        'DO' : '#0033CC',
        'DOUBLE' : '#0033CC',
        'ELSE' : '#0033CC',
        'EXTENDS' : '#0033CC',
        'FINAL' : '#0033CC',
        'FINALLY' : '#0033CC',
        'FLOAT' : '#0033CC',
        'FOR' : '#0033CC',
        'GOTO' : '#0033CC',
        'IF' : '#0033CC',
        'IMPLEMENTS' : '#0033CC',
        'IMPORTS' : '#0033CC',
        'INSTANCEOF' : '#0033CC',
        'INT' : '#0033CC',
        'INTERFACE' : '#0033CC',
        'LONG' : '#0033CC',
        'NATIVE' : '#0033CC',
        'NEW' : '#0033CC',
        'PACKAGE' : '#0033CC',
        'PRIVATE' : '#0033CC',
        'PROTECTED' : '#0033CC',
        'PUBLIC' : '#0033CC',
        'RETURN' : '#0033CC',
        'SHORT' : '#0033CC',
        'STATIC' : '#0033CC',
        'STRICTFP' : '#0033CC',
        'SUPER' : '#0033CC',
        'SYNCHRONIZED' : '#0033CC',
        'SWITCH' : '#0033CC',
        'THIS' : '#0033CC',
        'THROW' : '#0033CC',
        'THROWS' : '#0033CC',
        'TRANSIENT' : '#0033CC',
        'TRY' : '#0033CC',
        'VOID' : '#0033CC',
        'VOLATILE' : '#0033CC',
        'WHILE' : '#0033CC',

        # Literals
        'NUM' : '#0099FF', # light blue
        'CHAR_LITERAL' : '#FF99CC', # pink
        'STRING_LITERAL' : '#FF3300', # red

        # Comments
        'LINE_COMMENT' : '#009933', # LIGHT-GREEN
        'BLOCK_COMMENT' : '#009933' }

    token_to_color_map = {}

    def highlight_syntax(self, filename):
        # tokenizing
        f = open(filename)
        parser = plyj.Parser()
        parser.tokenize_file(f)
        token_list = parser.token_list
        # list contains instances of LexToken from PLY (Python Lex-Yacc)
        # e.g. LexToken(PUBLIC,'public',1,0)
        for t in token_list:
            self.token_to_color_map[t] = self.highlight_element(t)

    # return the hex color code for a single token
    def highlight_element(self, token):
        type = token.type
        for k, v in self.color_table.iteritems():
            if (type == k): return v
            else: return 'default'


