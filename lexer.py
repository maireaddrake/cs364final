import sys
from typing import Generator, Tuple
import re

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
    BLS = "binary left shift"
    BRS = "binary right shift"
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
    LBRACKET = "Left bracket"
    RBRACKET = "Right bracket"
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
                ((?<!(e|_))\+) |      # plus and capture (minus is not special unless in [])
                ((?<!(e|_))-) | 
                (\*)(?!(\/)) |      # multiply and capture
                (\/)(?!(\/|\*)) |      # divide and capture (if not followed by another / or *)
                (//) |      # comment indicator and capture
                (/\*) |     # multiline comment beginning
                (\*/) |     # multiline comment ending

                (\s)   |      # whitespace
                (\{) |      # left brace and capture
                (\}) |      # right brace and capture
                (\[) |      # left bracket and capture
                (\]) |      # right bracket and capture
                (\() |      # left paren and capture
                (\)) |       # right paren and capture
                (\<)(?!(\=|\<)) |   # less than and capture (if not followed by =)
                (\<\=) |
                (\>)(?!(\=|\>)) |   # greater than and capture (if not followed by =)
                (\>\=) |
                (\<\<) |    # binary left shift and capture
                (\>\>) |    # binary right shift and capture
                (,)  |
                (;)  |
                ((?<!(\\))\") |
                ((?<!(\\))\') |
                (:)
            """,
            re.VERBOSE
        )

        tokenDict = {
            "([0-9][_0-9]*[0-9]$|[0-9]$)": Lexer.INTLIT,
            '^[1-9][_0-9]*(\.)?(_)*[_0-9]*[e|_0-9](-|\+)?[_0-9]*[0-9]$': Lexer.FLOATLIT,
            'print|bool|else|false|if|true|float|int|char|while|main': Lexer.KEYWORD,
            '^[_a-zA-Z][_a-zA-Z0-9]*': Lexer.ID,
            '(^\".+\")|(^\'.+\')': Lexer.STRINGLIT,
            '\|\|': Lexer.OR,
            '&&': Lexer.AND,
            '==': Lexer.EQ,
            '\!\=': Lexer.NEQ,
            '\<=': Lexer.LTE,
            '\<(?!\=|\<)': Lexer.LT,
            '\>\=': Lexer.GTE,
            '\>(?!\=|\>)': Lexer.GT,
            '\<\<': Lexer.BLS,
            '\>\>': Lexer.BRS,
            '=': Lexer.ASSIGN,
            '\+': Lexer.PLUS,
            '-': Lexer.MINUS,
            '\*(?!\/)': Lexer.MULT,
            '\/(?!\/|\*)': Lexer.DIV,
            '%': Lexer.MOD,
            '!': Lexer.FACT,
            ';': Lexer.SEMI,
            '\,': Lexer.COMMA,
            '\{': Lexer.LBRACE,
            '\}': Lexer.RBRACE,
            '\[': Lexer.LBRACKET,
            '\]': Lexer.RBRACKET,
            '\(': Lexer.LPAREN,
            '\)': Lexer.RPAREN
        }

        line_num = 0
        in_something = 0
        for line in self.f:
            line_num += 1
            tokens = (t for t in split_patt.split(line) if t)
            for t in tokens:
                matched = 0
                # if tokens are in between quotes, they are merged and yielded as 1 string object
                if re.match('\"', t) and in_something == 0:
                    in_something = 1
                    temp = ""
                elif re.match('\'', t) and in_something == 0:
                    in_something = 2
                    temp = ""
                elif re.match(r'(?<!(\\))\"', t) and in_something == 1:
                    in_something = 0
                    yield (Lexer.STRINGLIT, temp, line_num)
                elif re.match(r'(?<!(\\))\'', t) and in_something == 2:
                    in_something = 0
                    yield (Lexer.STRINGLIT, temp, line_num)
                elif (in_something == 1 or in_something == 2):
                    temp = temp + t

                # if tokens are in a multi-line comment they are ignored until the */ is found
                elif in_something == 3:
                    if re.match('\*/', t):
                        in_something = 0
                        continue
                    else:
                        continue
                else:
                    # ignore empty spaces if not in a string
                    if re.match('\s', t):
                        continue
                    # go through all tokens regexes to find a match
                    for i in tokenDict.keys():
                        if re.match(i, t):
                            yield (tokenDict[i], t, line_num)
                            matched = 1
                            break
                    if matched == 0:
                        if re.match('//', t):
                            break
                        elif re.match('/\*', t):
                            in_something = 3
                        else:
                            yield ("ILLEGAL", t, line_num)
            if in_something == 1 or in_something == 2:
                in_something = 0
                yield ("ILLEGAL", "[MISSING \"]", line_num)


# create our own exception by inheriting from python's exception
class SLUCLexicalError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


if __name__ == "__main__":

    import sys

    filename = sys.argv[-1]

    lex = Lexer(filename)

    g = lex.token_generator()

    print('{:<30}{:<65}{:<12}'.format("Token", "Name", "Line Number"))
    print("-" * 70)

    while True:
        try:
            temp = next(g)
            print('{:<30}{:<65}{:<12}'.format(temp[0], temp[1], temp[2]))
        except StopIteration:
            print("Done")
            break