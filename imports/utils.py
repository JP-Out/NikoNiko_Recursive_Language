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
        with open(file_path, "w", encoding="utf-8") as file:
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
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return []
    except IOError:
        print(f"Erro: Não foi possível ler o arquivo '{file_path}'.")
        return []


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
