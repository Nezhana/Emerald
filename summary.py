import lexAnalyzer
import semanticAnalyzer
import RPN


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
    syntaxAnalyzer = RPN.SyntaxAnalyzer(table_of_symbols, 1)
    syntaxAnalyzer.parseProgram()

    print()
    print(f'- table_of_ids -\n{syntaxAnalyzer.table_of_ids}')
    print()

    print('--- RPN: postfixCode ---')
    counter = 0
    for lex, tok in RPN.postfixCode:
        counter += 1
        print(f'{counter}: {lex} {tok}')

    print()
    print(f'- tableOfLabel -\n{RPN.tableOfLabel}')

    print()
    print(f'- RPN table -\n{RPN.postfixCode}')

    savePostfixCode(syntaxAnalyzer.table_of_ids, RPN.tableOfLabel, lexer.table_of_constants, RPN.postfixCode)


def savePostfixCode(table_of_ids, tableOfLabel, table_of_constants, postfixCode):
    with open('my_code.postfix', 'w') as my_code:
        my_code.write('.target: Postfix Machine\n')
        my_code.write('.version: 0.2\n\n')

        my_code.write('.vars(\n')
        for name, data in table_of_ids.items():
            my_code.write(f'    {name}\t{data[1]}\n')
        my_code.write(')\n\n')

        my_code.write('.labels(\n')
        for name, data in tableOfLabel.items():
            my_code.write(f'    {name}\t{data}\n')
        my_code.write(')\n\n')

        my_code.write('.constants(\n')
        for name, data in table_of_constants.items():
            my_code.write(f'    {name}\t{data[0]}\n')
        my_code.write(')\n\n')

        my_code.write('.code(\n')
        for name, data in postfixCode:
            my_code.write(f'    {name}\t{data}\n')
        my_code.write(')\n\n')


if __name__ == "__main__":
    main()