"""
SLU-C Abstract Syntax Trees

An abstract syntax tree (AST) is a data structure that represents the
concrete (text)
"""
from typing import Sequence, List, Union, Optional, Dict
import operator

ops = {'*': operator.mul,
       '/': operator.truediv,
       '%': operator.mod,
       '+': operator.add,
       '-': operator.sub,
       '>': operator.gt,
       '>=': operator.ge,
       '<': operator.lt,
       '<=': operator.le,
       '==': operator.eq,
       '!=': operator.ne,
       '&&': operator.and_,
       '||': operator.or_
}

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
    def __init__(self, t: type, id: Expr):
        self.t = t
        self.id = id

    def __str__(self):
        return "{0} {1};".format(str(self.t), str(self.id))

    def eval(self):
        return self.id, self.t


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

    def eval(self, given: Sequence[Expr]) -> Union[int, float, bool, str]:
        env = {}
        prms = self.params.eval()
        if len(prms) != len(given):
            raise SLUCFunctionError("Error: function {0} expected {1} parameters, got {2}".format(self.id, len(prms), len(given)))
        for p in range(len(prms)):
            env[prms[p][1]] = (prms[p][0], given[p])
        for d in self.decls:
            dec = d.eval()
            env[dec[0]] = (dec[1], None)
        for s in self.stmts:
            if type(s) != str:
                st = s.eval(env)
                if type(st).__name__ == "dict":
                    env = st
                    continue
                elif st is not None:
                    return st


class Assignment(Stmt):
    def __init__(self, var: Expr, exp: Expr):
        self.var = var
        self.exp = exp

    def __str__(self):
        return "{0} = {1};".format(str(self.var), str(self.exp))

    def eval(self, env: Dict):
        if str(self.var) in env.keys():
            ex = self.exp.eval(env)
            if env[str(self.var)][0] == type(ex).__name__:
                temp = env[str(self.var)][0]
                env[str(self.var)] = (temp, ex)
                return env
            elif env[str(self.var)][0] == "int" and type(ex).__name__ == "float":
                ex = int(ex)
                temp = env[str(self.var)][0]
                env[str(self.var)] = (temp, ex)
                return env
            elif env[str(self.var)][0] == "float" and type(ex).__name__ == "int":
                ex = float(ex)
                temp = env[str(self.var)][0]
                env[str(self.var)] = (temp, ex)
                return env
            else:
                raise SLUCFunctionError("Error: Type Mismatch")
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
            for j in i:
                if type(j) != str:
                    j.eval(env)


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

        if self.cond.eval(env):
            self.truepart.eval(env)
        elif self.falsepart is not None:
            for i in self.falsepart:
                i.eval(env)


class WhileStmt(Stmt):
    def __init__(self, cond: Expr, inLoop: Stmt):
        self.cond = cond
        self.inLoop = inLoop

    def __str__(self):
        return "while ({0}) {1}".format(str(self.cond), str(self.inLoop))

    def eval(self, env):
        while self.cond.eval(env):
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
        pri = pri + ")"
        return pri

    def eval(self, env):
        args = [self.pArg.eval(env)]
        if self.pArgList is not None:
            for i in self.pArgList:
                if type(i) == str:
                    args.append(i)
                args.append(i.eval(env))
        for i in args:
            print(i)


class ReturnStmt(Stmt):
    def __init__(self, exp: Expr):
        self.exp = exp

    def __str__(self):
        return "return {0};" .format(str(self.exp))

    def eval(self, env):
        return self.exp.eval(env)


funcDict = {}

class Program:

    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs
        global funcDict

    def __str__(self):
        temp = ""
        for i in self.funcs:
            temp = temp + str(i)
        return temp

    def eval(self):
        for i in self.funcs:
            funcDict[str(i.id)] = i
            if str(i.id) == "main":
                i.eval([])
        return None


class BinaryExpr(Expr):

    def __init__(self, left: Expr,  op: str, right: Expr):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), self.op, str(self.right))

    def eval(self, env):
        l = self.left.eval(env)
        r = self.right.eval(env)
        if l is None or r is None:
            return None
        return ops[self.op](l, r)


class UnaryOp(Expr):
    def __init__(self, tree: Expr, op: str):
        self.tree = tree
        self.op = op

    def __str__(self):
        return"{0}{1}".format(self.op, str(self.tree))

    def eval(self, env) -> Union[int, float, bool]:
        return self.tree.eval(env) * -1


class IDExpr(Expr):

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id

    def eval(self, env):
        if type(env[self.id][1]) in {int, float, bool, str}:
            return env[self.id][1]
        else:
            return env[self.id][1].eval(env)

    def typeof(self, env) -> type:
        # lookup the value of self.id Look up where?
        return env[self.id][0].eval(env)


class FunctionExpr(Expr):
    def __init__(self, id: str, params: []):
        self.id = id
        self.params = params
        global funcDict

    def __str__(self):
        temp = "{0}(".format(str(self.id))
        if len(self.params) > 0:
            temp = temp + str(self.params[0])
            for i in range(1, len(self.params)):
                temp = temp + ", {0}".format(self.params[i])
            return temp + ")"
        else:
            return "{0}()".format(str(self.id))

    def eval(self, env):
        x = funcDict[self.id].eval(self.params)
        return x


class LitExpr(Expr):
    def __init__(self, lit: str, t: type):
        self.lit = lit
        self.t = t

    def __str__(self):
        if self.t == str:
            return "\"" + self.lit + "\""
        else:
            return str(self.lit)

    def eval(self, env):
        return self.t(self.lit)

    def typeof(self, env) -> type:
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
