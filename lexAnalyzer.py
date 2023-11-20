
class LexAnalyzer():

    def __init__(self):
        print('Lex Analyzer was created.')

        # state-transition function
        self.stf = { (0, 'ws'): 0, \
                (0, 'alpha'): 1, (1, 'alpha'): 1, (1, 'digit'): 1, (1, 'other'): 2, \
                (0, 'digit'): 3, (3, 'digit'): 3, (3, 'other'): 4, (3, 'dot'): 5, \
                (5, 'digit'): 5, (5, 'other'): 6, (0, '<'): 7, (7, 'other'): 16, \
                (7, '='): 8, (8, 'other'): 9, (8, '='): 10, (10, '>'): 11, \
                (10, 'other'): 102, (0, '>'): 17, (17, '='): 18, (17, 'other'): 19, \
                (0, '/'): 30, (0, '*'): 20, (20, '*'): 21, (20, 'other'): 29, (0, '='): 22, \
                (22, 'other'): 24, (22, '='): 23, (0, '!'): 14, \
                (14, '='): 15, (14, 'other'): 101, (0, '+'): 13, (0, '-'): 13, \
                (0, '('): 25, (0, ')'): 25, (0, '"'): 26, (26, 'alpha'): 26, \
                (26, 'digit'): 26, (26, 'specsign'): 26, (26, 'ws'): 26, (26, '"'): 27, \
                (0, 'newline'): 28, (0, 'other'): 103, \
                (0, '=begin'): 31, (31, 'specsign'): 31, (31, 'digit'): 31, (31, 'alpha'): 31,\
                (31, 'ws'): 31, (31, 'newline'): 31, (31, '=end'): 32, \
                (0, '#'): 33, (33, 'alpha'): 33, (33, 'specsign'): 33, \
                (33, 'digit'): 33, (33, 'ws'): 33, (33, 'other'): 34, \
                (0, ','): 35 }

        #language lexemes
        self.tokStateTable = {2: 'id', 4: 'intc', 6: 'floatc', 27: 'strc'}
        self.tokTable = {'+': 'addop', '-': 'addop', '*': 'multop', '/': 'multop', '**': 'powerop', '==': 'relop', '<=': 'relop', '<': 'relop',
                '>': 'relop', '>=': 'relop', '!=': 'relop', '<=>': 'relop', '(': 'bracketsop', ')': 'bracketsop', '=': 'assignop',
                '.': 'dot', ',': 'punct', ':': 'punct', ';': 'punct', '"': 'punct',
                '\n': 'newline', '\r': 'newline', '\t': 'ws', ' ': 'ws',
                'true': 'boolc', 'false': 'boolc',
                'def': 'keywords', 'BEGIN': 'keywords', 'END': 'keywords', 'and': 'keywords', 'begin': 'keywords', 'end': 'keywords',
                'if': 'keywords', 'else': 'keywords', 'elif': 'keywords', 'write': 'keywords', 'for': 'keywords', 'in': 'keywords', 'then': 'keywords',
                'alias': 'keywords', 'break': 'keywords', 'case': 'keywords', 'class': 'keywords', 'defined?': 'keywords', 'do': 'keywords',
                'elsif': 'keywords', 'ensure': 'keywords', 'module': 'keywords', 'next': 'keywords', 'nil': 'keywords', 'not': 'keywords',
                'or': 'keywords', 'redo': 'keywords', 'rescue': 'keywords', 'retry': 'keywords', 'return': 'keywords', 'self': 'keywords',
                'super': 'keywords', 'undef': 'keywords', 'unless': 'keywords', 'until': 'keywords', 'when': 'keywords', 'while': 'keywords',
                'yield': 'keywords', 'print': 'keywords', 'puts': 'keywords', 'gets': 'keywords'}

        self.table_of_symbols = {}
        #{id : (line_num, lexeme, token, specialInd)}

        self.table_of_IDs = {}
        #{ID: specialInd}

        self.table_of_constants = {}
        #{CONST: (token, specialInd)}

        self.initState = 0 #q0
        self.F = (2, 4, 6, 9, 11, 13, 15, 16, 18, 19, 21, 23, 24, 25, 27, 28, 29, 30, 32, 34, 35, 101, 102, 103)
        self.F_error = (101, 102, 103)


        #VARIABLES:
        #symbol_list - список символов
        #source_code - исходный код
        #symbol_counter - счётчик символов
        #line_counter - счётчик строк
        #state - state

    #Визначення класу, до якого належить символ, повертає значення класу
    def check_symbol_class(self, symbol):
        if symbol == '.':
            res = 'dot'
        elif symbol in '0123456789':
            res = 'digit'
        elif symbol in 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz':
            res = 'alpha'
        elif symbol == '\t' or symbol == ' ':
            res = 'ws'
        elif symbol in '\n\r':
            res = 'newline'
        elif symbol in '.:;':
            res = 'specsign'
        elif symbol in '()=+-*/<>"!#,':
            res = symbol
        else: res = 'There are no such symbol in the alphabet.'
        return res

    #Читання наступного символа, повертає сам символ та лічильник символів
    def next_symbol(self, source_code, symbol_counter):
        symbol_counter += 1
        try:
            return (source_code[symbol_counter], symbol_counter)
        except IndexError:
            print('------\nEnd of source code!')
            return (source_code[symbol_counter-1], symbol_counter)

    #Повернення символа у вхідний потік
    def prev_symbol(self, source_code, symbol_counter):
        symbol_counter -= 1
        return symbol_counter

    #Перехід до нового стану, повертає номер наступного стану
    def next_state(self, state, symbol_class):
        try:
            return self.stf[(state, symbol_class)]
        except KeyError:
            return self.stf[(state, 'other')]

    #Обробка таблиць ідентифікаторів та констант, повертає індекс, під яким було записано лексему до однієї з вищезазначених таблиць
    def set_index(self, lexeme, lexeme_class):
        if lexeme_class == 'id':
            if self.table_of_IDs:
                try:
                    last_id = self.table_of_IDs[lexeme]
                except KeyError:
                    last_id = list(self.table_of_IDs.values())[-1]
                    last_id += 1
            else:
                last_id = 1
            self.table_of_IDs[lexeme] = last_id
        else:
            if self.table_of_constants:
                try:
                    last_id = self.table_of_constants[lexeme][1]
                except KeyError:
                    last_id = list(self.table_of_constants.values())[-1][1]
                    last_id += 1
            else:
                last_id = 1
            self.table_of_constants[lexeme] = (lexeme_class, last_id)
        return last_id

    #Перевірка, чи є лексема ключовим (зарезервованим) словом, повертає токен лексеми
    def check_on_keyword(self, lexeme, state):
        if lexeme in self.tokTable:
            token = self.tokTable[lexeme]
        else:
            if state in (4, 6):
                lexeme, state = self.star_processing(lexeme, state)
            try:
                token = self.tokStateTable[state]
            except KeyError:
                lexeme, state = self.star_processing(lexeme, state)
                token = (lexeme, state)
        return token	

    def star_processing(self, lexeme, state):
        try:
            if state == 4:
                try:
                    lexeme = int(lexeme)
                except ValueError:
                    if lexeme[-1] in ' \t\n\r':
                        pass
                    else:
                        state = 103
            elif state == 6:
                try:
                    lexeme = float(lexeme)
                except ValueError:
                    if lexeme[-1] in ' \t\n\r':
                        pass
                    elif lexeme[-2:] == '..':
                        raise TypeError
                    else:
                        state = 103
            else:
                raise ValueError
        except ValueError:
            if lexeme[-1] in ' \t\n\r':
                pass
            elif lexeme[0] == '#':
                pass
            else:
                state = 103
        return lexeme, state

    #Семантична обробка лексем, вивід та заповнення таблиці символів
    def processing(self, lexeme, state, line_counter, source_code, symbol_counter):
        if self.table_of_symbols:
            last_ind_key = list(self.table_of_symbols.keys())[-1]
            if self.table_of_symbols[last_ind_key][2] == 'intc' and lexeme == '.':
                return line_counter, symbol_counter + 1
        if state == 28:
            line_counter += 1
            state = self.initState
            symbol_counter -= 1
        if state in list(self.tokStateTable.keys()) or state in (9, 16, 19, 21, 29, 30, 34):
            try:
                token = self.check_on_keyword(lexeme, state)
            except TypeError:
                symbol_counter -= 1
                lexeme = lexeme[:len(lexeme)-2]
                state = 4
                token = self.check_on_keyword(lexeme, state)
            if token[1] == 103:
                exit(f'Wrong symbol: "{lexeme}"')
            elif token[1] == 34:
                print('{0:<3d} {1:<20s} {2:<10s}'.format(line_counter, token[0], 'onelinecom'))
                return line_counter, symbol_counter
            if token != 'keywords' and token not in self.tokTable.values():
                lexeme_ind = self.set_index(lexeme, token)
                print('{0:<3d} {1:<20s} {2:<10s} {3:<2d}'.format(line_counter, lexeme, token, lexeme_ind))
                self.table_of_symbols[len(self.table_of_symbols)+1] = (line_counter, lexeme, token, lexeme_ind)
                try:
                    if self.table_of_symbols[len(self.table_of_symbols)-1][1] == 'in':
                        self.table_of_symbols[len(self.table_of_symbols)+1] = (line_counter, '..', 'rangeexpr', '')
                        print('{0:<3d} {1:<20s} {2:<10s}'.format(line_counter, '..', 'rangeexpr'))
                        symbol_counter += 2
                except KeyError:
                    pass
            else:
                print('{0:<3d} {1:<20s} {2:<10s}'.format(line_counter, lexeme, token))
                self.table_of_symbols[len(self.table_of_symbols)+1] = (line_counter, lexeme, token, '')
            lexeme = ''
            if token != 'strc':
                symbol_counter = self.prev_symbol(source_code, symbol_counter) #star processing
            state = self.initState
        if state == 35:
            lexeme = ','
        if state in (11, 13, 15, 18, 23, 25, 30, 32, 35):
            token = self.tokTable[lexeme]
            print('{0:<3d} {1:<20s} {2:<10s}'.format(line_counter, lexeme, token))
            self.table_of_symbols[len(self.table_of_symbols)+1] = (line_counter, lexeme, token, '')
            lexeme = ''
            state = self.initState
        if state == 24:
            if len(lexeme) == 1:
                token = self.tokTable[lexeme]
                print('{0:<3d} {1:<20s} {2:<10s}'.format(line_counter, lexeme, token))
                self.table_of_symbols[len(self.table_of_symbols)+1] = (line_counter, lexeme, token, '')
                lexeme = ''
                state = self.initState
                return line_counter, symbol_counter
            else:
                if lexeme[1] == 'b':
                    while lexeme[-1] != '\n':
                        symbol, symbol_counter = self.next_symbol(source_code, symbol_counter)
                        lexeme += symbol
                    lexeme = lexeme.strip('\n')
                    print('{0:<3d} {1:<20s} {2:<10s}'.format(line_counter, lexeme, 'startcom'))
                    line_counter +=1
                elif lexeme[1] == 'e':
                    while lexeme[-1] != '\n':
                        symbol, symbol_counter = self.next_symbol(source_code, symbol_counter)
                        lexeme += symbol
                    lexeme = lexeme.strip('\n')
                    print('{0:<3d} {1:<20s} {2:<10s}'.format(line_counter, lexeme, 'endcom'))
                    line_counter +=1
                    symbol_counter -= 1
        if state in self.F_error:
            self.my_exception()
        return line_counter, symbol_counter + 1

    #Перевірка, чи є стан заключним (фінальним)
    def is_final_state(self, state):
        if state in self.F:
            return True
        else: return False
            
    #Функція верхнього рівня - аналіз усіх символів у циклі
    def lex_analyser(self, source_code):
        symbol_counter = -1
        line_counter = 1
        state = self.initState
        lexeme = ''
        print(f'Lenght of source code: {len(source_code)}')
        try:
            while symbol_counter < len(source_code):
                symbol, symbol_counter = self.next_symbol(source_code, symbol_counter)
                symbol_class = self.check_symbol_class(symbol)
                state = self.next_state(state, symbol_class)
                if self.is_final_state(state):
                    if symbol in ' ,\n':
                        pass
                    else:
                        lexeme += symbol
                    line_counter, symbol_counter = self.processing(lexeme, state, line_counter, source_code, symbol_counter)
                    state = self.initState
                    lexeme = ''
                elif state == self.initState:
                    lexeme = ''
                else:
                    lexeme += symbol
            print('The lexical analyzer did its job successfully.')
            print('------')
            print(f'\n--- TABLE OF SYMBOLS ---\n{self.table_of_symbols}')
            print(f'\n--- TABLE OF IDs ---\n{self.table_of_IDs}')
            print(f'\n--- TABLE OF CONSTANTS ---\n{self.table_of_constants}')
        except SystemExit as e:
            print(f'Exit on symbol: {symbol_counter}')
            print(f'The lexical analyzer failed because of this error: {e}.')
        return self.table_of_symbols

    def my_exception(self):
        raise Exception('Error! Wrong symbol')
