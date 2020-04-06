import sys
from typing import Generator, Tuple
import re

#  """\n$1\n""" - replacement text bos where $1 represents the captured value

# sample comment

"""
 sample comment
"""


class Lexer:
    # class variables
    INTLIT = 0  # codes for the "kind" of value
    FLOATLIT = 1
    STRINGLIT = 2
    ID = 3
    KEYWORD = 4
    OR = 5
    AND = 6
    EQ = 7
    NEQ = 8
    LT = 9
    LTE = 10
    GT = 11
    GTE = 12
    ASSIGN = 13
    PLUS = 14
    MINUS = 15
    MULT = 16
    DIV = 17
    MOD = 18
    FACT = 19
    SEMI = 20
    COMMA = 21
    LBRACE = 22
    RBRACE = 23
    LPAREN = 24
    RPAREN = 25

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

        # backslash plague - eliminated because of python raw strings
        split_patt = re.compile(r"(\+)|\s|(\()|(\))")  # parentheses around a pattern
        # captures the value

        # a more readable way to write the split
        # pattern above using the VERBOSE option
        split_patt = re.compile(
            r"""             # Split on 
               (\+) |        #  plus and capture
               (-) |         #  minus and capture, minus not special unless in []
               \s   |        #  whitespace
               (\() |        #  left paren and capture
               (\))          #  right paren and capture
            """,
            re.VERBOSE
        )

        for line in self.f:
            tokens = (t for t in split_patt.split(line) if t)
            for t in tokens:
                if t == '+':  # TODO replace with a dictionary
                    yield (Lexer.PLUS, t)
                elif t == '(':
                    yield (Lexer.LPAREN, t)
                elif t == ')':
                    yield (Lexer.RPAREN, t)
                else:
                    yield (Lexer.ID, t)


if __name__ == "__main__":

    lex = Lexer("test.sluc")

    g = lex.token_generator()

    while True:
        try:
            print(next(g))
        except StopIteration:
            print("Done")
            break