from imports.keywords import reserved_keywords
from imports.utils import report_error

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


class Scanner:
    def __init__(self, delimiters, operators):
        """
        Inicializa o Scanner com os delimitadores e operadores usados para tokenização.
        
        Args:
            delimiters (set of str): Conjunto de delimitadores (ex.: parênteses, colchetes).
            operators (set of str): Conjunto de operadores (ex.: +, -, *, /).
        """
        self.brackets = {'(': ')', '[': ']', '{': '}', '"': '"'}
        self.stack = []
        self.tokens = []
        self.delimiters = delimiters
        self.operators = operators
        
        
    def tokenize(self, line, line_num):
        """
        Tokeniza uma linha de código e verifica se há erros sintáticos básicos.

        Args:
            line (str): A linha de código a ser tokenizada.
            line_num (int): O número da linha (para reportar erros).
        """
        token = ""        
        is_delimiter = False
        line_length = len(line.strip())
        i = 0 # indice
        
        while i < len(line):
            char = line[i]
            is_last_char = i == line_length - 1

            if char in self.delimiters or char in self.operators:
                is_delimiter = True
                if token:
                    self.tokens.append(token)
                    token = ""
                if char in self.brackets:
                    self.stack.append((char, line_num, i))  # Armazena o char, linha e posição
                elif char in self.brackets.values():
                    if self.stack and self.brackets.get(self.stack[-1][0]) == char: # [-1] acessa a ultima tupla da pilha, e [0] o primeiro item da tupla
                        self.stack.pop()  # Remove o par correspondente
                    else:
                        report_error(f"Delimitador inesperado '{char}' em linha {line_num}, coluna {i + 1}.")            

            elif is_delimiter:
                self.tokens.append(token)
                token = ""
                is_delimiter = False

            if is_last_char and char != ';':
                report_error(f"';' esperado no final da linha {line_num}, encontrado '{char}'.")

            # Verifica se o último item da pilha é aspas duplas e percorre a partir do índice atual
            if self.stack and self.stack[-1][0] == '"':
                i += 1  # Avança o índice para evitar repetição
                token += char  # Adiciona a primeira " já ao token
                while i < len(line):
                    this_char = line[i]
                    token += this_char
                    if this_char == '"':  # Fechou aspas duplas
                        self.stack.pop()  # Remove da pilha
                        break
                    i += 1
            else:
                token += char

            i += 1  # Incrementa o índice

        if token:
            self.tokens.append(token)


    def scan(self, lines):
        """
        Analisa uma lista de linhas de código, tokenizando elementos e verificando 
        erros sintáticos básicos, como a ausência de um ponto e vírgula (';') no final da linha.

        Args:
            lines (list of str): Uma lista de strings, onde cada string representa uma linha de código a ser analisada.

        Returns:
            list: Uma lista de tokens extraídos das linhas de código.
        """
        for line_num, line in enumerate(lines, start=1):
            self.tokenize(line, line_num)

        # Verifica se há delimitadores abertos não fechados
        if self.stack:
            for open_char, line_num, pos in self.stack:
                report_error(f"Delimitador '{open_char}' aberto na linha {line_num}, coluna {pos + 1} não foi fechado.")

        # Remove tokens vazios e retorna a lista final de tokens
        self.tokens = [t.strip() for t in self.tokens if t.strip()]
        return self.tokens
              

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

 
def lexical(tokens, delimiters, operators):
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