import lexAnalyzer
import semanticAnalyzer

class SyntaxAnalyzer():

    def __init__(self, sym_table, rowIndex):
        self.table_of_symbols = sym_table
        self.rowInd = rowIndex
        #{ id : (value, type) }
        self.table_of_ids = {}
        self.semantic = semanticAnalyzer.SemanticAnalyzer(sym_table)

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
        #statement : assign | input | index
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
            m1 = createLabel()
            postfixCode.append(m1)
            postfixCode.append(('JF', 'jf'))
            if self.parseStatement():
                pass
            else:
                return False
            if self.parseToken('elif', 'keywords', '\t\t\t'):
                self.parseExpression()
                m2 = createLabel()
                postfixCode.append(m2)
                postfixCode.append(('JFF', 'jff'))
                setValLabel(m1)
                postfixCode.append(m1)
                postfixCode.append((':','colon'))
                if self.parseStatement():
                    pass
                else:
                    return False
            else: pass
            if self.parseToken('else', 'keywords', '\t\t\t'):
                m3 = createLabel()
                postfixCode.append(m3)
                postfixCode.append(('JMP', 'jump'))
                setValLabel(m2)
                postfixCode.append(m2)
                postfixCode.append((':','colon'))
                if self.parseStatement():
                    pass
                else:
                    return False
            else:
                pass
            if self.parseToken('end', 'keywords', '\t\t\t'):
                setValLabel(m3)
                postfixCode.append(m3)
                postfixCode.append((':','colon'))
                return True
            else:
                return False
        except:
            pass

    def parseIndExpr(self):
        print('\t\t\tparseIndExpr():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        indID = lex
        self.rowInd += 1
        if self.parseToken('in', 'keywords', '\t\t\t\t'):
            # 
            range_expr = self.parseRangeExpr(indID)
            return range_expr
        else:
            return False

    def parseRangeExpr(self, indID):
        print('\t\t\t\tparseRangeExpr():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        if tok == 'intc':
            # 
            self.table_of_ids[indID] = (lex, tok)
            # 
            start = (lex, tok)
            self.rowInd += 1
            if self.parseToken('..', 'rangeexpr', '\t\t\t\t'):
                # 
                r2 = (1, 'intc')
                line_num, lex, tok = self.getSymbol(self.rowInd)
                if tok == 'intc':
                    # 
                    target = (lex, tok)
                    print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                    # 
                    return {'start': start, 'step': r2, 'target': target}
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
        postfixCode.append((lex, 'for-id'))
        postfixCode.append(('=', 'assignop'))
        print('\t'*3 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        # 
        range_expr = self.parseIndExpr()
        postfixCodeGen('start-for', range_expr['start'])

        r1 = 1
        postfixCode.append((r1, 'r1'))
        m1 = createLabel()
        postfixCode.append(m1)
        setValLabel(m1)
        postfixCode.append((':','colon'))

        postfixCodeGen('step-for', range_expr['step'])

        m2 = createLabel()
        postfixCode.append(m2)
        postfixCode.append(('JF','jf'))

        postfixCode.append((lex, 'for-id'))
        postfixCodeGen('step-for', range_expr['step'])
        postfixCode.append(('=', 'assignop'))

        postfixCode.append(m2)
        setValLabel(m2)
        postfixCode.append((':','colon'))
        
        r1 = 0
        postfixCode.append((r1, 'r1'))
        
        postfixCodeGen('target-for', range_expr['target'])
        postfixCode.append((lex, 'for-id'))
        postfixCode.append(('-', ''))
        postfixCode.append(('0', 'condition'))
        postfixCode.append(('<', ''))

        self.rowInd += 1
        if self.parseToken('do', 'keywords', '\t\t\t\t'):
            # 
            m3 = createLabel()
            postfixCode.append(m3)
            postfixCode.append(('JF','jf'))

            print('\t\t\tinner statement:')
            self.parseStatement()
            line_num, lex, tok = self.getSymbol(self.rowInd)
            if (lex, tok) == ('end', 'keywords'):
                print('\t'*3 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                self.rowInd += 1
                #
                postfixCode.append(m1)
                postfixCode.append(('JMP','jump'))
                postfixCode.append(m3)
                setValLabel(m3)
                postfixCode.append((':','colon'))

                return True
            elif (lex, tok) == ('', 'EOF') and self.getSymbol(self.rowInd-1) == (10, 'end', 'keywords'):
                self.rowInd -= 1
                line_num, lex, tok = self.getSymbol(self.rowInd)
                print('\t'*3 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                self.rowInd += 1
                #
                postfixCode.append(m1)
                postfixCode.append(('JMP','jump'))
                postfixCode.append(m3)
                postfixCode.append((':','colon'))

                return True
            else:
                self.failParse('parseFor()', 'end keyword was not founded.')
        else:
            return False

    def parseAssign(self):
        print('\t\t\t parseAssign():')
        _, lex, tok = self.getSymbol(self.rowInd)
        new_id = lex
        if not self.semantic.check_id(new_id, self.table_of_ids):
            print(f'\t\t\t ! reassign: {new_id} !')
        postfixCodeGen('lval', (lex, tok))
        self.rowInd += 1
        if self.parseToken('=', 'assignop', '\t\t\t\t'):
            #try parse Input
            try:
                line_num, lex, tok = self.getSymbol(self.rowInd)
                # self.table_of_ids[new_id] = (lex, tok)
                if (lex, tok) == ('gets', 'keywords'):
                    #input statement, temporary skip semantics
                    self.table_of_ids[new_id] = (lex, 'input')
                    postfixCodeGen('rval', (lex, 'input'))
                    print('\t'*5 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                    self.rowInd += 1
                    return True
                else:
                    raise ValueError
            except ValueError:
                val_type = self.parseExpression()
                self.table_of_ids[new_id] = (lex, val_type)
                postfixCodeGen('=',('=','assignop'))
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
                        # postfixCodeGen(lex,(lex,tok))
                        print('\t'*5 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                    else:
                        self.failParse('parseExpression')
                    line_num, lex, tok = self.getSymbol(self.rowInd)
                    if tok == 'boolc':
                        self.rowInd += 1
                        # postfixCodeGen(lex,(lex,tok))
                        print('\t'*5 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                        return True
                    else:
                        self.failParse('parseExpression', 'boolc RELOP other')
                    return True
            except KeyError:
                pass
        else:
            val_type = self.parseArithExp()
            try:
                if self.getSymbol(self.rowInd)[2] == 'relop':
                    line_num, lex, tok = self.getSymbol(self.rowInd)
                    if tok in ('relop'):
                        self.rowInd += 1
                        print('\t'*5 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                    else:
                        self.failParse('parseExpression')
                    val_type = self.parseArithExp()
                    postfixCodeGen(lex,(lex,tok))
            except KeyError:
                pass
            return val_type

    def parseArithExp(self):
        print('\t'*5 + 'parseArithExp():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        val_type_left = self.parseTerm()
        val_type = val_type_left
        F = True
        while F:
            line_num, lex, tok = self.getSymbol(self.rowInd)
            if tok in ('addop'):
                self.rowInd += 1
                print('\t'*6 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                val_type_right = self.parseTerm()
                if val_type_left == val_type_right:
                    postfixCodeGen(lex,(lex,tok))
                    val_type = val_type_right
                elif val_type_right == 'float':
                    postfixCodeGen(lex,(lex,tok))
                    val_type = val_type_right
                else:
                    postfixCodeGen(lex,(lex,tok))
                    val_type = val_type_right
            else:
                F = False
        return val_type

    def parseTerm(self):
        print('\t'*6 + 'parseTerm():')
        val_type_left = self.parseFactor()
        val_type = val_type_left
        F = True
        while F:
            line_num, lex, tok = self.getSymbol(self.rowInd)
            if tok in ('multop', 'powerop'):
                self.rowInd += 1
                print('\t'*6 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
                val_type_right = self.parseFactor()
                if val_type_left == val_type_right:
                    postfixCodeGen(lex,(lex,tok))
                    val_type = val_type_right
                elif val_type_right == 'float':
                    postfixCodeGen(lex,(lex,tok))
                    val_type = val_type_right
                else:
                    postfixCodeGen(lex,(lex,tok))
                    val_type = val_type_right
            else:
                F = False
        return val_type

    def parseFactor(self):
        print('\t'*7 + 'parseFactor():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        print('\t'*7 + 'parseFactor(): In row {0} token {1}'.format(line_num, (lex, tok)))
        if tok in ('intc', 'floatc'):
            val_type = tok
            postfixCodeGen('const', (lex, tok))
            self.rowInd += 1
            print('\t'*7 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        elif tok == 'id':
            if self.semantic.check_id(lex, self.table_of_ids):
                self.failParse('parseFactor', f'id doesnt exist: {lex}')
            val_type = self.table_of_ids[lex][1]
            postfixCodeGen('rval', (lex, 'rval'))
            self.rowInd += 1
            print('\t'*7 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        elif lex == '(':
            self.rowInd += 1
            val_type = self.parseArithExp()
            self.parseToken(')', 'bracketsop', '\t'*7)
            print('\t'*7 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        else:
            self.failParse('parseFactor', f'token not a factor: {tok}')
        return val_type

    def parseIdentList(self):
        print('\t\t\t\t parseIdentList():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        if tok in ('strc'):
            postfixCodeGen('rval', (lex, tok))
            self.rowInd += 1
            print('\t'*4 + 'In row {0} token {1}'.format(line_num, (lex, tok)))
        elif tok in ('id', 'intc', 'floatc'):
            self.parseExpression()
        else:
            self.failParse('parseIdentList', f'token not an id or strc: {tok}')
        return True

    def parseOutput(self):
        print('\t\t\t parseOutput():')
        line_num, lex, tok = self.getSymbol(self.rowInd)
        postfixCodeGen('lval', (lex, 'output'))
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

postfixCode = list()

def postfixCodeGen(case, toTran):
    if case == 'lval':
        lex,tok = toTran
        postfixCode.append((lex,'l-val'))
    elif case == 'rval':
        lex,tok = toTran
        postfixCode.append((lex,'r-val'))
    elif case == 'start-for':
        lex,tok = toTran
        postfixCode.append((lex,'start-for'))
    elif case == 'step-for':
        lex,tok = toTran
        postfixCode.append((lex,'step-for'))
    elif case == 'target-for':
        lex,tok = toTran
        postfixCode.append((lex,'target-for'))
    else:
        lex,tok = toTran
        postfixCode.append((lex,tok))

tableOfLabel = dict()

def createLabel():
    nmb = len(tableOfLabel) + 1
    lexeme = "m" + str(nmb)
    val = tableOfLabel.get(lexeme)
    if val is None:
        tableOfLabel[lexeme] = 'val_undef'
        tok = 'label' # # #
    else:
        tok = 'LabelError'
        print(tok)
        exit(1003)
    return (lexeme, tok)

def setValLabel(lbl):
    lex, _tok = lbl
    tableOfLabel[lex] = len(postfixCode) + 1
    return True

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

    print()
    print(f'- table_of_ids -\n{syntaxAnalyzer.table_of_ids}')
    print()

    print('--- RPN: postfixCode ---')
    counter = 0
    for lex, tok in postfixCode:
        counter += 1
        print(f'{counter}: {lex} {tok}')

    print()
    print(f'- tableOfLabel -\n{tableOfLabel}')


if __name__ == "__main__":
    main()