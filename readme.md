# NikoNiko Recursive Language (NNRL)

Bem-vindo ao projeto **NikoNiko Recursive Language (NNRL)**, uma linguagem de programação minimalista e personalizada, criada com sintaxe baseada em japonês, projetada para fins educativos e exploração de conceitos de compiladores e linguagens de programação, não possui a intenção de utilizá-la para implementações reais.

## Estrutura do Projeto

```bash
.
└── NikoNiko_Recursive_Language/
    ├── code/
    │   └── compiler.py       # Arquivo principal do compilador
    ├── imports/
    │   ├── keywords.py       # Mapeamento de palavras-chave reservadas
    │   └── utils.py          # Funções auxiliares e ferramentas de suporte
    └── io/
        ├── input.niko        # Código de entrada na linguagem Niko
        └── lexical.txt       # Arquivo de saída da análise lexical
```

### Diretórios:

- **code/**: Contém o compilador principal que analisa e interpreta o código escrito em Niko.
- **imports/**: Contém arquivos de suporte, como palavras-chave reservadas e utilitários.
- **io/**: Contém os arquivos de entrada e saída. `input.niko` é o arquivo de código-fonte que será analisado, e `lexical.txt` armazena o resultado da análise lexical.

## Sintaxe da Linguagem

A NikoNiko Recursive Language utiliza uma sintaxe baseada em palavras e expressões do idioma japonês. Veja abaixo alguns dos elementos principais da linguagem:

### Palavras-chave reservadas:

- **mein** (`main`): Marca o início do programa.
- **modoru** (`return`): Retorna um valor.
- **hyouji** (`print`): Imprime uma mensagem no console.
- **nyuuryoku** (`input`): Recebe uma entrada do usuário.
- **moshi** (`if`): Estrutura condicional.
- **sore igai** (`else`): Alternativa à condição.
- **kurikaeshi** (`for`): Estrutura de repetição.
- **kokoromiru** (`while`): Estrutura de repetição condicional.
  
### Tipos de Dados:

- **seisuu** (`int`): Números inteiros.
- **shousuu** (`float`): Números decimais.
- **mojiretsu** (`str`): Cadeias de caracteres.
- **shingi** (`bool`): Valores booleanos (`True`/`False`).
- **shin** (`True`): Valor verdadeiro.
- **gi** (`False`): Valor falso.

### Operadores Lógicos:

- **katsu** (`and`): Operador lógico E.
- **mata wa** (`or`): Operador lógico OU.
- **dewa nai** (`not`): Operador lógico de negação.

### Exemplo de Código Niko:

```niko
mein {
    hyouji("Olá, Mundo!");
    moshi (nyuuryoku() == seisuu(10)) {
        hyouji("Você digitou dez.");
    } sore igai {
        hyouji("Você digitou outro número.");
    }
}
```

## Funcionalidades do Compilador

### 1. **Scanner**:
- O scanner é responsável por ler o arquivo de entrada `input.niko` e dividir o código em tokens, com base em delimitadores e operadores definidos.
- Ele também verifica erros sintáticos básicos, como a ausência de ponto e vírgula ao final das linhas.

### 2. **Análise Lexical**:
- A análise lexical transforma o código em tokens lexicais, no formato `<token-name, índice>`. Se o token for um símbolo, ele é adicionado à Tabela de Símbolos e associado a um índice.

### 3. **Tabela de Símbolos**:
- A tabela de símbolos é um dicionário que armazena identificadores (como variáveis ou funções) e seus respectivos índices, permitindo a reutilização de nomes e facilitando a análise do código.

### 4. **Classes Auxiliares**:
- **SymbolTable**: Gerencia a tabela de símbolos, adicionando e retornando o índice de símbolos conforme necessário.
- **Utilitários**: Funções auxiliares que facilitam operações no compilador, como leitura e escrita de arquivos, além de manipulações básicas de strings.

## Como Usar

1. **Executar o Compilador**:
   - Escreva seu código no arquivo `io/input.niko`.
   - Execute o compilador presente no arquivo `compiler.py`:

   ```bash
   python code/compiler.py
   ```

2. **Resultados**:
   - O código será analisado, e os tokens gerados serão salvos em `io/lexical.txt`. Caso haja erros, eles serão exibidos no terminal.
   
3. **Adição de Novas Palavras-Chave**:
   - Novas palavras-chave podem ser adicionadas no arquivo `imports/keywords.py`, onde o dicionário `reserved_keywords` mapeia as palavras em japonês para seus equivalentes em Python.