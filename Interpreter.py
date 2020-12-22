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
            'SE', 'VERO', 'FAI', 'FALSO', 'RIPETI', 'VOLTE', 'SCRIVI', 'INSERISCI', 'E', 'O', 'ALTRIMENTI']


class Token:
    def __init__(self, type, xy, value=None):
        self.value = value
        self.type = type
        self.xy = xy

    def __repr__(self):
        if self.value is None:
            # return f'{self.type},{self.xy}'
            return f'{self.type}'
        else:
            # return f'{self.type}::{self.value},{self.xy}'
            return f'{self.type}::{self.value}'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.char = None
        self.pos = -1
        self.xy = [0, 1]
        self.advance()

    def get_xy(self):
        return [self.xy[0], self.xy[1]]

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

            tokens.append(Token(EOF_TOKEN, self.get_xy()))
            return tokens
        except Exception as e:
            #traceback.print_exc()
            return ERROR

    def sugar(self):
        if self.char == ';':
            return Token(SEMICOLON_TOKEN, self.get_xy())
        elif self.char == ':':
            return Token(COLON_TOKEN, self.get_xy())
        elif self.char == '.':
            return Token(DOT_TOKEN, self.get_xy())
        elif self.char == '(':
            return Token(LEFT_PAR_TOKEN, self.get_xy())
        elif self.char == ')':
            return Token(RIGHT_PAR_TOKEN, self.get_xy())
        elif self.char == ',':
            return Token(COMMA_TOKEN, self.get_xy())

    def operator(self):
        start = self.get_xy()
        if self.char == '+':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '+':
                self.advance()
                return Token(INC_TOKEN, start)
            else:
                return Token(PLUS_TOKEN, start)
        elif self.char == '-':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '-':
                self.advance()
                return Token(DEC_TOKEN, start)
            else:
                return Token(MIN_TOKEN, start)
        elif self.char == '/':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                self.comment()
            else:
                return Token(DIV_TOKEN, start)
        elif self.char == '*':
            return Token(MUL_TOKEN, start)

    def rel_operator(self):
        start = self.get_xy()
        if self.char == '<':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                return Token(LTE_TOKEN, start)
            else:
                return Token(LT_TOKEN, start)
        elif self.char == '>':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                return Token(GTE_TOKEN, start)
            else:
                return Token(GT_TOKEN, start)
        elif self.char == '=':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                return Token(EQ_TOKEN, start)
            else:
                return Token(ASSIGN_TOKEN, start)
        elif self.char == '!':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                return Token(NEQ_TOKEN, start)
            else:
                self.error('=_expected')

    def alpha_num(self):
        string = self.char
        start = self.get_xy()
        self.advance()
        while self.char is not None and self.char in ALPHANUM:
            string += self.char
            self.advance()
        if string.upper() in KEYWORDS:
            return Token(string.upper(), start)
        else:
            return Token(ID_TOKEN, start, string)

    def num_const(self):
        num = ''
        dot = 0
        start = self.get_xy()
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
            return Token(DECIMALE_TOKEN, start, float(num))
        else:
            return Token(INTERO_TOKEN, start, int(num))

    def str_const(self):
        str_const = ''
        start = self.get_xy()
        self.advance()
        while self.char is not None and self.char != '"':
            str_const += self.char
            self.advance()
        # str_const = bytes(str_const, "utf-8").decode("unicode_escape")
        if self.char is None:
            self.error('"_expected')
        else:
            return Token(STRINGA_TOKEN, start, str_const)

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
            return f'<[{self.left_child}], {self.right_child}>'
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


class IdNode:
    def __init__(self, child, brother=None):
        self.child = child
        self.brother = brother

    def __repr__(self):
        if self.brother is not None:
            return f'{self.child}, {self.brother}'
        else:
            return f'{self.child}'


class DeclListNode:
    def __init__(self, child, brother=None):
        self.child = child
        self.brother = brother

    def __repr__(self):
        if self.brother is not None:
            return f'{self.child},{self.brother}'
        else:
            return f'{self.child}'


class DeclNode:
    def __init__(self, type, child):
        self.child = child
        self.type = type

    def __repr__(self):
            return f'{self.type}({self.child})'


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


class AssignNode:
    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child

    def __repr__(self):
        return f'({self.left_child}, ASSIGN, {self.right_child})'


class RelExprNode:
    def __init__(self, left_child, operator, right_child):
        self.left_child = left_child
        self.right_child = right_child
        self.operator = operator

    def __repr__(self):
        return f'({self.left_child}, {self.operator}, {self.right_child})'


class LogicalExprNode:
    def __init__(self, left_child, operator, right_child):
        self.left_child = left_child
        self.right_child = right_child
        self.operator = operator

    def __repr__(self):
        return f'({self.left_child}, {self.operator}, {self.right_child})'


class BinaryOperationNode:
    def __init__(self, left_child, operator, right_child):
        self.left_child = left_child
        self.right_child = right_child
        self.operator = operator

    def __repr__(self):
        return f'({self.left_child}, {self.operator}, {self.right_child})'


class SeNode:
    def __init__(self, logical_expr, stat_node, altrimenti_stat_node=None):
        self.logical_expr = logical_expr
        self.stat_node = stat_node
        self.altrimenti_stat_node = altrimenti_stat_node

    def __repr__(self):
        if self.altrimenti_stat_node is not None:
            return f'(se{self.logical_expr}, {self.stat_node}, altrimenti{self.altrimenti_stat_node})'
        else:
            return f'(se{self.logical_expr}, {self.stat_node})'


class RipetiNode:
    def __init__(self, num_token, child):
        self.child = child
        self.num_token = num_token

    def __repr__(self):
        return f'(ripeti{self.child})'


class ScriviNode:
    def __init__(self, arg_token):
        self.arg_token = arg_token

    def __repr__(self):
        return f'(scrivi({self.arg_token}))'


class InserisciNode:
    def __init__(self, arg_token):
        self.arg_token = arg_token

    def __repr__(self):
        return f'(inserisci({self.arg_token}))'


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

    def match(self, token_type):
        if self.token.type == token_type:
            self.advance()
            return True
        else:
            return False

    def parse(self):
        try:
            return self.program()
        except Exception:
            return ERROR

    def program(self):
        decl_list = None
        if self.token.type in ('INTERO', 'DECIMALE', 'STRINGA', 'BOOLEAN'):
            decl_list = self.decl_list()
        if self.match('INIZIO'):
            body = self.body()
        else:
            self.error('inizio')
        if decl_list is not None:
            return RootNode(body, decl_list)
        else:
            return RootNode(body)

    def decl_list(self):
        child = self.decl()
        while self.token.type in ('INTERO', 'DECIMALE', 'STRINGA', 'BOOLEAN'):
            brother = self.decl_list()
            child = DeclListNode(child, brother)
        return child

    def decl(self):
        type = self.token
        self.advance()
        if self.match(COLON_TOKEN):
            id_list = self.id_list()
            if self.match(SEMICOLON_TOKEN):
                return DeclNode(type, id_list)
            else:
                self.error(';')
        else:
            self.error(':')

    def id_list(self):
        if self.token.type == ID_TOKEN:
            entered = False
            child = self.token
            self.advance()
            while self.token.type == COMMA_TOKEN:
                entered = True
                self.advance()
                brother = self.id_list()
                child = IdNode(child, brother)
            if entered:
                return child
            else:
                return IdNode(child)
        else:
            self.error('id_expected')

    def body(self):
        stat_list = self.stat_list()
        if self.match('FINE'):
            if not self.match(DOT_TOKEN):
                self.error('.')
        else:
            self.error('fine')
        return stat_list

    def stat_list(self):
        if self.token.type == 'FINE':
            self.warning('empty_body')
        else:
            stat_list_entered = False
            child = self.stat()

            while self.token.type != 'FINE' and self.token.type != EOF_TOKEN and self.token.type != 'ALTRIMENTI':
                stat_list_entered = True
                brother = self.stat_list()
                child = StatNode(child, brother)
            if stat_list_entered:
                return child
            else:
                return StatNode(child)

    def stat(self):
        if self.token.type == ID_TOKEN:
            if self.tokens_list[self.pos + 1].type == ASSIGN_TOKEN:
                stat = self.assign_stat()
            elif self.tokens_list[self.pos + 1].type in (DEC_TOKEN, INC_TOKEN):
                stat = self.inc_dec_stat()
            elif self.tokens_list[self.pos + 1].type in (ID_TOKEN, DEC_TOKEN, 'VERO', 'FALSO', INTERO_TOKEN, STRINGA_TOKEN):
                self.error('=')
            else:
                self.error('++_--_expected')
        elif self.match('SE'):
            stat = self.se_stat()
        elif self.match('RIPETI'):
            stat = self.ripeti_stat()
        elif self.match('SCRIVI'):
            stat = self.scrivi_stat()
        elif self.match('INSERISCI'):
            stat = self.inserisci_stat()
        elif self.token.type == 'STOP':
            stat = self.token
            self.advance()
        else:
            self.error('unexpected_token')
        if self.match(SEMICOLON_TOKEN):
            return stat
        else:
            self.error(';')

    def assign_stat(self):
        if self.token.type == ID_TOKEN:
            id = self.token
            self.advance()
            if self.match(ASSIGN_TOKEN):
                rhs = self.rhs_assign_stat()
                if rhs is not None:
                    return AssignNode(id, rhs)
                else:
                    self.error('expr_expected')
            else:
                self.error('=')
        else:
            self.error('id_expected')

    def rhs_assign_stat(self):
        if self.token.type in ('VERO', 'FALSO', STRINGA_TOKEN):
            value = self.token
            self.advance()
            return ConstNode(value)
        else:
            return self.math_expr()

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
        if self.match(INTERO_TOKEN):
            return ConstNode(token)
        elif self.match(DECIMALE_TOKEN):
            return ConstNode(token)
        elif self.match(ID_TOKEN):
            return ConstNode(token)
        elif token_type in (PLUS_TOKEN, MIN_TOKEN):
            self.advance()
            value = self.math_factor()
            if value is not None:
                return UnaryOperationNode(token, value)
            else:
                self.error('factor_expected')
        elif self.match(LEFT_PAR_TOKEN):
            math_expr = self.math_expr()
            if self.match(RIGHT_PAR_TOKEN):
                return math_expr
            else:
                self.error(')_expected')
        elif token_type == 'RADICE':
            return self.radice_stat()
        else:
            self.error('factor_expected')

    def radice_stat(self):
        sqrt = self.token.type
        self.advance()
        if self.match(LEFT_PAR_TOKEN):
            expr = self.math_expr()
            if self.match(RIGHT_PAR_TOKEN):
                return UnaryOperationNode(sqrt, expr)
            else:
                self.error(')_expected')
        else:
            self.error('(_expected')

    def se_stat(self):
        if self.match(LEFT_PAR_TOKEN):
            logical_expr = self.logical_expr()

            if self.match(RIGHT_PAR_TOKEN):
                if self.match('VERO'):
                    if self.match('FAI'):
                        if self.match(COLON_TOKEN):
                            if self.token.type != 'FINE':
                                stat_list = self.stat_list()
                                if self.match('ALTRIMENTI'):
                                    altrimenti_stat = self.altrimenti_stat()
                                    if self.match('FINE'):
                                        return SeNode(logical_expr, stat_list, altrimenti_stat)
                                    else:
                                        self.error('fine')
                                elif self.match('FINE'):
                                    return SeNode(logical_expr, stat_list)
                                else:
                                    self.error('fine')
                            else:
                                self.warning('se_empty_body')
                        else:
                            self.error(':')
                    else:
                        self.error('fai')
                else:
                    self.error('vero')
            else:
                self.error(')_expected')
        else:
            self.error('(_expected')

    def altrimenti_stat(self):
        if self.match(COLON_TOKEN):
            return self.stat_list()
        else:
            self.error(':')

    def logical_expr(self):
        lhs = self.rel_expr()

        while self.token.type in ('E', 'O'):
            op = self.token
            self.advance()
            rhs = self.rel_expr()
            lhs = LogicalExprNode(lhs, op, rhs)
        return lhs

    def rel_expr(self):
        lhs = self.rel_term()

        while self.token.type in (GT_TOKEN, GTE_TOKEN, EQ_TOKEN, LT_TOKEN, LTE_TOKEN, NEQ_TOKEN):
            op = self.token
            self.advance()
            rhs = self.rel_expr()
            lhs = RelExprNode(lhs, op, rhs)
        return lhs

    def rel_term(self):
        token = self.token
        if token.type in (INTERO_TOKEN, DECIMALE_TOKEN, ID_TOKEN):
            self.advance()
            return ConstNode(token)
        elif self.match(RIGHT_PAR_TOKEN):
            expr = self.logical_expr()
            self.advance()
            return expr
        else:
            self.error('term_expected')

    def ripeti_stat(self):
        if self.token.type == INTERO_TOKEN:
            num = self.token
            self.advance()
            if self.match('VOLTE'):
                if self.match(COLON_TOKEN):
                    if self.token.type != 'FINE':
                        stat = self.stat_list()
                        if self.match('FINE'):
                            return RipetiNode(num, stat)
                        else:
                            self.error('fine')
                    else:
                        self.warning('ripeti_empty_body')
                else:
                    self.error(':')
            else:
                self.error('volte')
        else:
            self.error('int_expected')

    def scrivi_stat(self):
        if self.match(LEFT_PAR_TOKEN):
            arg = self.scrivi_arg()
            if self.match(RIGHT_PAR_TOKEN):
                return ScriviNode(arg)
            else:
                self.error(')_expected')
        else:
            self.error('(_expected')

    def scrivi_arg(self):
        token = self.token
        if token.type in (ID_TOKEN, INTERO_TOKEN, DECIMALE_TOKEN, STRINGA_TOKEN):
            self.advance()
            return ConstNode(token)
        else:
            self.error('arg_expected')

    def inserisci_stat(self):
        if self.match(LEFT_PAR_TOKEN):
            if self.token.type == ID_TOKEN:
                arg = self.token
                self.advance()
                if self.match(RIGHT_PAR_TOKEN):
                    return InserisciNode(arg)
                else:
                    self.error(')_expected')
            else:
                self.error('id_expected')
        else:
            self.error('(_expected')

    def inc_dec_stat(self):
        id = self.token
        self.advance()
        op = self.token
        self.advance()
        return UnaryOperationNode(op, id)

    def error(self, error_type):
        print(f'{RED_STRING}ERRORE DI SINTASSI:')
        if error_type == ')_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Chiudere la parentesi \')\'')
        elif error_type == '(_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Aprire la parentesi \'(\'')
        elif error_type == 'id_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire un nome di variabile')
        elif error_type == 'expr_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire o un numero o un valore booleano o una variabile o un espressione matematica')
        elif error_type == 'no_body':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Manca il corpo del programma \'INIZIO...FINE\'')
        elif error_type == 'factor_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire o un numero o una variabile')
        elif error_type == 'term_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire o un numero o una variabile o un espressione booleana')
        elif error_type == 'int_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Numero intero mancante')
        elif error_type == 'arg_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire una stringa o un numero o una variabile')
        elif error_type in (';', 'fine', '=', '.', ':', 'vero', 'volte', 'inizio'):
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> \'{error_type}\' mancante')
        elif error_type == '++_--_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire o \'++\' o \'--\'')
        elif error_type == 'unexpected_token':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> \'{self.token.type}\' non valido')
        raise Exception

    def warning(self, warning_type):
        print(f'{YELLOW_STRING}ATTENZIONE:')
        if warning_type == 'empty_body':
            print(' --> Corpo del programma vuoto, non farà nulla!')
        elif warning_type == 'se_empty_body':
            print(' --> Corpo del costrutto \'se\' vuoto, non farà nulla!')
        elif warning_type == 'ripeti_empty_body':
            print(' --> Corpo del costrutto \'ripeti\' vuoto, non farà nulla!')
        raise Exception


def run(text):
    lexer = Lexer(text)
    tokens = lexer.lex()

    print(tokens)
    parser = Parser(tokens)
    tree = parser.parse()

    return tree
