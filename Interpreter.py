import string
import math

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

TYPE_DIC = {'str': 'STRINGA', 'int': 'INTERO', 'float': 'DECIMALE', 'bool': 'BOOLEAN'}


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


# classe per rappresentare i Token creati dall'analizzatore lessicale
# un token tiene traccia della posizione nel file sorgente, oltre al tipo di token e all'eventuale valore
class Token:
    def __init__(self, type, xy, value=None):
        self.value = value
        self.type = type
        self.xy = xy

    # metodo di rappresentazione (debug)
    def __repr__(self):
        if self.value is None:
            # return f'{self.type},{self.xy}'
            return f'{self.type}'
        else:
            # return f'{self.type}::{self.value},{self.xy}'
            return f'{self.type}::{self.value}'


# classe rappresentate l'analizzatore lessicale
class Lexer:
    def __init__(self, text):
        self.text = text  # codice sorgente da interpretare
        self.char = None  # carattere corrente del codice sorgente
        self.pos = -1  # posizione all'interno dell'array contente il codice sorgente
        self.xy = [0, 1]  # posizione "human friendly" (x=colonna, y=riga) usata per segnalare errori
        self.advance()

    # metodo che ritorna la posizione corrente "human friendly"
    def get_xy(self):
        return [self.xy[0], self.xy[1]]

    # metodo per fare avanzare l'analizzatore lessicale
    # aggiorna posizione e carattere corrente
    def advance(self):
        self.pos += 1
        self.xy[0] += 1

        if self.pos < len(self.text):
            self.char = self.text[self.pos]
        else:
            self.char = None

    # metodo per aggiornare la posizione "human friendly" quando il codice sorgento contiene un "a capo" \n
    def newline(self):
        self.xy[0] = 0
        self.xy[1] += 1
        self.advance()

    # metodo per avviare l'analizzatore lessicale
    # ritorna l'elenco dei tokens generati, se non ci sono errori
    def lex(self):
        try:
            tokens = []  # array che conterrà l'elenco dei tokens
            while self.char is not None:
                if self.char in '\t ':  # ignora spazi e \t
                    self.advance()
                elif self.char == '\n':  # ignora \n e aggiorna la posizione "human friendly"
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
            # traceback.print_exc() # debug
            return ERROR

    # metodo per creare i token di ;:.-(),
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

    # metodo per creare i token relativi agli operatori matematici
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

    # metodo per creare i token relativi agli operatori logici
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

    # metodo per creare i token relativi alle stringhe lessicali alfanumeriche (ID, KEYWORDS, VERO, FALSO)
    def alpha_num(self):
        string = self.char
        start = self.get_xy()
        self.advance()
        while self.char is not None and self.char in ALPHANUM:
            string += self.char
            self.advance()
        if string.upper() in KEYWORDS:
            if string.upper() == 'VERO':
                return Token(string.upper(), start, True)
            elif string.upper() == 'FALSO':
                return Token(string.upper(), start, False)
            else:
                return Token(string.upper(), start)
        else:
            return Token(ID_TOKEN, start, string)

    # metodo per creare i token relativi alle stringhe lessicali intconst o realconst
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

    # metodo per creare i token relativi alle stringhe lessicali strconst
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

    # metodo per ignorare i commenti nel codice sorgente
    def comment(self):
        while self.char is not None and self.char != '\n':
            self.advance()

    # metodo per la gestione e la rappresentazione degli errori sintattici individuabili dall'analizzatore lessicale
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

# classi per la rappresentazione dei vari tipi di nodi generati dal parser
# tutti hanno il metodo di rappresentazione utilizzato per il debug

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
    def __init__(self, child):
        self.child = child

    def __repr__(self):
        return f'{self.child}'


class IncDecNode:
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child

    def __repr__(self):
        return f'({self.operator}, {self.child})'


class UnaryOperationNode:
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child

    def __repr__(self):
        return f'({self.operator}, {self.child})'


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
    def __init__(self, child):
        self.child = child

    def __repr__(self):
        return f'(scrivi({self.child}))'


class InserisciNode:
    def __init__(self, child):
        self.child = child

    def __repr__(self):
        return f'(inserisci({self.child}))'


class StopNode:
    def __init__(self, stop_tok):
        self.stop_tok = stop_tok

    def __repr__(self):
        return f'{self.stop_tok.type}'


# classe rappresentante il parser
class Parser:
    def __init__(self, tokens_list):
        self.tokens_list = tokens_list  # lista di token da comporre nell'albero sintattico
        self.token = None  # token corrente
        self.pos = -1  # posizione all'interno della lista di token
        self.advance()

    # metodo per l'avanzamento del parser
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens_list):
            self.token = self.tokens_list[self.pos]

    # metodo che dato un tipo di token controlla che il token corrente sia di quel tipo o meno
    # in caso sia vero, il parser avanza
    def match(self, token_type):
        if self.token.type == token_type:
            self.advance()
            return True
        else:
            return False

    # metodo per avviare il parser
    # ritorna l'albero sintattico
    def parse(self):
        try:
            return self.program()
        except Exception:
            return ERROR

    # metodo per l'esecuzione della produzione "program"
    # se non ci sono errori, ritorna un RootNode
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

    # metodo per l'esecuzione della produzione "decl-list"
    # se non ci sono errori, ritorna un DeclListNode
    def decl_list(self):
        child = self.decl()
        while self.token.type in ('INTERO', 'DECIMALE', 'STRINGA', 'BOOLEAN'):
            brother = self.decl_list()
            child = DeclListNode(child, brother)
        return child

    # metodo per l'esecuzione della produzione "decl"
    # se non ci sono errori, ritorna un DeclNode
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

    # metodo per l'esecuzione della produzione "id-list"
    # se non ci sono errori, ritorna un IdNode
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

    # metodo per l'esecuzione della produzione "body"
    # se non ci sono errori, ritorna un StatListNode
    def body(self):
        stat_list = self.stat_list()
        if self.match('FINE'):
            if not self.match(DOT_TOKEN):
                self.error('.')
        else:
            self.error('fine')
        return stat_list

    # metodo per l'esecuzione della produzione "stat-list"
    # se non ci sono errori, ritorna un StatNode
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

    # metodo per l'esecuzione della produzione "stat"
    # se non ci sono errori, ritorna o uno StopNode o ritorna il nodo ritornato da un metodo specifico per ogni tipo di stat
    def stat(self):
        if self.token.type == ID_TOKEN:
            if self.tokens_list[self.pos + 1].type == ASSIGN_TOKEN:
                stat = self.assign_stat()
            elif self.tokens_list[self.pos + 1].type in (DEC_TOKEN, INC_TOKEN):
                stat = self.inc_dec_stat()
            elif self.tokens_list[self.pos + 1].type in (
                    ID_TOKEN, DEC_TOKEN, 'VERO', 'FALSO', INTERO_TOKEN, STRINGA_TOKEN):
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
            stat = StopNode(self.token)
            self.advance()
        else:
            self.error('unexpected_token')
        if self.match(SEMICOLON_TOKEN):
            return stat
        else:
            self.error(';')

    # metodo per l'esecuzione della produzione "assign-stat"
    # se non ci sono errori, ritorna un AssignNode
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

    # metodo per l'esecuzione della produzione "rhs-assign-stat"
    # se non ci sono errori, ritorna un ConstNode o il nodo ritornato dal metodo math_expr
    def rhs_assign_stat(self):
        if self.token.type in ('VERO', 'FALSO', STRINGA_TOKEN):
            value = self.token
            self.advance()
            return ConstNode(value)
        else:
            return self.math_expr()

    # metodo per l'esecuzione della produzione "math-expr"
    # se non ci sono errori, ritorna un BinaryOperationNode
    def math_expr(self):
        lhs = self.math_term()

        while self.token.type in (PLUS_TOKEN, MIN_TOKEN):
            op = self.token
            self.advance()
            rhs = self.math_term()
            lhs = BinaryOperationNode(lhs, op, rhs)

        return lhs

    # metodo per l'esecuzione della produzione "math-term"
    # se non ci sono errori, ritorna un BinaryOperationNode
    def math_term(self):
        lhs = self.math_factor()

        while self.token.type in (MUL_TOKEN, DIV_TOKEN):
            op = self.token
            self.advance()
            rhs = self.math_factor()
            lhs = BinaryOperationNode(lhs, op, rhs)
        return lhs

    # metodo per l'esecuzione della produzione "math-factor"
    # se non ci sono errori, ritorna un ConstNode o il Node ritornato da radice_stat o da math_expr
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

    # metodo per l'esecuzione della produzione "radice-stat"
    # se non ci sono errori, ritorna un UnaryOperationNode
    def radice_stat(self):
        sqrt = self.token
        self.advance()
        if self.match(LEFT_PAR_TOKEN):
            expr = self.math_expr()
            if self.match(RIGHT_PAR_TOKEN):
                return UnaryOperationNode(sqrt, expr)
            else:
                self.error(')_expected')
        else:
            self.error('(_expected')

    # metodo per l'esecuzione della produzione "se-stat"
    # se non ci sono errori, ritorna un SeNode
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

    # metodo per l'esecuzione della produzione "altrimenti-stat"
    # se non ci sono errori, ritorna il node ritornato dal metodo stat_list relativo al body dell'"altrimenti"
    def altrimenti_stat(self):
        if self.match(COLON_TOKEN):
            return self.stat_list()
        else:
            self.error(':')

    # metodo per l'esecuzione della produzione "logiacl-expr"
    # se non ci sono errori, ritorna un LogicalExprNode
    def logical_expr(self):
        lhs = self.rel_expr()

        while self.token.type in ('E', 'O'):
            op = self.token
            self.advance()
            rhs = self.rel_expr()
            lhs = LogicalExprNode(lhs, op, rhs)
        return lhs

    # metodo per l'esecuzione della produzione "rel-expr"
    # se non ci sono errori, ritorna un RelExprNode
    def rel_expr(self):
        lhs = self.rel_term()

        while self.token.type in (GT_TOKEN, GTE_TOKEN, EQ_TOKEN, LT_TOKEN, LTE_TOKEN, NEQ_TOKEN):
            op = self.token
            self.advance()
            rhs = self.rel_expr()
            lhs = RelExprNode(lhs, op, rhs)
        return lhs

    # metodo per l'esecuzione della produzione "rel-term"
    # se non ci sono errori, ritorna un ConstNode
    def rel_term(self):
        token = self.token
        if token.type in (INTERO_TOKEN, DECIMALE_TOKEN, ID_TOKEN, STRINGA_TOKEN):
            self.advance()
            return ConstNode(token)
        elif self.match(LEFT_PAR_TOKEN):
            expr = self.logical_expr()
            if self.match(RIGHT_PAR_TOKEN):
                return expr
            else:
                self.error(')_expected')
        else:
            self.error('term_expected')

    # metodo per l'esecuzione della produzione "ripeti-stat"
    # se non ci sono errori, ritorna un RipetiNode
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

    # metodo per l'esecuzione della produzione "scrivi-stat"
    # se non ci sono errori, ritorna un ScriviNode
    def scrivi_stat(self):
        if self.match(LEFT_PAR_TOKEN):
            arg = self.scrivi_arg()
            if self.match(RIGHT_PAR_TOKEN):
                return ScriviNode(arg)
            else:
                self.error(')_expected')
        else:
            self.error('(_expected')

    # metodo per l'esecuzione della produzione "scrivi-arg"
    # se non ci sono errori, ritorna un ConstNode
    def scrivi_arg(self):
        token = self.token
        if token.type in (ID_TOKEN, INTERO_TOKEN, DECIMALE_TOKEN, STRINGA_TOKEN):
            self.advance()
            return ConstNode(token)
        else:
            self.error('arg_expected')

    # metodo per l'esecuzione della produzione "inserisci-stat"
    # se non ci sono errori, ritorna un InserisciNode
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

    # metodo per l'esecuzione della produzione "inc-dec-stat"
    # se non ci sono errori, ritorna un IncDecNode
    def inc_dec_stat(self):
        id = self.token
        self.advance()
        op = self.token
        self.advance()
        return IncDecNode(op, ConstNode(id))

    # metodo per la gestione e la rappresentazione degli errori sintattici
    def error(self, error_type):
        print(f'{RED_STRING}ERRORE DI SINTASSI:')
        if error_type == ')_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Chiudere la parentesi \')\'')
        elif error_type == '(_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Aprire la parentesi \'(\'')
        elif error_type == 'id_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire un nome di variabile')
        elif error_type == 'expr_expected':
            print(
                f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire o un numero o un valore booleano o una variabile o un espressione matematica')
        elif error_type == 'no_body':
            print(
                f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Manca il corpo del programma \'INIZIO...FINE\'')
        elif error_type == 'factor_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire o un numero o una variabile')
        elif error_type == 'term_expected':
            print(
                f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire o un numero o una stringa o una variabile o un espressione booleana')
        elif error_type == 'int_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire un numero intero')
        elif error_type == 'arg_expected':
            print(
                f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire una stringa o un numero o una variabile')
        elif error_type in (';', 'fine', '=', '.', ':', 'vero', 'volte', 'inizio'):
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> \'{error_type}\' mancante')
        elif error_type == '++_--_expected':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> Inserire o \'++\' o \'--\'')
        elif error_type == 'unexpected_token':
            print(f'Riga {self.token.xy[1]}, colonna {self.token.xy[0]} --> \'{self.token.type}\' non valido')
        raise Exception

    # metodo per la rappresentazione di warning (corpo del programma/se/ripeti vuoiti)
    def warning(self, warning_type):
        print(f'{YELLOW_STRING}ATTENZIONE:')
        if warning_type == 'empty_body':
            print(' --> Corpo del programma vuoto, non farà nulla!')
        elif warning_type == 'se_empty_body':
            print(' --> Corpo del costrutto \'se\' vuoto, non farà nulla!')
        elif warning_type == 'ripeti_empty_body':
            print(' --> Corpo del costrutto \'ripeti\' vuoto, non farà nulla!')
        raise Exception


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################

# classe rappresentante della symbol table
class SymbolTable:
    def __init__(self):
        self.table = {}  # la symbol table, è un "dictionary"

    # metodo per popolare la symbol table, quando le variabili vengono dichiarate
    # salva nome della variabile e tipo se la variabile non è già stata dichiarate e ritorna True
    # se invece la variabile è già stata dichiarata ritorna Falso
    def decl_operation(self, type, name):
        if name.value not in self.table:
            self.table[name.value] = [type.type, None]
            # print(self.table) # debug
            return True
        else:
            return False

    # metodo per assegnare ad una variabile il suo valore
    # ritorna True se la variabile era stata dichiarata, altrimenti False
    def assign_operation(self, name, val):
        type_ = self.table[name.value][0]
        res = True
        if not isinstance(val, bool):
            if type_ == 'INTERO':
                if isinstance(val, (int, float)):
                    self.table[name.value][1] = int(val)
                else:
                    res = False
            elif type_ == 'DECIMALE':
                if isinstance(val, (int, float)):
                    self.table[name.value][1] = float(val)
                else:
                    res = False
            elif type_ == 'STRINGA':
                if isinstance(val, str):
                    self.table[name.value][1] = val
                else:
                    res = False
            else:
                res = False
        else:
            if type_ == 'BOOLEAN':
                self.table[name.value][1] = val
            else:
                res = False

        # print(self.table)
        return res

    # metodo per controllare se una variabile è presente nella symbol table
    def check(self, id):
        if id.value in self.table:
            return True
        else:
            return False

    # metodo per ottenere il valore di una variabile
    def get_value(self, id):
        return self.table[id.value][1]


# classe rappresentante l'interprete
class Interpreter:
    def __init__(self, tree):
        self.tree = tree  # albero sintattico
        self.pos = []  # tiene traccia della posizione del token corrente quando si verifica un errore
        self.symbol_table = SymbolTable()  # tiene un riferimento alla symbol table
        self.in_loop = -1  # variabile per tenere traccia dei cicli (anche di quelli innestati)

    # metodo generico per svolgere le operazioni relative ad un nodo
    # sfrutta la programmazione ad oggetti
    def do_node(self, node):
        method = getattr(self, f'do_{type(node).__name__}')
        res = method(node)
        if res is not None:
            return res

    # metodo per far partire l'interprete
    def interpret(self):
        try:
            self.do_node(self.tree)
        except:
            # traceback.print_exc() # Debugging
            return ERROR

    # metodi con le operazioni svolte per ogni tipo di nodo, vengono chiamati attraverso il metodo do_node

    def do_RootNode(self, node):
        if node.left_child is not None:
            self.do_node(node.left_child)  # DeclListNode
        self.do_node(node.right_child)  # StatNode

    def do_DeclListNode(self, node):
        self.do_node(node.child)  # DeclNode
        if node.brother is not None:
            self.do_node(node.brother)  # DeclNode

    def do_DeclNode(self, node):
        self.do_IdNode(node.child, node.type)

    def do_IdNode(self, node, type):
        child = node.child
        if not self.symbol_table.decl_operation(type, child):  # aggiunge l'ID alla symbol table
            self.pos = child.xy
            self.error('id_already_symbol_table', child.value)
        if node.brother is not None:
            self.do_IdNode(node.brother, type)

    def do_StatNode(self, node):
        self.do_node(node.child)  # AssignNode, seNode...
        if node.brother is not None:
            self.do_StatNode(node.brother)

    def do_AssignNode(self, node):
        if self.symbol_table.check(node.left_child):
            rhs = self.do_node(node.right_child)  # ConstNode, BinaryOperationNode, UnaryOperationNode
            if not self.symbol_table.assign_operation(node.left_child, rhs):
                self.pos = node.left_child.xy
                self.error('type_mismatch', node.left_child.value, type(rhs).__name__)

        else:
            self.pos = node.left_child.xy
            self.error('id_not_decl', node.left_child.value)

    def do_BinaryOperationNode(self, node):
        op = node.operator
        lhs = self.do_node(node.left_child)  # BinaryOperationNode, ConstNode, UnaryOperationNode
        rhs = self.do_node(node.right_child)  # BinaryOperationNode, ConstNode, UnaryOperationNode

        if type(rhs).__name__ in ('int', 'float'):
            if type(lhs).__name__ in ('int', 'float'):
                if op.type == PLUS_TOKEN:
                    return lhs + rhs
                elif op.type == MIN_TOKEN:
                    return lhs - rhs
                elif op.type == MUL_TOKEN:
                    return lhs * rhs
                elif op.type == DIV_TOKEN:
                    if rhs != 0:
                        return lhs / rhs
                    else:
                        self.pos = node.operator.xy
                        self.error('div_0')
            else:
                self.pos = node.operator.xy
                self.error('not_num_expr')
        else:
            self.pos = node.operator.xy
            self.error('not_num_expr')

    def do_UnaryOperationNode(self, node):
        if node.operator.type == MIN_TOKEN:
            return self.do_node(node.child) * (-1)  # BinaryOperationNode, ConstNode, UnaryOperationNode
        elif node.operator.type == 'RADICE':
            arg = self.do_node(node.child)

            if type(arg).__name__ in ('int', 'float'):
                if arg >= 0:
                    return math.sqrt(arg)
                else:
                    self.pos = node.operator.xy
                    self.error('sqrt_arg')
            else:
                self.pos = node.operator.xy
                self.error('sqrt_arg_not_num')
        else:
            return self.do_node(node.child)

    def do_IncDecNode(self, node):
        if node.operator.type == INC_TOKEN:
            id_val = self.do_node(node.child)
            # print(type(id_val))
            if isinstance(id_val, (bool, str)):
                self.pos = node.child.child.xy
                self.error('id_not_num', node.child.child.value)
            else:
                id_val += 1
        else:
            id_val = self.do_node(node.child)
            if isinstance(id_val, (bool, str)):
                self.pos = node.child.child.xy
                self.error('id_not_num', node.child.child.value)
            else:
                id_val -= 1

        self.symbol_table.assign_operation(node.child.child, id_val)

    def do_ConstNode(self, node):
        if node.child.type == ID_TOKEN:
            if self.symbol_table.check(node.child):
                val = self.symbol_table.get_value(node.child)
                if val is not None:
                    return val
                else:
                    self.pos = node.child.xy
                    self.error('id_none', node.child.value)
            else:
                self.pos = node.child.xy
                self.error('id_not_decl', node.child.value)
        else:
            return node.child.value

    def do_ScriviNode(self, node):
        arg_to_print = str(self.do_node(node.child))
        if arg_to_print == 'False':
            print('FALSO')
        elif arg_to_print == 'True':
            print('VERO')
        else:
            # arg_to_print = bytes(arg_to_print, "utf-8").decode("unicode_escape")
            arg_to_print = arg_to_print.replace('\\n',
                                                '\n')  # necessario, altrimenti verrebbe stampato \n e non andrebbe a capo
            arg_to_print = arg_to_print.replace('\\t', '\t')
            print(arg_to_print)

    def do_InserisciNode(self, node):
        input_val = my_input()
        if self.symbol_table.check(node.child):
            if not self.symbol_table.assign_operation(node.child, input_val):
                self.pos = node.child.xy
                self.error('type_mismatch_inserisci', node.child.value, type(input_val).__name__)
        else:
            self.pos = node.child.xy
            self.error('id_not_decl', node.child.value)

    def do_RipetiNode(self, node):
        try:
            self.in_loop += 1
            for i in range(node.num_token.value):
                self.do_node(node.child)
        except:
            pass
        self.in_loop -= 1

    def do_SeNode(self, node):
        cond = self.do_node(node.logical_expr)
        if cond:
            self.do_node(node.stat_node)

        if node.altrimenti_stat_node is not None:
            if not cond:
                self.do_node(node.altrimenti_stat_node)

    def do_LogicalExprNode(self, node):
        lhs = self.do_node(node.left_child)
        rhs = self.do_node(node.right_child)
        if node.operator.type == 'E':
            return lhs and rhs
        else:
            return lhs or rhs

    def do_RelExprNode(self, node):
        lhs = self.do_node(node.left_child)
        rhs = self.do_node(node.right_child)

        if node.operator.type == EQ_TOKEN:
            return lhs == rhs
        elif node.operator.type == NEQ_TOKEN:
            return lhs != rhs

        elif isinstance(lhs, str) and not isinstance(rhs, str):
            lhs = len(lhs)
        elif not isinstance(lhs, str) and isinstance(rhs, str):
            rhs = len(rhs)
        elif isinstance(lhs, str) and isinstance(rhs, str):
            lhs = len(lhs)
            rhs = len(rhs)

        if node.operator.type == GTE_TOKEN:
            return lhs >= rhs
        elif node.operator.type == GT_TOKEN:
            return lhs > rhs
        elif node.operator.type == LTE_TOKEN:
            return lhs <= rhs
        elif node.operator.type == LT_TOKEN:
            return lhs < rhs

    def do_StopNode(self, node):
        if self.in_loop >= 0:
            raise Exception
        else:
            self.pos = node.stop_tok.xy
            self.error('stop_not_in_loop')

    # metodo per la gestione degli errori run time
    def error(self, error_type, var_name=None, var_type=None):

        print(f'\n{RED_STRING}ERRORE DURANTE L\'ESECUZIONE DEL PROGRAMMA:')
        if error_type == 'div_0':
            print(f'Alla riga {self.pos[1]} --> Non si può dividere per \'0\'')
        elif error_type == 'id_already_symbol_table':
            print(f'Alla riga {self.pos[1]} --> Nome di variabile \'{var_name}\' già utilizzato')
        elif error_type == 'id_not_decl':
            print(f'Alla riga {self.pos[1]} --> Variabile \'{var_name}\' non dichiarata')
        elif error_type == 'type_mismatch':
            print(f'Alla riga {self.pos[1]} --> Il tipo della variabile \'{var_name}\' non è \'{TYPE_DIC[var_type]}\'')
        elif error_type == 'type_mismatch_inserisci':
            print(
                f'Alla riga {self.pos[1]} --> Il tipo della variabile \'{var_name}\' non è \'{TYPE_DIC[var_type]}\' come il valore che hai inserito')
        elif error_type == 'sqrt_arg':
            print(f'Alla riga {self.pos[1]} --> L\'argomento della \'radice\' deve essere positivo')
        elif error_type == 'id_not_num':
            print(f'Alla riga {self.pos[1]} --> La variabile \'{var_name}\' non è un numero')
        elif error_type == 'not_num_expr':
            print(f'Alla riga {self.pos[1]} --> L\'espressione contiene valori non numerici')
        elif error_type == 'sqrt_arg_not_num':
            print(f'Alla riga {self.pos[1]} --> L\'argomento della radice non è un numero')
        elif error_type == 'id_none':
            print(f'Alla riga {self.pos[1]} --> Alla variabile \'{var_name}\' non è stato assegnato alcun valore')
        elif error_type == 'stop_not_in_loop':
            print(
                f'Alla riga {self.pos[1]} --> \'stop\' può essere utilizzato soltanto all\'interno dei cicli \'ripeti\'')
        raise Exception


# metodo per trasformare una stringa data in input nel corretto tipo
def my_input():
    val = input()
    if val.upper() == 'VERO':
        return True
    elif val.upper() == 'FALSO':
        return False
    else:
        try:
            return int(val)
        except:
            try:
                return float(val)
            except:
                return val


# metodo che riceve in input il codice sorgente e avvia lexer, parser e interprete
def run(text):
    lexer = Lexer(text)
    tokens = lexer.lex()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter(tree)
    interpreter.interpret()
