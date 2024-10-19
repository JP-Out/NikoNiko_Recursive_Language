from keywords import reserved_keywords
from utils import read_file, write_to_file, report_error



delimiters = {' ','=',';','{','}','[',']', '(', ')', '"'}
operators = {'=', '+', '-', '*', '/'}

class SymbolTable:
    def __init__(self):
        self.symbols = {}  # Dicionário para armazenar símbolos
        self.next_index = 0  # Controle do próximo índice

    def add(self, symbol):
        """
        Adiciona um símbolo à tabela se ele ainda não existir. 
        Retorna o índice do símbolo na tabela.

        Args:
            symbol (str): O símbolo a ser adicionado ou verificado.

        Returns:
            int: O índice do símbolo na tabela.
        """
        # Verifica se o símbolo já está na tabela de símbolos
        if symbol not in self.symbols.values():
            self.symbols[self.next_index] = symbol
            self.next_index += 1  # Incrementa o índice para o próximo símbolo

        return self.get_id_by_value(symbol)

    def get_id_by_value(self, value):
        """
        Retorna o índice correspondente ao valor fornecido na tabela de símbolos.

        Args:
            value (str): O valor do símbolo a ser procurado.

        Returns:
            int: O índice do símbolo correspondente ou None se não encontrado.
        """
        for key, val in self.symbols.items():
            if val == value:
                return key
        return None

    def __repr__(self):
        return f"Tabela de Símbolos: {self.symbols}"



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
    symbol_table = SymbolTable()
    lexical_token = []  # Lista para armazenar os tokens formatados
    
    for i, token in enumerate(tokens):
        # Se o token é reservado, operador, delimitador, ou número
        if is_reserved_keyword(token) or is_double_quote(token) or token in delimiters or token in operators or token.isdigit() or isinstance(token, (int, float)):
            expr = f'<{token}, {i}>'
            lexical_token.append(expr)

        # Caso o token não seja reservado, é tratado como um símbolo
        elif token:
            symbol_index = symbol_table.add(token) # Adiciona o símbolo à tabela e pega o índice
            expr = f'<TS[{symbol_index}], {i}>'
            lexical_token.append(expr)  # Adiciona o token formatado à lista

    print(f"Tabela de Símbolos: {symbol_table}")        
    return lexical_token
  
       
# Caminhos          
file_path_input = "io/input.niko"
file_path_lexical = "io/lexical.txt"

# Chamadas
lines = read_file(file_path_input) # Lê o "codigo" de entrada
token_code = scanner(lines) # Processa cada linha
lexical_code = lexical(token_code) # Transforma na expressão lexical

write_to_file(lexical_code, file_path_lexical)
