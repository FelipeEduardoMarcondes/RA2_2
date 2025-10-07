# Analisador Sintático LL(1) para Linguagem RPN

- **Autor:** FELIPE EDUARDO MARCONDES
- **Grupo:** 2
- **Universidade:** Pontifícia Universidade Católica do Paraná (PUCPR)
- **Curso:** Linguagens Formais e Compiladores

## Visão Geral

Este projeto consiste em um analisador sintático descendente recursivo do tipo **LL(1)** desenvolvido em Python. O analisador processa uma linguagem de programação simplificada que utiliza a Notação Polonesa Reversa (RPN).

O programa recebe como entrada um vetor de tokens gerado por um analisador léxico e tem como objetivos:
- Validar a estrutura sintática do código.
- Gerar uma Árvore Sintática (AST) para cada expressão válida.
- Identificar e reportar erros sintáticos de forma clara.

---

## Pré-requisitos

- Python 3.x

## Como Executar

O programa é executado diretamente pela linha de comando, recebendo como argumento o caminho para o arquivo de teste.

```bash
python AnalisadorSintatico.py <arquivo_de_teste.txt>
```

**Exemplo:**

```bash
python AnalisadorSintatico.py teste1.txt
```

---

# Gramática LL(1)

## Símbolos Terminais

| Terminal   | Símbolo | Descrição                             |
| :--------- | :------ | :------------------------------------ |
| `lparen`   | `(`     | Abre parênteses                       |
| `rparen`   | `)`     | Fecha parênteses                      |
| `plus`     | `+`     | Adição                                |
| `minus`    | `-`     | Subtração                             |
| `mult`     | `*`     | Multiplicação                         |
| `div_real` | `\|`    | Divisão (ponto flutuante)             |
| `div_int`  | `/`     | Divisão (inteira)                     |
| `mod`      | `%`     | Módulo (resto da divisão)             |
| `pow`      | `^`     | Potenciação                           |
| `eq`       | `==`    | Igualdade                             |
| `neq`      | `!=`    | Diferença                             |
| `lt`       | `<`     | Menor que                             |
| `gt`       | `>`     | Maior que                             |
| `lte`      | `<=`    | Menor ou igual que                    |
| `gte`      | `>=`    | Maior ou igual que                    |
| `assign`   | `:=`    | Atribuição                            |
| `num`      | N/A     | Literal numérico (inteiro ou real)    |
| `id`       | N/A     | Identificador (ex: `A`, `VAR`)        |
| `res`      | `res`   | Keyword para comando de histórico     |
| `if`       | `if`    | Keyword para estrutura condicional    |
| `while`    | `while` | Keyword para estrutura de repetição   |
| `eof`      | N/A     | Marcador de fim de arquivo            |

## Produções da Gramática

> **PROGRAM** → `LINE` `PROGRAM` | **ε**
>
> **LINE** → `lparen` `STMT` `rparen`
>
> **STMT** → `EXPR` `STMT_TAIL`
>
> **STMT_TAIL** → `EXPR` `STMT_TAIL_OP` | `res` | **ε**
>
> **STMT_TAIL_OP** → `OP_BIN` | `EXPR` `if` | `while`
>
> **EXPR** → `num` | `id` | `lparen` `STMT` `rparen`
>
> **OP_BIN** → `plus` | `minus` | `mult` | `div_real` | `div_int` | `mod` | `pow` | `eq` | `neq` | `lt` | `gt` | `lte` | `gte` | `assign`

## Conjuntos FIRST

- **FIRST(PROGRAM)** = { `lparen`, **ε** }
- **FIRST(LINE)** = { `lparen` }
- **FIRST(STMT)** = { `num`, `id`, `lparen` }
- **FIRST(STMT_TAIL)** = { `num`, `id`, `lparen`, `res`, **ε** }
- **FIRST(STMT_TAIL_OP)** = { `plus`, `minus`, `mult`, `div_real`, `div_int`, `mod`, `pow`, `eq`, `neq`, `lt`, `gt`, `lte`, `gte`, `assign`, `num`, `id`, `lparen`, `while` }
- **FIRST(EXPR)** = { `num`, `id`, `lparen` }
- **FIRST(OP_BIN)** = { `plus`, `minus`, `mult`, `div_real`, `div_int`, `mod`, `pow`, `eq`, `neq`, `lt`, `gt`, `lte`, `gte`, `assign` }

## Conjuntos FOLLOW

- **FOLLOW(PROGRAM)** = { `eof` }
- **FOLLOW(LINE)** = { `lparen`, `eof` }
- **FOLLOW(STMT)** = { `rparen` }
- **FOLLOW(STMT_TAIL)** = { `rparen` }
- **FOLLOW(STMT_TAIL_OP)** = { `rparen` }
- **FOLLOW(EXPR)** = { `plus`, `minus`, `mult`, `div_real`, `div_int`, `mod`, `pow`, `eq`, `neq`, `lt`, `gt`, `lte`, `gte`, `assign`, `num`, `id`, `lparen`, `while`, `res`, `rparen`, `if` }
- **FOLLOW(OP_BIN)** = { `rparen` }

---

# Estruturas de Controle

### Estrutura IF

- **Sintaxe:** `(condição valor_verdadeiro valor_falso if)`
- **Descrição:** Avalia a `condição`. Se for verdadeira, retorna `valor_verdadeiro`; caso contrário, retorna `valor_falso`.
- **Exemplo:**
  ```rpn
  # Se A > 0, retorna A; senão, retorna 0
  ((A 0 >) (A) (0) if)
  ```

### Estrutura WHILE

- **Sintaxe:** `(condição corpo while)`
- **Descrição:** Enquanto a `condição` for verdadeira, executa o `corpo` repetidamente.
- **Exemplo:**
  ```rpn
  # Enquanto I < 10, incrementa I
  ((I 10 <) ((I 1 +) I assign) while)
  ```