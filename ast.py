"""
SLU-C Abstract Syntax Trees

An abstract syntax tree (AST) is a data structure that represents the
concrete (text)
"""
from typing import Sequence, Union, Optional

# use a class hierarchy to represent types


class Type:
    pass


class FunctionDef:
    def __init__(self, t, id:str, params, decls, stmts):
        # provide typehints for all of the parameters
        # Decls should be a dictionary
        # Key: id
        # Value: type
        pass

    def __str__(self):
        pass


class Expr:
    pass


class Stmt:
    pass

class IfStmt(Stmt):
    def __init__(self, cond: Expr, truepart: Stmt, falsepart: Optional[Stmt]):
        self.cond = cond
        self.truepart = truepart
        self.falsepart = falsepart

    def eval(self, env):

        if self.cond.eval():
            self.truepart.eval(env)
        elif self.falsepart is not None:
            self.falsepart.eval(env)

class WhileStmt(Stmt):
    def __init__(self, cond: Expr, inLoop: Stmt):
        self.cond = cond
        self.inLoop = inLoop

    def eval(self, env):
        while self.cond.eval():
            self.inLoop.eval(env)

class PrintStmt(Stmt):
    def __init__(self, pArg: Stmt, pArgList: Optional[Stmt]):
        self.pArg = pArg
        self.pArgList = pArgList

    def __str__(self):
        pri = "print({0}" .format(str(self.pArg))
        if len(self.pArgList) != 0:
            for i in self.pArgList:
                pri = pri + ", " + i
        pri  = pri + ")"
        return pri

class Declaration:
    pass


class Program:

    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs


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

    def typeof(self, decls) -> Type:
        # lookup the value of self.id Look up where?
        return Type


class IntLitExpr(Expr):

    def __init__(self, intlit: str):
        self.intlit = int(intlit)

    def __str__(self):
        return str(self.intlit)

    def scheme(self):
        return str(self.intlit)

    def eval(self):
        return self.intlit  # base case

    #def typeof(self) -> Type:
    # representing SLU-C types using Python types
    def typeof(self) -> type:

        # return IntegerType
        return int


class FloatLitExpr(Expr):

    def __init__(self, floatlit: str):
        self.floatlit = floatlit

    def __str__(self):
        return str(self.floatlit)

    def scheme(self):
        return str(self.floatlit)

    def eval(self):
        return self.floatlit  # base case

class StringLitExpr(Expr):

    def __init__(self, stringlit: str):
        self.stringlit = stringlit

    def __str__(self):
        return str(self.stringlit)

    def scheme(self):
        return str(self.stringlit)

    def eval(self):
        return self.stringlit


if __name__ == '__main__':
    """
    Represent (a + b) + (c * d)
    """
    expr = BinaryExpr(BinaryExpr(IDExpr('a'), "+", IDExpr('b')), "+",
                    BinaryExpr(IDExpr('c'), "*", IDExpr('d')))
    print(expr)
