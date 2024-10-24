from imports.utils import read_file, write_to_file
from src.compiler import Scanner, lexical

# Definir delimitadores e operadores usados na linguagem
delimiters = {' ', '=', ';', '{', '}', '[', ']', '(', ')', '"', '#'}
operators = {'=', '+', '-', '*', '/'}


def main():
    # Caminhos dos arquivos
    file_path_input = "io/input.niko"
    file_path_lexical = "io/lexical.txt"
    
    # Lê o "codigo" de entrada
    lines = read_file(file_path_input)
    
    # Instância do Scanner com os delimitadores e operadores definidos
    scanner = Scanner(delimiters, operators)
    
    # Tokeniza as linhas
    token_code = scanner.scan(lines)
    
    # Processa tokens pra gerar a análise lexical
    lexical_code = lexical(token_code, delimiters, operators)
    
    # Escreve o código lexical no arquivo de saída
    write_to_file(lexical_code, file_path_lexical)
    
    print(f"Tokens gerados: {token_code}")
    print(f"Análise lexical escrita no arquivo: {file_path_lexical}")

if __name__ == "__main__":
    main()
