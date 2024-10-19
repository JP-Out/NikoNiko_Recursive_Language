from keywords import reserved_keywords

# Dicionário da Tabela de Simbolos do código
simbols = {}

delimiters = {' ','=',';','{','}','[',']', '(', ')', '"'}
operators = {'=', '+', '-', '*', '/'}

def get_id_by_value(token_value, dict):
    """
    Retorna o índice correspondente ao valor fornecido em um dicionário.

    Args:
        token_value (str): O valor do token que se deseja encontrar.
        dict (dict): O dicionário onde o valor será procurado.

    Returns:
        list of int: Uma lista contendo os índices das chaves no dicionário onde 
                     o valor corresponde ao `token_value`. Retorna uma lista vazia 
                     se o valor não for encontrado.
                     
    Comportamento:
        - Itera sobre o dicionário e verifica se algum valor corresponde ao `token_value` fornecido.
        - Para cada ocorrência, adiciona o índice correspondente a uma lista e a retorna.
    """
    return [i for i, (index, value) in enumerate(dict.items()) if value == token_value]


def is_double_quote(char):
    """
    Verifica se o caractere fornecido é uma string delimitada por aspas duplas.

    Args:
        char (str): A string a ser verificada.

    Returns:
        bool: Retorna True se a string começar e terminar com aspas duplas, 
              caso contrário, retorna False.

    Comportamento:
        - A função verifica se o primeiro e o último caracteres da string fornecida 
          são aspas duplas (").
    """
    return char.startswith('"') and char.endswith('"')

 
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
    return string in reserved_keywords



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
    tokens = []
    token = ""
    is_delimiter = False
    brackets = {'(': ')', '[': ']', '{': '}', '"': '"'}
    stack = []
    
    for line_num, line in enumerate(lines, start=1):
        line_length = len(line.strip())
        
        i = 0  # Inicializando o índice
        while i < len(line):
            char = line[i]
            is_last_char = i == line_length - 1
            
            if char in delimiters or char in operators:
                is_delimiter = True
                if token:
                    tokens.append(token)
                    token = ""
                if char in brackets:
                    stack.append((char, line_num, i))  # Armazena o char, linha e posição
                elif char in brackets.values():
                    if stack and brackets.get(stack[-1][0]) == char:
                        stack.pop()  # Remove par correspondente
                    else:
                        report_error(f"Delimitador inesperado '{char}' em linha {line_num}, coluna {i + 1}.")            
                
            elif is_delimiter:
                tokens.append(token)
                token = ""
                is_delimiter = False
                
            if is_last_char and char != ';':
                report_error(f"';' esperado no final da linha {line_num}, encontrado '{char}'.")

            # Verifica se o último item da pilha é aspas duplas e percorre a partir do índice atual
            if stack and stack[-1][0] == '"':
                i += 1  # Avança o índice para evitar repetição
                token += char # Adiciona a primeira " já ao token
                while i < len(line):
                    this_char = line[i]
                    token += this_char
                    if this_char == '"':  # Fechou aspas duplas
                        stack.pop()  # Remove da pilha
                        break
                    i += 1
            else:
                token += char
            
            i += 1  # Incrementando o índice
        
        if token:
            tokens.append(token)
            token = ""
          
    tokens = [t.strip() for t in tokens if t.strip()]
    
    # Finaliza verificando se há delimitadores abertos não fechados
    if stack:
        for open_char, line_num, pos in stack:
            report_error(f"Delimitador '{open_char}' aberto na linha {line_num}, coluna {pos + 1} não foi fechado.")
    
    return tokens

 
def lexical(tokens):
    """
    Gera uma lista de tokens no formato '<token-name, índice>' ou '<índice, token-id>'
    para cada token encontrado, dependendo se é um token reservado ou um símbolo.

    Args:
        tokens (list of str): A lista de tokens a ser processada.

    Returns:
        list of str: Uma lista de strings, onde cada string representa um token
                     no formato '<token-name, índice>' ou '<índice, token-id>'.
    """
    new_index = 0  # Índice para novos tokens na tabela de símbolos
    lexical_token = []  # Lista para armazenar os tokens formatados
    
    for i, token in enumerate(tokens):
        # Se o token é reservado, operador, delimitador, ou número
        if is_reserved_keyword(token) or is_double_quote(token) or token in delimiters or token in operators or token.isdigit() or isinstance(token, (int, float)):
            expr = f'<{token}, {i}>'
            lexical_token.append(expr)

        # Caso o token não seja reservado, é tratado como um símbolo
        elif token:
            # Se a tabela de símbolos não estiver vazia, definir o próximo índice
            if simbols:
                new_index = max(simbols.keys()) + 1  # Define o novo índice baseado no maior valor existente
            # Se o token já existe na tabela, pegar o índice dele
            if token in simbols.values():
                curr_index = get_id_by_value(token, simbols)[0]  # Pega o índice existente
                expr = f'<TS[{curr_index}], {i}>'
            else:
                simbols[new_index] = token  # Adiciona um novo símbolo na tabela
                expr = f'<TS[{new_index}], {i}>'
            lexical_token.append(expr)  # Adiciona o token formatado à lista

    print(f"Tabela de Símbolos: {simbols}")        
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
