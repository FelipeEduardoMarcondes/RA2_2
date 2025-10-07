# FELIPE EDUARDO MARCONDES
# GRUPO 2
# Universidade: Pontifícia Universidade Católica do Paraná
# Curso: Linguagens Formais e Compiladores

## Este projeto consiste em um analisador sintático descendente recursivo do tipo LL(1) desenvolvido em Python. O analisador é projetado para processar uma linguagem de programação simplificada que utiliza a Notação Polonesa Reversa (RPN). Ele recebe como entrada um vetor de tokens gerado por um analisador léxico e tem como objetivo validar a estrutura sintática do código, gerar uma Árvore Sintática para cada expressão válida e identificar erros sintáticos.

Pré-requisitos
Python 3.x

O programa é executado diretamente pela linha de comando, recebendo como argumento o caminho para o arquivo de teste.

python AnalisadorSintatico.py <arquivo_de_teste.txt>

Exemplo:

python main.py teste1.txt

# Gramática LL(1)

## Símbolos Terminais
'
lparen     : '('
rparen     : ')'
plus       : '+'
minus      : '-'
mult       : '*'
div_real   : '|'
div_int    : '/'
mod        : '%'
pow        : '^'
eq         : '=='
neq        : '!='
lt         : '<'
gt         : '>'
lte        : '<='
gte        : '>='
assign     : ':=' (operador de atribuição)
num        : Literal numérico (inteiro ou real)
id         : Identificador (letras maiúsculas: A, B, VAR, CONTADOR, etc.)
res        : 'res' (keyword - comando de histórico)
if         : 'if' (keyword - estrutura condicional)
while      : 'while' (keyword - estrutura de repetição)
eof        : Fim do arquivo (marcador de fim de entrada)
'
## Produções da Gramática
'
PROGRAM      -> LINE PROGRAM 
                | ε

LINE         -> lparen STMT rparen

STMT         -> EXPR STMT_TAIL

STMT_TAIL    -> EXPR STMT_TAIL_OP 
                | res 
                | ε

STMT_TAIL_OP -> OP_BIN 
                | EXPR if 
                | while

EXPR         -> num 
                | id 
                | lparen STMT rparen

OP_BIN       -> plus | minus | mult | div_real | div_int | mod | pow | 
                eq | neq | lt | gt | lte | gte | assign
'
## Conjuntos FIRST

FIRST(PROGRAM)      = { lparen, ε }
FIRST(LINE)         = { lparen }
FIRST(STMT)         = { num, id, lparen }
FIRST(STMT_TAIL)    = { num, id, lparen, res, ε }
FIRST(STMT_TAIL_OP) = { plus, minus, mult, div_real, div_int, mod, pow, eq, neq, lt, gt, lte, gte, assign, num, id, lparen, while }
FIRST(EXPR)         = { num, id, lparen }
FIRST(OP_BIN)       = { plus, minus, mult, div_real, div_int, mod, pow, eq, neq, lt, gt, lte, gte, assign }

## Conjuntos FOLLOW

FOLLOW(PROGRAM)      = { eof }
FOLLOW(LINE)         = { lparen, eof }
FOLLOW(STMT)         = { rparen }
FOLLOW(STMT_TAIL)    = { rparen }
FOLLOW(STMT_TAIL_OP) = { rparen }
FOLLOW(EXPR)         = { plus, minus, mult, div_real, div_int, mod, pow, eq, neq, lt, gt, lte, gte, assign, num, id, lparen, while, res, rparen, if }
FOLLOW(OP_BIN)       = { rparen }

## Estruturas de Controle

----------------------------------------------------------------------------------------------------------------------------------------
### Estrutura IF
**Sintaxe**: `(condição valor_verdadeiro valor_falso IF)`

**Descrição**: Avalia a condição. Se for verdadeira, retorna valor_verdadeiro, caso contrário, retorna valor_falso.

**Exemplos**:

# Se A > 0 retorna A, senão retorna 0
((A 0 >) (A) (0) if)


### Estrutura WHILE
**Sintaxe**: `(condição corpo WHILE)`

**Descrição**: Enquanto a condição for verdadeira (diferente de zero), executa o corpo repetidamente.

**Exemplos**:

 # Enquanto I < 10, incrementa I
((I 10 <) ((I 1 +) I assign) while)

----------------------------------------------------------------------------------------------------------------------------------------