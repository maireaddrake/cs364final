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

    def eval(self):
        return self.prms


class Declaration:
    def __init__(self, type: Type, id: Expr):
        self.type = type
        self.id = id

    def __str__(self):
        return "{0} {1};".format(str(self.type), str(self.id))

    def eval(self):
        return self.id, self.type


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
            st = st + str(d) + " "
        for s in self.stmts:
            st = st + str(s) + " "
        st = st + "}"
        return st

    def eval(self) -> Union[int, float, bool, str]:
        # an environment maps identifiers to values
        # parameters or local variables
        # to evaluate a function you evaluate all of the statements
        # within the environment
        env = {}   # TODO Fix this
        prms = self.params.eval()
        for p in prms:
            env[p[0]] = p[1]
        for d in self.decls:
            dec = d.eval()
            env[dec[0]] = (dec[1], None)
        for s in self.stmts:
            s.eval(env)  # TODO define environment


class Assignment(Stmt):
    def __init__(self, var: Expr, exp: Expr):
        self.var = var
        self.exp = exp

    def __str__(self):
        return "{0} = {1};".format(str(self.var), str(self.exp))

    def eval(self, env):
        if self.var in env:
            env[self.var.eval(env)] = self.exp.eval(env)
        else:
            raise SLUCFunctionError("Error: Variable {0} is not defined in this environment".format(self.var))


class Block(Stmt):
    def __init__(self, stmts: [[Stmt]]):
        self.stmts = stmts

    def __str__(self):
        temp = ""
        for i in self.stmts:
            for j in i:
                temp = temp + str(j)
        return temp

    def eval(self, env):
        # TODO condition for empty list?
        for i in self.stmts:
            i.eval(env)


class IfStmt(Stmt):
    def __init__(self, cond: Expr, truepart: Stmt, falsepart: [Stmt]):
        self.cond = cond
        self.truepart = truepart
        self.falsepart = falsepart

    def __str__(self):
        if len(self.falsepart) == 0:
            return "if ( {0} ) {1}".format(str(self.cond), str(self.truepart))
        else:
            return "if ( {0} ) {1} else {2}".format(str(self.cond), str(self.truepart), str(self.falsepart))

    def eval(self, env):

        if self.cond.eval():
            self.truepart.eval(env)
        elif self.falsepart is not None:
            self.falsepart.eval(env)


class WhileStmt(Stmt):
    def __init__(self, cond: Expr, inLoop: Stmt):
        self.cond = cond
        self.inLoop = inLoop

    def __str__(self):
        return "while ({0}) {1}".format(str(self.cond), str(self.inLoop))

    def eval(self, env):
        while self.cond.eval():
            self.inLoop.eval(env)


class PrintStmt(Stmt):
    def __init__(self, pArg: Union[Expr, str], pArgList: Optional[Union[Expr, str]]):
        self.pArg = pArg
        self.pArgList = pArgList

    def __str__(self):
        pri = "print({0}" .format(str(self.pArg))
        if len(self.pArgList) != 0:
            for i in self.pArgList:
                pri = pri + ", " + str(i)
        pri  = pri + ")"
        return pri

    def eval(self, env):
        self.pArg.eval(env)
        if self.pArgList is not None:
            self.pArgList.eval(env)


class ReturnStmt(Stmt):
    def __init__(self, exp:Expr):
        self.exp = exp

    def __str__(self):
        return "return {0};" .format(str(self.exp))


class Program:

    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs

    def __str__(self):
        temp = ""
        for i in self.funcs:
            temp = temp + str(i)
        return temp

    def eval(self):
        funcEvals = []
        for i in self.funcs:
            funcEvals.append(i.eval())
        return funcEvals


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


class FunctionExpr(Expr):
    def __init__(self, id: str, params: []):
        self.id = id
        self.params = params

    def __str__(self):
        temp = "{0}(".format(str(self.id))
        if len(self.params) > 0:
            temp = temp + str(self.params[0])
            for i in range(1, len(self.params)):
                temp = temp + ", {0}".format(self.params[i])
            return temp + ")"
        else:
            return "{0}()".format(str(self.id))


class LitExpr(Expr):
    def __init__(self, lit: str, t: type):
        self.lit = lit
        self.t = t

    def __str__(self):
        if self.t == str:
            return "\"" + self.lit + "\""
        else:
            return str(self.lit)

    def eval(self):
        return self.lit  # base case

    def typeof(self) -> type:
        return self.t


class SLUCFunctionError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


if __name__ == '__main__':
    """
    Represent (a + b) + (c * d)
    """
    expr = BinaryExpr(BinaryExpr(IDExpr('a'), "+", IDExpr('b')), "+",
                    BinaryExpr(IDExpr('c'), "*", IDExpr('d')))
    print(expr)
