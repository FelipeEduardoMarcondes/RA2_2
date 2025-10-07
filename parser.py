# FELIPE EDUARDO MARCONDES
# GRUPO 2

def criarNodeArvore(node_type, value=None, children=None):
    # Cria um nó da árvore.
    if children is None:
        children = []

    return {'type': node_type, 'value': value, 'children': children}


def tokenAtual(parser_state):
    # Retorna o token atual sem consumi-lo.
    pos = parser_state['pos']
    tokens = parser_state['tokens']

    if pos < len(tokens):

        return tokens[pos]
    
    return {'type': 'eof', 'value': None, 'line': 0, 'col': 0}

def consume(parser_state, expected_type):
    # Consome um token do tipo esperado e avança a posição.
    token = tokenAtual(parser_state)
    if token['type'] != expected_type:

        raise SyntaxError(f"Erro na linha {token['line']}: esperado '{expected_type}', encontrado '{token['type']}'")
    
    parser_state['pos'] += 1

    return criarNodeArvore(token['type'], value=token['value'])

def selectProducao(parser_state, non_terminal):
    # Seleciona a produção correta da tabela LL(1).
    token_type = tokenAtual(parser_state)['type']
    tabela = parser_state['tabela']
    production = tabela[non_terminal].get(token_type)

    if production is None:
        token = tokenAtual(parser_state)

        raise SyntaxError(f"Erro na linha {token['line']}: entrada inesperada '{token_type}' para '{non_terminal}'")
    
    return production



def parse_PROGRAM(parser_state):

    production = selectProducao(parser_state, 'PROGRAM')
    ast_list = []

    if production == ['LINE', 'PROGRAM']:
        line_ast = parse_LINE(parser_state)

        if line_ast:
            ast_list.append(line_ast)

        ast_list.extend(parse_PROGRAM(parser_state))

    return ast_list

def parse_LINE(parser_state):
    consume(parser_state, 'lparen')
    stmt_node = parse_STMT(parser_state)
    consume(parser_state, 'rparen')

    return stmt_node

def parse_STMT(parser_state):
    op1 = parse_EXPR(parser_state)

    return parse_STMT_TAIL(parser_state, op1)

def parse_STMT_TAIL(parser_state, op1):
    production = selectProducao(parser_state, 'STMT_TAIL')

    if production == ['EXPR', 'STMT_TAIL_OP']:
        op2 = parse_EXPR(parser_state)

        return parse_STMT_TAIL_OP(parser_state, op1, op2)
    
    elif production == ['res']:
        res_node = consume(parser_state, 'res')
        res_node['children'].append(op1)

        return res_node
    
    elif production == ['epsilon']:
        
        return op1

def parse_STMT_TAIL_OP(parser_state, op1, op2):
    production = selectProducao(parser_state, 'STMT_TAIL_OP')

    if production == ['OP_BIN']:
        op_node = parse_OP_BIN(parser_state)
        op_node['children'] = [op1, op2]

        return op_node
    
    elif production == ['EXPR', 'if']:
        op3 = parse_EXPR(parser_state)
        if_node = consume(parser_state, 'if')
        if_node['children'] = [op1, op2, op3]

        return if_node
    
    elif production == ['while']:

        while_node = consume(parser_state, 'while')
        while_node['children'] = [op1, op2]

        return while_node

def parse_EXPR(parser_state):
    production = selectProducao(parser_state, 'EXPR')

    if production == ['num']:

        return consume(parser_state, 'num')
    
    elif production == ['id']:

        return consume(parser_state, 'id')
    
    elif production == ['lparen', 'STMT', 'rparen']:
        consume(parser_state, 'lparen')
        node = parse_STMT(parser_state)
        consume(parser_state, 'rparen')

        return node

def parse_OP_BIN(parser_state):

    return consume(parser_state, tokenAtual(parser_state)['type'])


def parsear(tokens, tabela_ll1):
    # Retorna uma lista de ASTs para expressões válidas e uma lista de erros para as inválidas.
    expressoes = []
    current_expr_tokens = []
    paren_count = 0
    

    for token in tokens:
        if token['type'] == 'eof':

            break
            
        if token['type'] == 'lparen':
            if paren_count == 0:
                current_expr_tokens = [] # Inicia uma nova expressão

            paren_count += 1
        
        if paren_count > 0:
            current_expr_tokens.append(token)
            
        if token['type'] == 'rparen':
            paren_count -= 1

            if paren_count == 0 and current_expr_tokens:
                expressoes.append(current_expr_tokens)
                current_expr_tokens = []
    
    ast_list = []
    erros = []
    
    for i, expr_tokens in enumerate(expressoes, 1):
        try:
            # Adiciona um EOF ao final de cada expressão para o parser saber onde parar
            expr_tokens_with_eof = expr_tokens + [{'type': 'eof', 'value': None, 'line': expr_tokens[-1]['line'], 'col': 1}]
            
            parser_state = {
                'tokens': expr_tokens_with_eof,
                'pos': 0,
                'tabela': tabela_ll1
            }

            ast_node = parse_LINE(parser_state)
            
            if tokenAtual(parser_state)['type'] != 'eof':
                raise SyntaxError(f"Tokens extras no final da expressão, começando com '{tokenAtual(parser_state)['type']}'")
            
            ast_list.append((i, ast_node))
            
        except (SyntaxError, ValueError) as e:
            erros.append(f"Expressão {i}: {e}")
            
    return ast_list, erros


def construirGramatica():
    # Define a gramática LL(1) da linguagem.
    return {
        'PROGRAM':    [['LINE', 'PROGRAM'], ['epsilon']],
        'LINE':       [['lparen', 'STMT', 'rparen']],
        'STMT':       [['EXPR', 'STMT_TAIL']],
        'STMT_TAIL':  [['EXPR', 'STMT_TAIL_OP'], ['res'], ['epsilon']],
        'STMT_TAIL_OP': [['OP_BIN'], ['EXPR', 'if'], ['while']],
        'EXPR':       [['num'], ['id'], ['lparen', 'STMT', 'rparen']],
        'OP_BIN':     [
            ['plus'], ['minus'], ['mult'], ['div_real'], ['div_int'], ['mod'], ['pow'],
            ['eq'], ['neq'], ['lt'], ['gt'], ['lte'], ['gte'], ['assign']
        ]
    }

def getSimbolos(gramatica):
    # Extrai os símbolos terminais e não-terminais da gramática.
    non_terminals = set(gramatica.keys())
    terminals = set()

    for prods in gramatica.values():

        for prod in prods:

            for symbol in prod:
                if symbol != 'epsilon' and symbol not in non_terminals:
                    terminals.add(symbol)

    return terminals, non_terminals

def calcularFirst(gramatica):
    # Calcula os conjuntos FIRST para a gramática.
    terminals, non_terminals = getSimbolos(gramatica)
    first = {s: {s} for s in terminals}; first['epsilon'] = {'epsilon'}

    for nt in non_terminals: first[nt] = set()

    while True:
        updated = False

        for nt, productions in gramatica.items():

            for prod in productions:

                for symbol in prod:
                    if symbol == 'epsilon':
                        if 'epsilon' not in first[nt]: first[nt].add('epsilon'); updated = True

                        break
                    before = len(first[nt])
                    first_symbol = first.get(symbol, set())
                    first[nt].update(s for s in first_symbol if s != 'epsilon')

                    if len(first[nt]) != before: updated = True

                    if 'epsilon' not in first_symbol: break

                else:
                    if 'epsilon' not in first[nt]: first[nt].add('epsilon'); updated = True

        if not updated: break

    return first

def calcularFollow(gramatica, first):
    # Calcula os conjuntos FOLLOW para a gramática.
    _, non_terminals = getSimbolos(gramatica)
    follow = {nt: set() for nt in non_terminals}
    start_symbol = list(gramatica.keys())[0]
    follow[start_symbol].add('eof')

    while True:
        updated = False

        for nt, productions in gramatica.items():

            for prod in productions:
                trailer = set(follow[nt])

                for i in range(len(prod) - 1, -1, -1):
                    symbol = prod[i]

                    if symbol == 'epsilon': continue

                    if symbol in non_terminals:
                        before = len(follow[symbol])
                        follow[symbol].update(trailer)

                        if len(follow[symbol]) != before: updated = True

                        if 'epsilon' in first[symbol]:
                            trailer.update(s for s in first[symbol] if s != 'epsilon')

                        else: trailer = set(first.get(symbol, set()))

                    else: trailer = first.get(symbol, set())

        if not updated: break

    return follow

def construirTabelaLL1(gramatica, first, follow):
    # Constrói a tabela de parsing LL(1).
    table = {nt: {} for nt in gramatica}
    for A, productions in gramatica.items():

        for prod in productions:
            first_prod = set()

            for symbol in prod:

                if symbol == 'epsilon': first_prod.add('epsilon'); break

                first_symbol = first.get(symbol, set())
                first_prod.update(s for s in first_symbol if s != 'epsilon')

                if 'epsilon' not in first_symbol: break

            else: first_prod.add('epsilon')

            for terminal in first_prod:
                if terminal != 'epsilon':
                    if terminal in table[A]: raise ValueError(f"Conflito LL(1) em ({A}, {terminal})")
                    table[A][terminal] = prod

            if 'epsilon' in first_prod:

                for terminal in follow[A]:
                    if terminal in table[A]: raise ValueError(f"Conflito LL(1) em ({A}, {terminal}) para epsilon")

                    table[A][terminal] = ['epsilon']
    return table