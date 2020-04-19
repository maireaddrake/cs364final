"""
SLU-C Abstract Syntax Trees

An abstract syntax tree (AST) is a data structure that represents the
concrete (text)
"""
from typing import Sequence, Union

# use a class hierarchy to represent types


class FunctionDef:
    def __init__(self, t, id:str, params, decls, stmts):
        # provide typehints for all of the parameters
        # Decls should be a dictionary
        # Key: id
        # Value: type
        pass

    def __str__(self):
        pass


class Declaration:
    pass


class Program:

    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs


class Expr:
    pass


class BinaryExpr(Expr):

    def __init__(self, left: Expr,  op: str, right: Expr):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "{0} {1} {2}".format(str(self.left), self.op, str(self.right))


class UnaryOp(Expr):
    def __init__(self, tree: Expr, op: str):
        self.tree = tree
        self.op = op

    def __str__(self):
        return"{0}{1}".format(self.op, str(self.tree))

    def scheme(self):
        return "({0} {1})".format(self.op, self.tree.scheme())

    def eval(self) -> Union[int, float]:
        return self.tree.eval() * -1


class IDExpr(Expr):

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id

    def scheme(self):
        return self.id

    def eval(self, env):
        # lookup the value of self.id
        # env is a dictionary
        pass


class IntLitExpr(Expr):

    def __init__(self, intlit: str):
        self.intlit = int(intlit)

    def __str__(self):
        return str(self.intlit)

    def scheme(self):
        return str(self.intlit)

    def eval(self):
        return self.intlit  # base case


class FloatLitExpr(Expr):

    def __init__(self, floatlit: str):
        self.floatlit = floatlit

    def __str__(self):
        return str(self.floatlit)

    def scheme(self):
        return str(self.floatlit)

    def eval(self):
        return self.floatlit  # base case


if __name__ == '__main__':
    """
    Represent (a + b) + (c * d)
    """
    expr = AddExpr(AddExpr(IDExpr('a'), IDExpr('b')),
                    MultExpr(IDExpr('c'), IDExpr('d')))
    print(expr)
