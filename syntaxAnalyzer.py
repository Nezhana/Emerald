import lexAnalyzer

class SyntaxAnalyzer():

    def __init__(self, sym_table, rowIndex):
        self.table_of_symbols = sym_table
        self.rowInd = rowIndex

    def getSymbol(self, rowInd):
        if self.rowInd > len(self.table_of_symbols):
            self.failParse('getSymbol', 'rowInd > len of table')
        #table_of_symbols = {id : (line_num, lexeme, token, specialInd)}
        line_num, lexeme, token, _ = self.table_of_symbols[rowInd]
        return line_num, lexeme, token

    def parseToken(self, lexeme, token, specialInd):
        if self.rowInd > len(self.table_of_symbols):
            self.failParse('parseToken', 'rowInd > len of table')

        line_num, lex, tok = self.getSymbol(self.rowInd)
        self.rowInd += 1
        
        if (lex, tok) == (lexeme, token):
            print(specialInd + 'parseToken: In row {0} token {1}'.format(line_num, (lex, tok)))
            return True
        else:
            self.failParse('parseToken', f'unpredictable lexeme: {lex}')
            return False

    def parseStatementList(self):
        print('\t parseStatementList():')
        while self.parseStatement():
            pass
        return True

    def parseStatement(self):
        print('\t\t parseStatement():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        #statement : assign | input
        if tok == 'id':
            _, next_lex, next_tok = self.getSymbol(self.rowInd+1)
            if (next_lex, next_tok) == ('in', 'keywords'):
                self.parseIndExpr()
            else:
                self.parseAssign()
            return True
        elif tok == 'onelinecom':
            print('\t\t\tIn row {0} token {1}'.format(line_num, (lex, tok)))
            return True
        #statement : linecomments
        elif tok == 'startcom':
            self.parseLineComments()
            return True
        #statement : ifstate
        elif (lex, tok) == ('if', 'keywords'):
            self.parseIf()
            return True
        #statement : forstate
        elif (lex, tok) == ('for', 'keywords'):
            self.parseFor()
            return True
        #statement : output
        elif (lex, tok) == ('print', 'keywords') or (lex, tok) == ('puts', 'keywords'):
            self.parseOutput()
            return True
        #EOF - End Of File
        elif (lex, tok) == ('', 'EOF'):
            return False
        #Fail
        else:
            self.failParse('parseStatement', f'unpredictable lexeme: {lex} {tok}')
            return False

    def parseLineComments(self):
        print('\t\t\tparseLineComments():')
        self.rowInd += 1
        line_num, lex, tok = self.getSymbol(self.rowInd)
        while tok != 'endcom':
            print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
            self.rowInd += 1
            line_num, lex, tok = self.getSymbol(self.rowInd)
        else:
            if self.parseToken('=end', 'endcom', '\t\t\t\t'):
                return True
            else:
                return False

    def parseIf(self):
        print('\t\t\tparseIf():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        self.rowInd += 1
        try:
            self.parseExpression()
            if self.parseStatement():
                pass
            else:
                return False
            if self.parseToken('elif', 'keywords', '\t\t\t'):
                self.parseExpression()
                if self.parseStatement():
                    pass
                else:
                    return False
            else: pass
            if self.parseToken('else', 'keywords', '\t\t\t'):
                if self.parseStatement():
                    pass
                else:
                    return False
            else:
                pass
            if self.parseToken('end', 'keywords', '\t\t\t'):
                return True
            else:
                return False
        except:
            pass

    def parseIndExpr(self):
        print('\t\t\tparseIndExpr():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        self.rowInd += 1
        if self.parseToken('in', 'keywords', '\t\t\t\t'):
            self.parseRangeExpr()
        else:
            return False

    def parseRangeExpr(self):
        print('\t\t\t\tparseRangeExpr():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        if tok == 'intc':
            self.rowInd += 1
            if self.parseToken('..', 'rangeexpr', '\t\t\t\t'):
                line_num, lex, tok = self.getSymbol(self.rowInd)
                if tok == 'intc':
                    print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                    return True
                else:
                    return False
            elif self.parseToken('...', 'rangeexpr', '\t\t\t\t'):
                line_num, lex, tok = self.getSymbol(self.rowInd)
                if tok == 'intc':
                    print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                    return True
                else:
                    return False
            else:
                return False
        else:
            self.failParse('parseRangeExpr', 'range lexeme not intc')

    def parseFor(self):
        print('\t\t\tparseFor():')
        self.rowInd += 1
        line_num, lex, tok = self.getSymbol(self.rowInd)
        print('\t'*3 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        self.parseIndExpr()
        self.rowInd += 1
        if self.parseToken('do', 'keywords', '\t\t\t\t'):
            self.parseStatement()
            self.rowInd += 1
            line_num, lex, tok = self.getSymbol(self.rowInd)
            if (lex, tok) == ('end', 'keywords'):
                return True
            else:
                return False
        else:
            return False

    def parseAssign(self):
        print('\t\t\t parseAssign():')
        _, lex, tok = self.getSymbol(self.rowInd)
        self.rowInd += 1
        if self.parseToken('=', 'assignop', '\t\t\t\t'):
            #try parse Input
            try:
                _, lex, tok = self.getSymbol(self.rowInd)
                if (lex, tok) == ('gets', 'keywords'):
                    self.rowInd += 1
                    return True
                else:
                    raise ValueError
            except ValueError:
                self.parseExpression()
                return True
        else:
            return False

    def parseExpression(self):
        print('\t\t\t\t parseExpression():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        if tok == 'boolc':
            self.rowInd += 1
            print('\t'*5 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
            try:
                if self.getSymbol(self.rowInd)[2] == 'relop':
                    line_num, lex, tok = self.getSymbol(self.rowInd)
                    if tok in ('relop'):
                        self.rowInd += 1
                        print('\t'*5 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                    else:
                        self.failParse('parseExpression')
                    line_num, lex, tok = self.getSymbol(self.rowInd)
                    if tok == 'boolc':
                        self.rowInd += 1
                        print('\t'*5 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                        return True
                    else:
                        self.failParse('parseExpression', 'boolc RELOP other')
                    return True
            except KeyError:
                pass
        else:
            self.parseArithExp()
            try:
                if self.getSymbol(self.rowInd)[2] == 'relop':
                    line_num, lex, tok = self.getSymbol(self.rowInd)
                    if tok in ('relop'):
                        self.rowInd += 1
                        print('\t'*5 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                    else:
                        self.failParse('parseExpression')
                    self.parseArithExp()
                    return True
            except KeyError:
                pass

    def parseArithExp(self):
        print('\t'*5 + 'parseArithExp():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        self.parseTerm()
        F = True
        while F:
            line_num, lex, tok = self.getSymbol(self.rowInd)
            if tok in ('addop'):
                self.rowInd += 1
                print('\t'*6 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                self.parseTerm()
            else:
                F = False
        return True

    def parseTerm(self):
        print('\t'*6 + 'parseTerm():')
        self.parseFactor()
        F = True
        while F:
            line_num, lex, tok = self.getSymbol(self.rowInd)
            if tok in ('multop', 'powerop'):
                self.rowInd += 1
                print('\t'*6 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                self.parseFactor()
            else:
                F = False
        return True

    def parseFactor(self):
        print('\t'*7 + 'parseFactor():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        print('\t'*7 + 'parseFactor(): In row {0} token {1}'.format(line_num, (lex, tok)))
        if tok in ('intc', 'floatc', 'id'):
            self.rowInd += 1
            print('\t'*7 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        elif lex == '(':
            self.rowInd += 1
            self.parseArithExp()
            self.parseToken(')', 'bracketsop', '\t'*7)
            print('\t'*7 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        else:
            self.failParse('parseFactor', f'token not a factor: {tok}')
        return True

    def parseIdentList(self):
        print('\t\t\t\t parseIdentList():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        if tok in ('strc'):
            self.rowInd += 1
            print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        elif tok in ('id', 'intc', 'floatc'):
            # self.rowInd += 1
            self.parseExpression()
        else:
            self.failParse('parseIdentList', f'token not an id or strc: {tok}')
        return True

    def parseOutput(self):
        print('\t\t\t parseOutput():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        self.rowInd += 1
        self.parseIdentList()
        F = True
        while F:
            line_num, lex, tok = self.getSymbol(self.rowInd)
            if (lex, tok) == (',', 'punct'):
                self.rowInd += 1
                print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                self.parseIdentList()
            else:
                F = False
        return True

    def failParse(self, func, details='nothing.'):
        print(f'Parser ERROR:\n\tFunc: {func}\n\tDetails: {details}')
        print('Fail.')
        exit(1)

    def parseProgram(self):
        try:
            self.parseStatementList()
            print('Success.')
        except SystemExit as e:
            print(e)


def main():
    with open('demo.txt', 'r') as my_code:
        source_code = my_code.read()
    
    print('--- LEX ANALYZER ---')
    lexer = lexAnalyzer.LexAnalyzer()
    table_of_symbols = lexer.lex_analyser(source_code)
    print()

    ind = list(table_of_symbols.keys())[-1] + 1
    table_of_symbols[ind] = (1, '', 'EOF', '')
    
    print('--- SYNTAX ANALYZER ---')
    syntaxAnalyzer = SyntaxAnalyzer(table_of_symbols, 1)
    syntaxAnalyzer.parseProgram()


if __name__ == "__main__":
    main()