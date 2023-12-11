

class SemanticAnalyzer():
    
    def __init__(self, sym_table):
        self.table_of_symbols = sym_table
        self.buffer = ''

    def type_when_assign(self):
        pass

    def check_id(self, new_id, table_of_ids):
        if new_id in list(table_of_ids.keys()):
            return False
        else: return True

    def dominating_type(self):
        pass

    def relop_expr_assign(self):
        pass

    def zero_division(self):
        pass

    def rewrite_buffer(self, token):
        if not self.buffer:
            self.buffer = token
        else:
            if token == 'floatc':
                self.buffer = token
            elif token == 'intc':
                if self.buffer == 'floatc':
                    pass
                else:
                    pass
            elif token in ('intc', 'floatc') and self.buffer == 'boolc' or \
            self.buffer in ('intc', 'floatc') and token == 'boolc':
                self.semantic_error('rewrite_buffer', 'type error: operations between bool and nymerical.')
            elif token == 'boolc' and self.buffer == 'boolc':
                pass
            else:
                self.semantic_error('rewrite_buffer', 'type error: wrong type.')

    def empty_buffer(self):
        self.buffer = ''

    def semantic_error(self, func, details='nothing.'):
        print(f'Semantic ERROR:\n\tFunc: {func}\n\tDetails: {details}')
        print('Fail.')
        exit(1)




