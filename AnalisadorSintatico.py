# FELIPE EDUARDO MARCONDES
# GRUPO 2

import json
import sys
from leitor import lerTokens
from parser import parsear, construirGramatica, calcularFirst, calcularFollow, construirTabelaLL1

def gerarArvore(node, indent=0, prefix=""):
    if node is None:
        return
    
    print("  " * indent + prefix + node['type'], end="")

    if node['value'] is not None:
        print(f" = {node['value']}")

    else:
        print()

    for i, child in enumerate(node['children']):
        is_last = (i == len(node['children']) - 1)
        child_prefix = "└─ " if is_last else "├─ "

        gerarArvore(child, indent + 1, child_prefix)

def salvarArvore(tree, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tree, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) != 2:
        print("Uso: python AnalisadorSintatico.py <arquivo_de_teste.txt>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        print(f"=== Analisando arquivo: {filename} ===\n")

        gramatica = construirGramatica()
        first = calcularFirst(gramatica)
        follow = calcularFollow(gramatica, first)
        tabela_ll1 = construirTabelaLL1(gramatica, first, follow)
        
        tokens = lerTokens(filename)
        
        ast_list_com_indices, erros = parsear(tokens, tabela_ll1)
        
        if erros:
            print("=== ERROS SINTÁTICOS ENCONTRADOS ===\n")

            for erro in erros:
                print(f"- {erro}")

            print("\n" + "=" * 40 + "\n")
            
        if not ast_list_com_indices:
            print("Nenhuma expressão válida encontrada para gerar árvore.")

        else:
            print("=== ÁRVORES SINTÁTICAS GERADAS (EXPRESSÕES VÁLIDAS) ===\n")
            arvores_para_salvar = []

            for i, tree in ast_list_com_indices:
                print(f"--- Árvore da Expressão {i} ---")
                gerarArvore(tree)
                print("-" * (25 + len(str(i))))
                print()
                arvores_para_salvar.append(tree)

            output_file = filename.replace('.txt', '_arvore.json')

            if arvores_para_salvar:
                salvarArvore(arvores_para_salvar, output_file)
                print(f"\nÁrvore(s) salva(s) em: {output_file}")
            
    except (FileNotFoundError, ValueError, SyntaxError) as e:
        print(f"\nERRO GERAL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()