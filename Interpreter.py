import string

PLUS_TOKEN = 'PLUS'
MIN_TOKEN = 'MIN'
DIV_TOKEN = 'DIV'
MUL_TOKEN = 'MUL'
INC_TOKEN = 'INC'
DEC_TOKEN = 'DEC'
SEMICOLON_TOKEN = 'SEMICOLON'
COLON_TOKEN = 'COLON'
DOT_TOKEN = 'DOT'
COMMA_TOKEN = 'COMMA'
LEFT_PAR_TOKEN = 'LEFT_PAR'
RIGHT_PAR_TOKEN = 'RIGHT_PAR'
GT_TOKEN = 'GT'
GTE_TOKEN = 'GTE'
LT_TOKEN = 'LT'
LTE_TOKEN = 'LTE'
EQ_TOKEN = 'EQ'
NEQ_TOKEN = 'NEQ'
ASSIGN_TOKEN = 'ASSIGN'
ID_TOKEN = 'ID'
INTERO_TOKEN = 'INT'
DECIMALE_TOKEN = 'DECIM'
STRINGA_TOKEN = 'STR'

ERROR = 'ERROR'
RED_STRING = '\033[91m'

SUGAR = '.,;:()'
OPERATORS = '*/-+'
REL_OPERATORS = '<>=!'
LETTERS = string.ascii_letters
DIGITS = '0123456789'
ALPHANUM = LETTERS + DIGITS
KEYWORDS = ['INTERO', 'DECIMALE', 'STRINGA', 'BOOLEAN', 'INIZIO', 'FINE', 'STOP', 'RADICE',
            'SE', 'VERO', 'FAI', 'FALSO', 'RIPETI', 'VOLTE', 'SCRIVI', 'INSERISCI', 'E', 'O']


class Token:
    def __init__(self, type, value=None):
        self.value = value
        self.type = type

    def __repr__(self):
        if self.value is None:
            return f'Type:{self.type}\n'
        else:
            return f'Type:{self.type} :: Value:{self.value}\n'


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
            elif self.char in REL_OPERATORS:
                rel_op = self.rel_operator()
                if rel_op == -1:
                    return ERROR
                else:
                    tokens.append(rel_op)
                self.advance()
            elif self.char in LETTERS:
                tokens.append(self.alpha_num())
            elif self.char in DIGITS:
                num_const = self.num_const()
                if num_const == -1:
                    return ERROR
                else:
                    tokens.append(num_const)
            elif self.char == '"':
                str_const = self.str_const()
                if str_const == -1:
                    return ERROR
                else:
                    tokens.append(str_const)
                self.advance()
            else:
                self.error('unknown_char')
                return ERROR

        return tokens

    def sugar(self):
        if self.char == ';':
            return Token(SEMICOLON_TOKEN)
        elif self.char == ':':
            return Token(COLON_TOKEN)
        elif self.char == '.':
            return Token(DOT_TOKEN)
        elif self.char == '(':
            return Token(LEFT_PAR_TOKEN)
        elif self.char == ')':
            return Token(RIGHT_PAR_TOKEN)
        elif self.char == ',':
            return Token(COMMA_TOKEN)

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

    def rel_operator(self):
        if self.char == '<':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                return Token(LTE_TOKEN)
            else:
                return Token(LT_TOKEN)
        elif self.char == '>':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                return Token(GTE_TOKEN)
            else:
                return Token(GT_TOKEN)
        elif self.char == '=':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                return Token(EQ_TOKEN)
            else:
                return Token(ASSIGN_TOKEN)
        elif self.char == '!':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                return Token(NEQ_TOKEN)
            else:
                self.advance()
                self.error('=_expected')
                return -1

    def alpha_num(self):
        string = self.char
        self.advance()
        while self.char is not None and self.char in ALPHANUM:
            string += self.char
            self.advance()
        if string.upper() in KEYWORDS:
            return Token(string.upper())
        else:
            return Token(ID_TOKEN, string)

    def num_const(self):
        num = ''
        dot = 0
        while self.char is not None and (self.char in DIGITS or self.char == '.'):
            if dot == 1 and self.char == '.':
                dot +=1
                break
            elif self.char == '.':
                dot += 1
                num += self.char
            else:
                num += self.char
            self.advance()
        if dot == 2:
            self.error('too_many_dots')
            return -1
        elif dot == 1:
            return Token(DECIMALE_TOKEN, float(num))
        else:
            return Token(INTERO_TOKEN, int(num))

    def str_const(self):
        str_const = ''
        self.advance()
        while self.char is not None and self.char != '"':
            str_const += self.char
            self.advance()
        #str_const = bytes(str_const, "utf-8").decode("unicode_escape")
        if self.char is None:
            self.error('"_expected')
            return -1
        else:
            return Token(STRINGA_TOKEN, str_const)

    def comment(self):
        while self.char is not None and self.char != '\n':
            self.advance()

    def error(self, error_type):
        print(f'{RED_STRING}ERRORE DI SINTASSI:')
        if error_type == '"_expected"':
            print(f'Riga {self.xy[1]}, colonna {self.xy[0]} --> Chiudere le virgolette \'"\'')
        elif error_type == 'unknown_char':
            print(f'Riga {self.xy[1]}, colonna {self.xy[0]} --> Carattere \'{self.char}\' non valido!')
        elif error_type == '=_expected':
            print(f'Riga {self.xy[1]}, colonna {self.xy[0]} --> Aggiungere un \'=\'')
        elif error_type == 'too_many_dots':
            print(f'Riga {self.xy[1]}, colonna {self.xy[0]} --> Togliere un \'.\'')

def run(text):
    lexer = Lexer(text)
    return lexer.lex()
