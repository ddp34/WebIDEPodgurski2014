from plyj import parser as plyj


class HighlightingEngine(object):

    color_table = dict(NAME='#9966FF', ABSTRACT='#0033CC', ASSERT='#0033CC', BOOLEAN='#0033CC', BREAK='#0033CC',
                       BYTE='#0033CC', CASE='#0033CC', CATCH='#0033CC', CHAR='#0033CC', CLASS='#0033CC',
                       CONST='#0033CC', CONTINUE='#0033CC', DEFAULT='#0033CC', DO='#0033CC', DOUBLE='#0033CC',
                       ELSE='#0033CC', EXTENDS='#0033CC', FINAL='#0033CC', FINALLY='#0033CC', FLOAT='#0033CC',
                       FOR='#0033CC', GOTO='#0033CC', IF='#0033CC', IMPLEMENTS='#0033CC', IMPORTS='#0033CC',
                       INSTANCEOF='#0033CC', INT='#0033CC', INTERFACE='#0033CC', LONG='#0033CC', NATIVE='#0033CC',
                       NEW='#0033CC', PACKAGE='#0033CC', PRIVATE='#0033CC', PROTECTED='#0033CC', PUBLIC='#0033CC',
                       RETURN='#0033CC', SHORT='#0033CC', STATIC='#0033CC', STRICTFP='#0033CC', SUPER='#0033CC',
                       SYNCHRONIZED='#0033CC', SWITCH='#0033CC', THIS='#0033CC', THROW='#0033CC', THROWS='#0033CC',
                       TRANSIENT='#0033CC', TRY='#0033CC', VOID='#0033CC', VOLATILE='#0033CC', WHILE='#0033CC',
                       NUM='#0099FF', CHAR_LITERAL='#FF99CC', STRING_LITERAL='#FF3300', LINE_COMMENT='#009933',
                       BLOCK_COMMENT='#009933')

    token_to_color_map = {}

    def highlight_syntax(self, filename):
        # tokenizing
        f = open(filename)
        parser = plyj.Parser()
        parser.tokenize_file(f)
        token_list = parser.token_list
        tokens = [] # LexTokens are converted to a list [TYPE, VALUE, LINENUM, POSITION(INLINE)]
        for t in token_list:
            tokens.append(self.rep_tok_as_list(t))

        # list contains instances of LexToken from PLY (Python Lex-Yacc)
        # e.g. LexToken(PUBLIC,'public',1,0)
        for t in tokens:
            t.append(self.highlight_element(t))
        print tokens
    # return the hex color code for a single token
    def highlight_element(self, token):
        toktype = token[0]
        if toktype in self.color_table: return self.color_table[toktype]
        else: return 'default'

    def rep_tok_as_list(self, token):
        li = []
        li.append(str(token.type))
        li.append(token.value)
        li.append(token.lineno)
        li.append(token.lexpos)
        return li



