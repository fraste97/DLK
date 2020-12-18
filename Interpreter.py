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
EOF_TOKEN = 'EOF'

ERROR = 'ERROR'
RED_STRING = '\033[91m'
YELLOW_STRING = '\033[93m'

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
            return f'{self.type}'
        else:
            return f'{self.type}::{self.value}'


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
        try:
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
                    tokens.append(self.rel_operator())
                    self.advance()
                elif self.char in LETTERS:
                    tokens.append(self.alpha_num())
                elif self.char in DIGITS:
                    tokens.append(self.num_const())
                elif self.char == '"':
                    tokens.append(self.str_const())
                    self.advance()
                else:
                    self.error('unknown_char')

            tokens.append(Token(EOF_TOKEN))
            return tokens
        except Exception:
            return ERROR

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
                self.error('=_expected')

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
                dot += 1
                break
            elif self.char == '.':
                dot += 1
                num += self.char
            else:
                num += self.char
            self.advance()
        if dot == 2:
            self.error('too_many_dots')
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
        # str_const = bytes(str_const, "utf-8").decode("unicode_escape")
        if self.char is None:
            self.error('"_expected')
        else:
            return Token(STRINGA_TOKEN, str_const)

    def comment(self):
        while self.char is not None and self.char != '\n':
            self.advance()

    def error(self, error_type):
        print(f'{RED_STRING}ERRORE DI SINTASSI:')
        if error_type == '"_expected':
            print(f'Riga {self.xy[1]}, colonna {self.xy[0]} --> Chiudere le virgolette \'"\'')
        elif error_type == 'unknown_char':
            print(f'Riga {self.xy[1]}, colonna {self.xy[0]} --> Carattere \'{self.char}\' non valido!')
        elif error_type == '=_expected':
            print(f'Riga {self.xy[1]}, colonna {self.xy[0]} --> Aggiungere un \'=\'')
        elif error_type == 'too_many_dots':
            print(f'Riga {self.xy[1]}, colonna {self.xy[0]} --> Togliere un \'.\'')

        raise Exception


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
class RootNode:
    def __init__(self, right_child, left_child=None):
        self.left_child = left_child
        self.right_child = right_child

    def __repr__(self):
        if self.left_child is not None:
            return f'{self.left_child}, {self.right_child}'
        else:
            return f'{self.right_child}'

class StatNode:
    def __init__(self, child, brother=None):
        self.child = child
        self.brother = brother

    def __repr__(self):
        if self.brother is not None:
            return f'({self.child}, {self.brother})'
        else:
            return f'{self.child}'

class ConstNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class UnaryOperationNode:
    def __init__(self, operator, token):
        self.operator = operator
        self.token = token

    def __repr__(self):
        return f'({self.operator}, {self.token})'


class BinaryOperationNode:
    def __init__(self, left_child, operator, right_child):
        self.left_child = left_child
        self.right_child = right_child
        self.operator = operator

    def __repr__(self):
        return f'({self.left_child}, {self.operator}, {self.right_child})'


class Parser:
    def __init__(self, tokens_list):
        self.tokens_list = tokens_list
        self.token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens_list):
            self.token = self.tokens_list[self.pos]


    def parse(self):
        try:
            return self.program()
        except Exception as e:
            print(e)
            return ERROR

    def program(self):
        #if self.toke.type in ('INTERO', 'DECIMALE', 'STRINGA', 'BOOLEAN'):
        #    self.advance()
        #    decl_list = self.decl_list()
        if self.token.type == 'INIZIO':
            self.advance()
            body = self.body()
        else:
            self.error('no_body')

        return RootNode(body)


    def body(self):
        stat_list = self.stat_list()
        if self.token.type == 'FINE':
            self.advance()
            if self.token.type == DOT_TOKEN:
                self.advance()
            else:
                self.error('._expected')
        else:
            self.error('fine_expected')
        return stat_list

    def stat_list(self):
        if self.token.type == 'FINE':
            self.warning('empty_body')
        else:
            stat_list_entered = False
            child = self.stat()
            while self.token.type != 'FINE' and self.token.type != EOF_TOKEN:
                stat_list_entered = True
                brother = self.stat()
                child = StatNode(child, brother)
            if stat_list_entered:
                return child
            else:
                return StatNode(child)

    def stat(self):
        stat = self.assign_stat()
        if self.token.type == SEMICOLON_TOKEN:
            self.advance()
            return stat
        else:
            self.error(';_expected')

    def assign_stat(self):
        if self.token.type == ID_TOKEN:
            id = self.token
            self.advance()
            if self.token.type == ASSIGN_TOKEN:
                op = self.token.type
                self.advance()
                rhs = self.rhs_assign_stat()
                if rhs is not None:
                    return BinaryOperationNode(id, op, rhs)
                else:
                    self.error('expr_expected')
            else:
                self.error('=_expected')
        else:
            self.error('id_expected')

    def rhs_assign_stat(self):
        if self.token.type in ('VERO', 'FALSO'):
            return self.bool_const()
        else:
            return self.math_expr()

    def bool_const(self):
        if self.token.type == 'VERO':
            return ConstNode(self.token)
        else:
            return ConstNode(self.token)

    def math_expr(self):
        lhs = self.math_term()

        while self.token.type in (PLUS_TOKEN, MIN_TOKEN):
            op = self.token
            self.advance()
            rhs = self.math_term()
            lhs = BinaryOperationNode(lhs, op, rhs)
        return lhs

    def math_term(self):
        lhs = self.math_factor()

        while self.token.type in (MUL_TOKEN, DIV_TOKEN):
            op = self.token
            self.advance()
            rhs = self.math_factor()
            lhs = BinaryOperationNode(lhs, op, rhs)
        return lhs

    def math_factor(self):
        token = self.token
        token_type = token.type
        if token_type == INTERO_TOKEN:
            self.advance()
            return ConstNode(token)
        elif token_type == DECIMALE_TOKEN:
            self.advance()
            return ConstNode(token)
        elif token_type == ID_TOKEN:
            self.advance()
            return ConstNode(token)
        elif token_type in (PLUS_TOKEN, MIN_TOKEN):
            self.advance()
            return UnaryOperationNode(token, self.math_factor())
        elif token_type == LEFT_PAR_TOKEN:
            self.advance()
            math_expr = self.math_expr()
            if self.token.type != RIGHT_PAR_TOKEN:
                self.error(')_expected')
            else:
                self.advance()
                return math_expr
        elif token_type == 'RADICE':
            return self.radice_stat()

    def radice_stat(self):
        sqrt = self.token.type
        self.advance()
        if self.token.type == LEFT_PAR_TOKEN:
            self.advance()
            expr = self.math_expr()
            if self.token.type == RIGHT_PAR_TOKEN:
                self.advance()
                return UnaryOperationNode(sqrt, expr)
            else:
                self.error(')_expected')
        else:
            self.error('(_expected')

    def error(self, error_type):
        print(f'{RED_STRING}ERRORE DI SINTASSI:')
        if error_type == ')_expected':
            print(f' --> Chiudere la parentesi \')\'')
        elif error_type == '(_expected':
            print(f' --> Aprire la parentesi \'(\'')
        elif error_type == ';_expected':
            print(f' --> \';\' mancante')
        elif error_type == 'id_expected':
            print(f' --> Inserire un nome di variabile')
        elif error_type == '=_expected':
            print(f' --> \'=\' mancante')
        elif error_type == 'expr_expected':
            print(f' --> Inserire o un numero o un valore booleano o un espressione matematica')
        elif error_type == 'no_body':
            print(f' --> Manca il corpo del programma \'INIZIO...FINE\'')
        elif error_type == 'fine_expected':
            print(f' --> \'fine\' mancante')
        elif error_type == '._expected':
            print(f' --> \'.\' mancante')
        raise Exception

    def warning(self, warning_type):
        print(f'{YELLOW_STRING}ATTENZIONE:')
        if warning_type == 'empty_body':
            print(' --> Corpo del programma vuoto, il programma non farà nulla!')
        raise Exception

def run(text):
    lexer = Lexer(text)
    tokens = lexer.lex()
    print(tokens)
    parser = Parser(tokens)
    tree = parser.parse()
    #print(tree)
    return tree