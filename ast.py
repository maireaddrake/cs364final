"""
SLU-C Abstract Syntax Trees

An abstract syntax tree (AST) is a data structure that represents the
concrete (text)
"""
from typing import Sequence, List, Union, Optional


# use a class hierarchy to represent types
class Expr:
    pass


class Type:
    def __init__(self, t: str):
        self.t = t

    def __str__(self):
        return self.t


class Params:
    def __init__(self, prms: Sequence):
        self.prms = prms

    def __str__(self):
        if len(self.prms) > 0:
            st = "{0} {1}".format(self.prms[0][0], self.prms[0][1])
            for i in range(1, len(self.prms)):
                st = st + ", {0} {1}".format(self.prms[i][0], self.prms[i][1])
            return st
        else:
            return ""


class Declaration:
    def __init__(self, type: Type, id: Expr):
        self.type = type
        self.id = id

    def __str__(self):
        return "{0} {1};".format(str(self.type), str(self.id))


class Stmt:
    pass


class FunctionDef:
    def __init__(self, t: Type, id: Expr, params: Params, decls: [Declaration], stmts: [Stmt]):
        self.t = t
        self.id = id
        self.params = params
        self.decls = decls
        self.stmts = stmts

    def __str__(self):
        st = "{0} {1}({2}) {{".format(str(self.t), str(self.id), str(self.params))
        for d in self.decls:
            st = st + str(d)
        for s in self.stmts:
            st = st + str(s)
        st = st + "}"
        return st


class IfStmt(Stmt):
    def __init__(self, cond: Expr, truepart: Stmt, falsepart: Optional[Stmt]):
        self.cond = cond
        self.truepart = truepart
        self.falsepart = falsepart

    def __str__(self):
        return "if "


class Program:

    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs

    def __str__(self):
        return str(self.funcs[0])


class BinaryExpr(Expr):

    def __init__(self, left: Expr,  op: str, right: Expr):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), self.op, str(self.right))


class UnaryOp(Expr):
    def __init__(self, tree: Expr, op: str):
        self.tree = tree
        self.op = op

    def __str__(self):
        return"{0}{1}".format(self.op, str(self.tree))

    def eval(self) -> Union[int, float]:
        return self.tree.eval() * -1


class IDExpr(Expr):

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id

    def eval(self, env):
        # lookup the value of self.id
        # env is a dictionary
        pass

    def typeof(self, decls) -> Type:
        # lookup the value of self.id Look up where?
        return Type


class IntLitExpr(Expr):

    def __init__(self, intlit: str):
        self.intlit = int(intlit)

    def __str__(self):
        return str(self.intlit)

    def eval(self):
        return self.intlit  # base case

    def typeof(self) -> type:

        # return IntegerType
        return int


class FloatLitExpr(Expr):

    def __init__(self, floatlit: str):
        self.floatlit = floatlit

    def __str__(self):
        return str(self.floatlit)

    def eval(self):
        return self.floatlit  # base case


if __name__ == '__main__':
    """
    Represent (a + b) + (c * d)
    """
    expr = BinaryExpr(BinaryExpr(IDExpr('a'), "+", IDExpr('b')), "+",
                    BinaryExpr(IDExpr('c'), "*", IDExpr('d')))
    print(expr)
