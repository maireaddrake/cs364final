from lexer import Lexer
from ast import Expr, BinaryExpr, UnaryOp, IDExpr, IntLitExpr, FloatLitExpr


class Parser:

    def __init__(self, fn: str):

        self.lex = Lexer(fn)
        self.tg = self.lex.token_generator()
        self.currtok = next(self.tg)


    # top level function that will be called
    def program(self):
        """
        Program -> {FunctionDef}            (while loop)
        """

    def conjunction(self):
        pass

    def equality(self):
        pass

    def relation(self):
        pass

    def addition(self) -> Expr:
        """
        Expr -> Term { + Term }
        """
        left = self.term()

        while self.currtok[0] in {Lexer.PLUS, Lexer.MINUS}:
            self.currtok = next(self.tg)  # advance to the next token because
            # we matched a plus
            right = self.term()
            left = BinaryExpr(left, , right)

        return left

    def term(self) -> Expr:
        """
        Term -> Fact { (*|/) Fact}
        """
        left = self.fact()

        while self.currtok[0] in {Lexer.MULT}:
            self.currtok = next(self.tg)
            right = self.fact()
            left = BinaryExpr(left, "*", right)

        return left

    def fact(self) -> Expr:
        """
        Fact -> [ - ] Primary
        """

        # only advance to the next token on a successful match
        if self.currtok[0] == Lexer.MINUS:
            self.currtok = next(self.tg)
            tree = self.primary()
            return UnaryOp(tree, )

        return self.primary()

    def primary(self) -> Expr:
        """
        Primary -> ID | INTLIT | (Expr)
        """

        # TODO Add real literals

        # parse an ID
        if self.currtok[0] == Lexer.ID:  # using ID in expression
            tmp = self.currtok
            # TODO check to make sure ID is declared (in the dictionary)
            self.currtok = next(self.tg)
            return IDExpr(tmp[1])

        # parse an integer literal
        if self.currtok[0] == Lexer.INTLIT:
            tmp = self.currtok
            self.currtok = next(self.tg)
            return IntLitExpr(tmp[1])

        if self.currtok[0] == Lexer.FLOATLIT:
            tmp = self.currtok
            self.currtok = next.(self.tg)
            return FloatLitExpr(tmp[1])

        # parse a parenthesized expression
        if self.currtok[0] == Lexer.LPAREN:
            self.currtok = next(self.tg)
            tree = self.addition()  # TODO keeps changing
            if self.currtok[0] == Lexer.RPAREN:
                self.currtok = next(self.tg)
                return tree
            else:
                # use the line number from your token object
                raise SLUCSyntaxError("Missing right paren on line {0}".format(-1))

        # if we get here we have a problem
        raise SLUCSyntaxError("ERROR: Unexpected token on line {0}".format(self.currtok[1]))


# create our own exception by inheriting from python's exception
class SLUCSyntaxError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


if __name__ == "__main__":
    p = Parser('simple.c')
    t = p.addition()
    print(t)
    print(t.scheme())
