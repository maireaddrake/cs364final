from lexer import Lexer
from ast import *


class Parser:

    def __init__(self, fn: str):

        self.lex = Lexer(fn)
        self.tg = self.lex.token_generator()
        self.variableDict = {}
        self.functionDict = {}

    # top level function that will be called
    def program(self):
        """
        Program -> {FunctionDef}            (while loop)
        """
        funcs = []
        while True:
            try:
                self.currtok = next(self.tg)
                temp = self.functiondef()
                funcs.append(temp)
            except StopIteration:
                print("Done")
                break
        return Program(funcs)

    def functiondef(self) -> FunctionDef:
        """
        FunctionDef → Type id ( Params ) { Declarations Statements }
        """
        t = self.currtok[1]
        self.currtok = next(self.tg)
        id = self.currtok[1]
        self.currtok = next(self.tg)
        if id in self.functionDict:
            raise SLUCSyntaxError("Function Already Declared")
        else:
            self.functionDict[id] = (t, None)
            if self.currtok[0] == Lexer.LPAREN:
                self.currtok = next(self.tg)
                params = self.params()
                if self.currtok[0] == Lexer.RPAREN:
                    self.currtok = next(self.tg)
                else:
                    raise SLUCSyntaxError("Missing right paren on line {0}".format(self.currtok[2]))
                if self.currtok[0] == Lexer.LBRACE:
                    self.currtok = next(self.tg)
                    decls = self.declarations()
                    stmts = self.statements()
                    if self.currtok[0] == Lexer.RBRACE:
                        temp = FunctionDef(Type(t), IDExpr(id), params, decls, stmts)
                        return temp
                    else:
                        raise SLUCSyntaxError("Missing Right Brace on line {0}".format(self.currtok[2]))
        raise SLUCSyntaxError("Error")

    def params(self) -> Params:
        """
        Params → Type id { , Type id } | ε
        """
        params = []
        if self.currtok[0] == Lexer.RPAREN:
            return Params(params)
        else:
            t = self.currtok[1]
            self.currtok = next(self.tg)
            id = self.currtok[1]
            self.currtok = next(self.tg)
            self.variableDict[id] = t
            params.append((t, id))
            while self.currtok[0] == Lexer.COMMA:
                self.currtok = next(self.tg)
                t = self.currtok[1]
                self.currtok = next(self.tg)
                id = self.currtok[1]
                self.currtok = next(self.tg)
                self.variableDict[id] = (t, None)
                params.append((t, id))
            return Params(params)

    def declarations(self):
        """
        Declarations → { Declaration }
        """
        decls = []
        while self.currtok[1] in {"int", "bool", "float"}:
            temp = self.declaration()
            self.currtok = next(self.tg)
            decls.append(temp)
        return decls

    def declaration(self):
        """
        Declaration → Type Identifier ;
        """
        t = self.currtok[1]
        self.currtok = next(self.tg)
        id = self.currtok[1]
        self.currtok = next(self.tg)
        self.variableDict[id] = (t, None)
        if self.currtok[0] == Lexer.SEMI:
            temp = Declaration(t, id)
            id = self.currtok[1]
            return temp
        else:
            raise SLUCSyntaxError("Error: Missing Semi-colon on line {0}".format(self.currtok[2]))

    def statements(self) -> [Stmt]:
        stmts = []
        while True:
            temp = self.statement()
            if temp is not None:
                stmts.append(temp)
            else:
                break
        return stmts

    def statement(self):
        """
        Statement → ; | Block | Assignment | IfStatement | WhileStatement | PrintStmt | ReturnStmt
        """
        if self.currtok[0] == Lexer.SEMI:  # semi-colon
            temp = self.currtok[1]
            self.currtok = next(self.tg)
            return temp
        elif self.currtok[0] == Lexer.KEYWORD and self.currtok[1] == "if":
            return self.ifstatement()
        elif self.currtok[0] == Lexer.KEYWORD and self.currtok[1] == "while":
            return self.whilestatement()
        elif self.currtok[0] == Lexer.KEYWORD and self.currtok[1] == "print":
            return self.printstmt()
        elif self.currtok[0] == Lexer.KEYWORD and self.currtok[1] == "return":
            return self.returnstmt()
        elif self.currtok[0] == Lexer.LBRACE:  # block
            return self.block()
        elif self.currtok[0] == Lexer.ID:  # assignment
            return self.assignment()
        else:
            return None

    def returnstmt(self):
        """
        ReturnStmt → return Expression ;
        """
        self.currtok = next(self.tg)
        temp = self.expression()
        if self.currtok[0] == Lexer.SEMI:
            self.currtok = next(self.tg)
            return ReturnStmt(temp)
        else:
            raise SLUCSyntaxError("Missing Semi-Colon on line {0}".format(self.currtok[2]))


    def block(self):
        """
        Block → { Statements }
        """
        self.currtok = next(self.tg)
        block = []
        while self.currtok[0] != Lexer.RBRACE:
            temp = self.statements()
            if temp is not None:
                block.append(temp)
            else:
                break
        if self.currtok[0] == Lexer.RBRACE:
            self.currtok = next(self.tg)
            return Block(block)
        else:
            raise SLUCSyntaxError("Missing Right Brace on line {0}".format(self.currtok[2]))


    def assignment(self):
        """
        Asssignment → ID = Expression ;
        """
        id = self.currtok[1]
        if id in self.variableDict.keys():
            self.currtok = next(self.tg)
            if self.currtok[0] == Lexer.ASSIGN:
                self.currtok = next(self.tg)
                exp = self.expression()
                if self.currtok[0] == Lexer.SEMI:
                    temp = self.variableDict[id][0]
                    self.variableDict[id] = (temp, exp)
                    self.currtok = next(self.tg)
                    return Assignment(IDExpr(id), exp)
                else:
                    raise SLUCSyntaxError("Missing Semi-colon on line {0}".format(self.currtok[2]))
        else:
            raise SLUCSyntaxError("Assignment of an undeclared variable on line {0}".format(self.currtok[2]))

    def ifstatement(self):
        """
        IfStatement → if ( Expression ) Statement [ else Statement ]
        """
        stmtList = []
        if self.currtok[0] == Lexer.KEYWORD and self.currtok[1] == "if":
            self.currtok = next(self.tg)
            if self.currtok[0] == Lexer.LPAREN:
                self.currtok = next(self.tg)
                ifCond = self.expression()
                if self.currtok[0] == Lexer.RPAREN:
                    self.currtok = next(self.tg)
                    firstStmt = self.statement()
                    while self.currtok[0] == Lexer.KEYWORD and self.currtok[1] == "else":
                        self.currtok = next(self.tg)
                        elseStmt = self.statement()
                        stmtList.append(elseStmt)
                    temp = IfStmt(ifCond, firstStmt, stmtList)
                    return temp
                else:
                    # use the line number from your token object
                    raise SLUCSyntaxError("Missing right paren on line {0}".format(self.currtok[2]))


    def whilestatement(self):
        """
        WhileStatement → while ( Expression ) Statement
        """

        if self.currtok[0] == Lexer.KEYWORD and self.currtok[1] == "while":
            self.currtok = next(self.tg)
            if self.currtok[0] == Lexer.LPAREN:
                self.currtok = next(self.tg)
                left = self.expression()
                if self.currtok[0] == Lexer.RPAREN:
                    self.currtok = next(self.tg)
                    right = self.statement()
                    temp = WhileStmt(left, right)
                    return temp
                else:
                    # use the line number from your token object
                    raise SLUCSyntaxError("Missing right paren on line {0}".format(self.currtok[2]))

    def printstmt(self):
        """
        PrintStmt → print( PrintArg { , PrintArg })
        """
        printS = []

        if self.currtok[0] == Lexer.KEYWORD and self.currtok[1] == "print":
            self.currtok = next(self.tg)
            if self.currtok[0] == Lexer.LPAREN:
                self.currtok = next(self.tg)
                firstPrint = self.printarg()
                while self.currtok[0] == Lexer.COMMA:
                    self.currtok = next(self.tg)
                    otherPrint = self.printarg()
                    printS.append(otherPrint)
                if self.currtok[0] == Lexer.RPAREN:
                    self.currtok = next(self.tg)
                    temp = PrintStmt(firstPrint, printS)
                    return temp
                else:
                    # use the line number from your token object
                    raise SLUCSyntaxError("Missing right paren on line {0}".format(self.currtok[2]))

    def printarg(self):
        """
        PrintArg → Expression | stringlit
        """
        # parse the stringlit
        if self.currtok[0] == Lexer.STRINGLIT:
            tmp = self.currtok
            self.currtok = next(self.tg)
            return LitExpr(tmp[1], str)
        # parse the Expression
        else:
            return self.expression()
        # raise SLUCSyntaxError("ERROR: Unexpected token {0} on line {1}".format(self.currtok[1], self.currtok[2]))

    def expression(self) -> Expr:
        """
        Expression -> Conjunction { || Conjunction }
        """
        left = self.conjunction()

        while self.currtok[0] == Lexer.OR:
            op = self.currtok[1]
            self.currtok = next(self.tg)  # advance to the next token because
            # we matched a plus
            right = self.conjunction()
            left = BinaryExpr(left, op, right)
        return left

    def conjunction(self) -> Expr:
        """
        Conjunction → Equality { && Equality }
        """
        left = self.equality()

        while self.currtok[0] == Lexer.AND:
            op = self.currtok[1]
            self.currtok = next(self.tg)  # advance to the next token because
            # we matched a plus
            right = self.equality()
            left = BinaryExpr(left, op, right)

        return left

    def equality(self) -> Expr:
        """
        Equality → Relation [ EquOp Relation ]
        """
        left = self.relation()

        if self.currtok[0] in {Lexer.EQ, Lexer.NEQ}:
            op = self.currtok[1]
            self.currtok = next(self.tg)
            right = self.relation()
            left = BinaryExpr(left, op, right)

        return left

    def relation(self) -> Expr:
        """
        Relation → Addition [ RelOp Addition ]
        """
        left = self.addition()

        if self.currtok[0] in {Lexer.GT, Lexer.GTE, Lexer.LT, Lexer.LTE}:
            op = self.currtok[1]
            self.currtok = next(self.tg)  # advance to the next token because
            # we matched a plus
            right = self.addition()
            left = BinaryExpr(left, op, right)

        return left

    def addition(self) -> Expr:
        """
        Expr -> Term { + Term }
        """
        left = self.term()

        while self.currtok[0] in {Lexer.PLUS, Lexer.MINUS}:
            op = self.currtok[1]
            self.currtok = next(self.tg)  # advance to the next token because
            # we matched a plus
            right = self.term()
            left = BinaryExpr(left, op, right)
        return left

    def term(self) -> Expr:
        """
        Term -> Fact { (*|/) Fact}
        """
        left = self.fact()

        while self.currtok[0] in {Lexer.MULT, Lexer.DIV, Lexer.MOD}:
            op = self.currtok[1]
            self.currtok = next(self.tg)
            right = self.fact()
            left = BinaryExpr(left, op, right)

        return left

    def fact(self) -> Expr:
        """
        Fact -> [ - ] Primary
        """

        # only advance to the next token on a successful match
        if self.currtok[0] in {Lexer.MINUS, Lexer.FACT}:
            op = self.currtok[1]
            self.currtok = next(self.tg)
            tree = self.primary()
            return UnaryOp(tree, op)

        return self.primary()

    def primary(self) -> Expr:
        """
        Primary -> ID | INTLIT | FLOATLIT | (Expr)
        """

        # parse an ID
        if self.currtok[0] == Lexer.ID:  # using ID in expression
            tmp = self.currtok
            if self.currtok[1] in self.variableDict:  # parse variable ID
                self.currtok = next(self.tg)
                return IDExpr(tmp[1])
            elif self.currtok[1] in self.functionDict:  # parse function ID
                self.currtok = next(self.tg)
                if self.currtok[0] == Lexer.LPAREN:
                    self.currtok = next(self.tg)
                    params = []
                    if self.currtok[0] == Lexer.RPAREN:
                        return FunctionExpr(tmp[1], params)
                    else:
                        params.append(self.expression())
                        while self.currtok[0] == Lexer.COMMA:
                            self.currtok = next(self.tg)
                            params.append(self.expression())
                        if self.currtok[0] == Lexer.RPAREN:
                            self.currtok = next(self.tg)
                            return FunctionExpr(tmp[1], params)
                else:
                    raise SLUCSyntaxError("Invalid Function call")
            else:
                raise SLUCSyntaxError("Undefined variable {0} on line {1}".format(tmp[1], tmp[2]))
        elif self.currtok[0] == Lexer.INTLIT:  # parse an integer literal
            tmp = self.currtok
            self.currtok = next(self.tg)
            return LitExpr(tmp[1], int)
        elif self.currtok[0] == Lexer.FLOATLIT:  # parse an float literal
            tmp = self.currtok
            self.currtok = next(self.tg)
            return LitExpr(tmp[1], float)
        elif self.currtok[0] == Lexer.STRINGLIT:  # parse an float literal
            tmp = self.currtok
            self.currtok = next(self.tg)
            return LitExpr(tmp[1], str)
        elif self.currtok[0] == Lexer.KEYWORD and self.currtok[1] in {"true", "false"}:
            tmp = self.currtok
            self.currtok = next(self.tg)
            return LitExpr(tmp[1], bool)
        elif self.currtok[0] == Lexer.LPAREN:  # parse a parenthesized expression
            self.currtok = next(self.tg)
            tree = self.expression()
            if self.currtok[0] == Lexer.RPAREN:
                self.currtok = next(self.tg)
                return tree
            else:
                # use the line number from your token object
                raise SLUCSyntaxError("Missing right paren on line {0}".format(self.currtok[2]))

        # if we get here we have a problem
        raise SLUCSyntaxError("ERROR: Unexpected token {0} on line {1}".format(self.currtok[1], self.currtok[2]))


# create our own exception by inheriting from python's exception
class SLUCSyntaxError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


if __name__ == "__main__":

    import sys

    filename = sys.argv[-1]

    p = Parser("interpretertest.c")

    t = p.program()

    t.eval()


