# Dicionário de palavras-chave e seus equivalentes em Python
reserved_keywords = {
    "mein": "main",             # Marca o início do programa `main`
    "modoru": "return",         # Retorna um valor `return`
    "hyouji": "print",          # Imprime o texto `print`
    "nyuuryoku": "input",       # Lê o texto de entrada `input`
    "moshi": "if",              # Início de uma estrutura condicional `if`
    "sore igai": "else",        # Alternativa na estrutura condicional `else`
    "kurikaeshi": "for",        # Início de uma estrutura de repetição `for`
    "kokoromiru": "while",      # Início de uma estrutura de repetição `while`

    # Tipos de dados
    "seisuu": "int",            # Representa números inteiros `int`
    "shousuu": "float",         # Representa números decimais `float`
    "mojiretsu": "str",         # Representa sequências de caracteres `str`
    "shingi": "bool",           # Representa valores verdadeiro/falso `bool`
    # "mu": "None",               # Representa uma função que não retorna valor `None`
    # "nuru": "None",             # Representa um valor nulo `None`
    "shin": "True",             # Representa o valor verdadeiro `True`
    "gi": "False",              # Representa o valor falso `False`

    # Operadores Lógicos
    "katsu": "and",             # Representa o operador lógico `and`
    "mata wa": "or",            # Representa o operador lógico `or`
    "dewa nai": "not"           # Representa o operador lógico `not`
}

# Dicionário da Tabela de Simbolos do código
simbols = {}

delimiters = {' ','=',';','{','}','[',']', '(', ')', '"'}
operators = {'=', '+', '-', '*', '/'}

def get_id_by_value(s_value, dict): # Pega o id do dicionario pelo seu valor
    return [i for i, (index, value) in enumerate(dict.items()) if value == s_value]

def is_reserved_keyword(string):
    """
    Verifica se uma determinada string é uma palavra-chave reservada na linguagem de programação.

    Args:
        string (str): A string a ser verificada.

    Returns:
        bool: Retorna True se a string for uma palavra-chave reservada, caso contrário, retorna False.

    Comportamento:
        - Compara a string fornecida com uma lista ou conjunto de palavras-chave reservadas.
        - Retorna True se houver uma correspondência, indicando que a string é uma palavra reservada.
    """
    if string in reserved_keywords:
       return True 
    return False

def write_to_file(content_list, file_path):
    """
    Escreve o conteúdo fornecido em um arquivo, sobrescrevendo qualquer conteúdo existente.

    Args:
        content (str): O texto que será escrito no arquivo.
        file_path (str): O caminho do arquivo onde o conteúdo será salvo.

    Comportamento:
        - Abre o arquivo especificado no modo de escrita ('w'), que sobrescreve o conteúdo existente.
        - Grava o conteúdo fornecido no arquivo.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(content_list))
        print(f"Conteúdo gravado com sucesso em '{file_path}'.")
    except IOError:
        print(f"Erro: Não foi possível escrever no arquivo '{file_path}'.")


def read_file(file_path):
    """
    Lê o conteúdo de um arquivo e retorna uma lista de linhas.

    Args:
        file_path (str): O caminho para o arquivo a ser lido.

    Returns:
        list of str: Uma lista de strings, onde cada string representa uma linha do arquivo.
                     Retorna uma lista vazia se o arquivo não for encontrado ou se ocorrer um erro de leitura.

    Comportamento:
        - Tenta abrir o arquivo no modo de leitura ('r') com codificação UTF-8.
        - Retorna o conteúdo do arquivo como uma lista de linhas.
        - Imprime uma mensagem de erro e retorna uma lista vazia se o arquivo não for encontrado (FileNotFoundError) 
          ou se houver um problema na leitura (IOError).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return []
    except IOError:
        print(f"Erro: Não foi possível ler o arquivo '{file_path}'.")
        return []


def scanner(lines):
    """
    Analisa uma lista de linhas de código, tokenizando elementos e verificando 
    erros sintáticos básicos, como a ausência de um ponto e vírgula (';') no final da linha.

    Args:
        lines (list of str): Uma lista de strings, onde cada string representa uma linha de código a ser analisada.

    Returns:
        list: Uma lista de tokens extraídos das linhas de código.

    Comportamento:
        - Para cada linha, separa tokens com base em delimitadores e operadores.
        - Gera uma mensagem de erro caso o último caractere de uma linha não seja um ponto e vírgula (';').
    """
    tokens = [] # Lista com os tokens
    token = ""
    is_delimiter = False

    for line in lines:
        line_lenght = len(line.strip())
        
        for i, char in enumerate(line):
            is_last_char = i == line_lenght - 1
            
            if char in delimiters or char in operators:
                is_delimiter = True # O caracter atual é um delimitador
                if token: # Se tiver algo no token
                    tokens.append(token)
                    token = ""
            elif(is_delimiter):
                tokens.append(token)
                token = ""
                is_delimiter = False
                
            if is_last_char and char != ';': # Se for o caracter final e não for `;`
                report_error(f"';' esperado no final da linha, encontrado '{char}'")
                
            token += char # Enquanto `char` não for um delimitador ou operador, continua adicionando
            
        if token:
            tokens.append(token)
            token = ""
          
    # Remove tokens que são apenas espaços ou quebras de linha
    tokens = [t.strip() for t in tokens if t.strip()]
    
    return tokens


def lexical(tokens):
    """
    Gera uma lista de tokens no formato '<token-name, índice>' para cada token reservado.

    Args:
        tokens (list of str): A lista de tokens a ser processada.

    Returns:
        list of str: Uma lista de strings, onde cada string representa um token
                     no formato '<token-name, índice>'.
    """
    new_index = 0 # Cria um novo indice 
    lexical_token = []  # Lista para armazenar os tokens formatados
    for i, token in enumerate(tokens):
        if (is_reserved_keyword(token) or token in delimiters or token in operators or token.isdigit() or isinstance(token, (int, float))):  # Se for uma palavra reservada, delimitador, operador, número, ou tipo numérico          
            expr = f'<{token}, {i}>'
            lexical_token.append(expr)
        elif token:
            if simbols.items(): # se tiver algo no array
                for index in simbols.keys(): # Percorre todos os indices
                    new_index = index + 1 # Se ja existir indice no dicionario, então adiciona um novo
            elif token in simbols.values(): # Se algum token ja estiver na "Tabela/Dicionário de Simbolos"
                # Pegar o id desse token especifico
                # adicionar na lista `lexical_token` esse id novamente
                ...
            simbols[new_index] = token # Cria um novo valor na "Tabela/Dicionário de Simbolos"        
            expr = f'<{i}, {new_index}>'
            lexical_token.append(expr) # Adiciona a expressão na lista
    print(f"DICIONARIO: {simbols}")
    return lexical_token


def report_error(message):
    """
    Exibe ou registra uma mensagem de erro durante a análise do código.

    Args:
        message (str): A mensagem de erro a ser exibida, descrevendo o tipo e a localização do erro.

    Comportamento:
        - Recebe uma mensagem de erro como string e a imprime diretamente no console.
        - Pode ser adaptada para registrar erros em uma lista ou arquivo, dependendo da necessidade.
    """
    print(f"Erro: {message}")
       
# Caminhos          
file_path_input = "io/input.niko"
file_path_lexical = "io/lexical.txt"

# Chamadas
lines = read_file(file_path_input) # Lê o "codigo" de entrada
token_code = scanner(lines) # Processa cada linha
lexical_code = lexical(token_code) # Transforma na expressão lexical

write_to_file(lexical_code, file_path_lexical)
