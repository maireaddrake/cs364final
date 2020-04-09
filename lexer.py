import sys
from typing import Generator, Tuple
import re

#  """\n$1\n""" - replacement text bos where $1 represents the captured value

"""
current problem: 
    number like 1.23__e-1_1_ can not be ID (because it starts with a digit)
    can not recognize a comment properly
    numbers in token part instead of token names
"""


class Lexer:
    # class variables
    INTLIT = "Integer"  # codes for the "kind" of value
    FLOATLIT = "Real number"
    STRINGLIT = "String"
    ID = "identifier"
    KEYWORD = "Keyword"
    OR = "or"
    AND = "and"
    EQ = "equal-equal"
    NEQ = "not equal"
    LT = "less than"
    LTE = "less than or equal"
    GT = "greater than"
    GTE = "greater than or equal"
    ASSIGN = "assignment"
    PLUS = "plus"
    MINUS = "minus"
    MULT = "multiply"
    DIV = "divide"
    MOD = "mod"
    FACT = "factorial"
    SEMI = "semicolon"
    COMMA = "comma"
    LBRACE = "Left brace"
    RBRACE = "Right brace"
    LPAREN = "Left paren"
    RPAREN = "Right paren"


    # fn - file name we are lexing
    def __init__(self, fn: str):

        try:
            self.f = open(fn)
        except IOError:
            print("File {} not found".format(fn))
            print("Exiting")
            sys.exit(1)  # can't go on

    def token_generator(self) -> Generator[Tuple[int, str], None, None]:
        """
        Returns the tokens of the language
        """

        split_patt = re.compile(
            r"""            # Split on
                (\+) |      # plus and capture (minus is not special unless in [])
                (-) |      # minus and capture
                (\*) |      # multiply and capture
                (/) |      # divide and capture
                \s   |      # whitespace
                (\{) |      # left brace and capture
                (\}) |      # right brace and capture
                (\() |      # left paren and capture
                (\))        # right paren and capture
            """,
            re.VERBOSE
        )

        tokenDict = {
            "([0-9][_0-9]*[0-9]$|[0-9]$)": Lexer.INTLIT,
            '^[1-9][_0-9]*(\.)?(_)*[_0-9]*[e|_0-9](-|\+)?[_0-9]*[0-9]$': Lexer.FLOATLIT,
            '^[_a-zA-Z][_a-zA-Z0-9]*': Lexer.ID,
            '^\"|\'.+\"|\'': Lexer.STRINGLIT
            '\|\|': Lexer.OR,
            '&&': Lexer.AND,
            '==': Lexer.EQ,
            '\!\=': Lexer.NEQ,
            '\<': Lexer.LT,
            '\<=': Lexer.LTE,
            '\>': Lexer.GT,
            '\>\=': Lexer.GTE,
            '=': Lexer.ASSIGN,
            '\+': Lexer.PLUS,
            '-': Lexer.MINUS,
            '\*': Lexer.MULT,
            '/': Lexer.DIV,
            '%': Lexer.MOD,
            '!': Lexer.FACT,
            ';': Lexer.SEMI,
            '\,': Lexer.COMMA,
            '\{': Lexer.LBRACE,
            '\}': Lexer.RBRACE,
            '\(': Lexer.LPAREN,
            '\)': Lexer.RPAREN
        }

        line_num = 0
        for line in self.f:
            line_num += 1
            tokens = (t for t in split_patt.split(line) if t)
            for t in tokens:
                matched = 0
                for i in tokenDict.keys():
                    if re.match(i, t):
                        yield (tokenDict[i], t, line_num)
                        matched = 1
                        break
                # if matched == 0:
                #     yield (Lexer.ID, t, line_num)  #

if __name__ == "__main__":

    lex = Lexer("lexertest.c")

    g = lex.token_generator()

    print('{:<20}{:<30}{:<12}'.format("Token", "Name", "Line Number"))
    print("-"*70)

    while True:
        try:
            temp = next(g)
            print('{:<20}{:<30}{:<12}'.format(temp[0], temp[1], temp[2]))
        except StopIteration:
            print("Done")
            break