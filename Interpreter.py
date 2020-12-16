PLUS_TOKEN = 'PLUS'
MIN_TOKEN = 'MIN'
DIV_TOKEN = 'DIV'
MUL_TOKEN = 'MUL'
INC_TOKEN = 'INC'
DEC_TOKEN = 'DEC'
SEMICOLON_TOKEN = 'SEMICOLON'
COLON_TOKEN = 'COLON'
DOT_TOKEN = 'DOT'
LEFT_PAR_TOKEN = 'LEFT_PAR'
RIGHT_PAR_TOKEN = 'RIGHT_PAR'

SUGAR = '.;:()'
OPERATORS = '*/-+'


class Token:
    def __init__(self, type, value=None):
        self.value = value
        self.type = type

    def __repr__(self):
        if self.value is None:
            return f'{self.type}'
        else:
            return f'{self.type}->{self.value}'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.char = None
        self.pos = -1
        self.xy = [0, 1]
        self.advance()

    def advance(self):
        self.pos += 1
        self.xy[0] += 1

        if self.pos < len(self.text):
            self.char = self.text[self.pos]
        else:
            self.char = None

    def newline(self):
        self.xy[0] = 0
        self.xy[1] += 1
        self.advance()

    def lex(self):
        tokens = []

        while self.char is not None:
            if self.char in '\t ':
                self.advance()
            elif self.char == '\n':
                self.newline()
            elif self.char in SUGAR:
                tokens.append(self.sugar())
                self.advance()
            elif self.char in OPERATORS:
                res = self.operator()
                if res is not None:
                    tokens.append(res)
                self.advance()

        return tokens

    def sugar(self):
        if self.char == ';':
            return Token(SEMICOLON_TOKEN)
        elif self.char == ':':
            return Token(COLON_TOKEN)
        elif self.char == '.':
            return (Token(DOT_TOKEN))
        elif self.char == '(':
            return Token(LEFT_PAR_TOKEN)
        elif self.char == ')':
            return Token(RIGHT_PAR_TOKEN)

    def operator(self):
        if self.char == '+':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '+':
                self.advance()
                return Token(INC_TOKEN)
            else:
                return Token(PLUS_TOKEN)
        elif self.char == '-':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '-':
                self.advance()
                return Token(DEC_TOKEN)
            else:
                return Token(MIN_TOKEN)
        elif self.char == '/':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                self.comment()
            else:
                return Token(DIV_TOKEN)
        elif self.char == '*':
            return Token(MUL_TOKEN)

    def comment(self):
        while self.char is not None and self.char != '\n':
            self.advance()


def run(text):
    lexer = Lexer(text)
    return lexer.lex()
