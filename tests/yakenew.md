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

----------------------Docstrings----------------------------------:

Adicionada docstring ao módulo
Adicionada docstring à classe
Adicionadas docstrings aos métodos com descrição dos parâmetros

----------------------Formatação----------------------------------:

Espaçamento atualizados
Parênteses removidos de condicionais desnecessários
Limite de 100 caracteres
Parâmetros do __init__ organizados verticalmente para melhor legibilidade

-----------------------Boas práticas------------------------------:

Removida herança explícita de object (atualmente desnecessária em Python 3)
Melhorada mensagem de exceção
Substituído

    == False
por
    not

Melhorada verificação de string vazia usando if not text

-------------------------Consistência-----------------------------:

Uso consistente de aspas simples
Tratamento de exceções mais específico
Nomes mais descritivos para variáveis temporárias

Status semanda 07/02/2025   //////Refactoring score (3.21)

- Exploração das mencionadas ferramentas puppet e cheff.
(Ferramentas que acabam por ser extremamente parecidas ao git actions, não considero que usá-las seja algo que vala a pena; visto que o github actions será mais intuitivo.) (04 e 05 /02/2025)

- finalização da configuração do pylint (Git Action), que me deu uma série de "code smells" em vários ficheiros. (07/02/2025)

pylint: Action capaz de avaliar um commit, analizando todos os ficheiros .py, num sistema de pontos de 0 a 10 realçando melhoramentos.

Planos próxima semana:

- Criação de novos testes e possivel automatização dos mesmos para puder aprofundar refatorização.
  (de 9 a 11 pretendo acabar esta etapa), visto que viajo dia 14 e 15

- Caso consigo tempo, começar a tratar de problemas identificados pelo pylint

Status semana 14/02/2025   //////Refactoring score (3.21)

- Automatização dos testes de resultados

Planos próxima semana

- Avançar com refatorização e tratamento de problemas identificados pelo pylint.

////// Refactoring score (3.21) -> (3.94) 18/02/2025

Tamanhos de linha e troca para enumerate
isinstance() por vez de type()

////// Refactoring score (3.94) -> (5.07) 20/02/2025

indexação de linhas e espaços
tamanho de linhas
atualizados os catches de erros (especificação quantos aos catches)

////// Refactoring score (5.07) -> (6.57) 25/02/2025

organização dos métodos, classes e variaveis
generator por vez 'sum'
enumerate por vez de iteração com range e len
prefixos com 'u' e 'r' removidos e adicionados respetivamente ( 'u' não necessarios para o python 3.10 e o contrário para 'r')