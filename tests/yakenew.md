Importações:

Organizadas em grupos (stdlib, third-party, local)
Ordenadas alfabeticamente
Removida importação não utilizada de string


Nomes de variáveis e funções:

Convertidos para snake_case: dedupLim → dedup_lim
windowsSize → window_size
stop_fil → stop_file
todedup → candidates_sorted
toadd → should_add


Docstrings:

Adicionada docstring ao módulo
Adicionada docstring à classe
Adicionadas docstrings aos métodos com descrição dos parâmetros


Formatação:

Espaçamento atualizados
Parênteses removidos de condicionais desnecessários
Limite de 79 caracteres
Parâmetros do __init__ organizados verticalmente para melhor legibilidade


Boas práticas:

Removida herança explícita de object (atualmente desnecessária em Python 3)
Melhorada mensagem de exceção
Substituído

    == False
por
    not

Melhorada verificação de string vazia usando if not text


Consistência:

Uso consistente de aspas simples
Tratamento de exceções mais específico
Nomes mais descritivos para variáveis temporárias




Status 06/02/2025

- Exploração das mencionadas ferramentas puppet e cheff.
(Ferramentas que acabam por ser extremamente parecidas ao git actions, não considero que usá-las seja algo que vala a pena; visto que o github actions será mais intuitivo.)

- Criação de dataset para criar mais testes e poder aprofundar refatorização 