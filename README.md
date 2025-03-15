# [UFS 2024.2] Resolução do Problema de Seleção Ótima de Pedidos em Waves - SBPO 2025

O presente trabalho explica e demonstra uma solução para a prova da Unidade 2 da disciplina de Inteligência Artificial (2024.2). A prova se baseia no [Desafio SBPO 2025 - Problema da Seleção de pedidos Ótima](https://github.com/mercadolibre/challenge-sbpo-2025/blob/master/docs/pt_problem_description.pdf?authuser=0).

---

## Parte 1: Modelagem do Problema como CSP

**Definição dos Componentes (X, D, C):**

- **Variáveis (X):**  
  - **Pedidos:** O0, O1, O2, O3, O4  
  - **Corredores:** A0, A1, A2, A3, A4  

- **Domínios (D):**  
  Cada variável pode assumir o valor 0 (não selecionado) ou 1 (selecionado).

- **Restrições (C):**  
  1. **Total de Unidades:**  
     Se todas as variáveis dos pedidos estiverem atribuídas, a soma das unidades dos pedidos selecionados deve estar entre o limite inferior (LB) e o limite superior (UB).
  2. **Disponibilidade:**  
     Quando todas as variáveis (pedidos e corredores) estão atribuídas, para cada item a quantidade total solicitada (nos pedidos selecionados) não pode exceder a quantidade disponível (nos corredores selecionados).

**Função Objetivo:**  
A produtividade é definida pela média de itens coletados por corredor, isto é:

$$
\text{Objetivo} = \frac{\text{Total de Unidades dos Pedidos Selecionados}}{\text{Número de Corredores Selecionados}}
$$

Para desempate, também se considera o total de unidades – ou seja, entre soluções com a mesma média, a que tiver maior total de unidades é considerada melhor.

---

## Parte 2: Implementação da Solução com AIMA-Python

O código completo da solução pode ser encontrado em [aima/unidade2_mercadolivre.py](https://github.com/wilfilho/aima-python/blob/master/aima/unidade2_mercadolivre.py).

Esta implementação utiliza as estruturas de dados básicas para representar o problema:
- **Dicionários para os dados:**  
  Os dados dos pedidos e dos corredores são armazenados em dicionários (`orders_data` e `corridors_data`), onde cada chave representa um identificador e o valor é uma lista com as quantidades dos itens.
- **Listas para as variáveis:**  
  As variáveis do problema são definidas como a união dos identificadores de pedidos e de corredores.
- **Dicionários para os domínios e vizinhança:**  
  Cada variável tem como domínio o conjunto {0, 1} e as estruturas `domains` e `neighbors` são definidas para facilitar a aplicação das restrições.

A classe **OrderCSP** foi construída estendendo a classe base **CSP** do AIMA, que serviu de fundamento para nossa solução. Ela redefine métodos cruciais, como:
- `nconflicts` – que verifica os conflitos globais, utilizando a função `constraints` para validar a consistência de uma atribuição.
- `assign` e `unassign` – para gerenciar as atribuições das variáveis.
- `select_unassigned_variable` – para escolher a próxima variável a ser atribuída durante a busca.

A função `all_solutions` implementa uma busca por backtracking que enumera todas as soluções viáveis. Para cada solução, é calculado o valor objetivo (um par contendo a média de itens por corredor e o total de unidades), o que permite comparar diferentes waves geradas e, finalmente, selecionar a solução que maximiza a produtividade.

Os passos para rodar a solução são:

1. Clone o projeto:  
   `$ git clone https://github.com/wilfilho/aima-python`
2. Entre no diretório:  
   `$ cd aima-python`
3. Crie um ambiente virtual:  
   `$ python3 -m venv csp-env`
4. Ative o ambiente:  
   `$ source csp-env/bin/activate`
5. Instale os pacotes necessários:  
   `$ pip install -r aima/requirements.txt`
6. Rode o código:  
   `$ python aima/unidade2_mercadolivre.py`

---

## Parte 3: Testes, Validação e Análise de Desempenho

### Teste com o Exemplo Fornecido

**Dados do Exemplo:**

- **Pedidos:**  
  - O0: [3, 0, 1, 0, 0]  
  - O1: [0, 1, 0, 1, 0]  
  - O2: [0, 0, 1, 0, 2]  
  - O3: [1, 0, 2, 1, 1]  
  - O4: [0, 1, 0, 0, 0]

- **Corredores:**  
  - A0: [2, 1, 1, 0, 1]  
  - A1: [2, 1, 2, 0, 1]  
  - A2: [0, 2, 0, 1, 2]  
  - A3: [2, 1, 0, 1, 1]  
  - A4: [0, 1, 2, 1, 2]

- **Limites:** LB = 5 e UB = 12

**Cálculo do Valor Objetivo:**  
Cada wave é avaliada pela função objetivo, que calcula:

$$
\text{Média} = \frac{\text{Total de Unidades dos Pedidos Selecionados}}{\text{Número de Corredores Selecionados}}
$$

Por exemplo, se a solução seleciona os pedidos ['O0', 'O1', 'O2', 'O4'] com um total de 10 unidades e os corredores ['A1', 'A3'] (2 corredores), então:

$$
\text{Média} = \frac{10}{2} = 5
$$

Essa média, juntamente com o total de unidades, forma o par objetivo usado para comparar as soluções.

**Resultado Obtido:**

A saída do algoritmo lista todas as soluções encontradas, por exemplo:

- *Solução 1:* Pedidos ['O3'], Corredores ['A3', 'A4'], Objetivo (média, total) = (2.5, 5)
- *Solução 2:* Pedidos ['O3'], Corredores ['A2', 'A3', 'A4'], Objetivo (média, total) = (1.67, 5)
- ...
- *Solução 309:* Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 10)

A solução ótima escolhida pelo algoritmo foi:

- **Pedidos Selecionados:** ['O0', 'O1', 'O2', 'O4']
- **Corredores Selecionados:** ['A1', 'A3']
- **Número de Corredores:** 2
- **Total de Unidades:** 10
- **Valor Objetivo (Média):** 5.0
- **Tempo de Execução:** (exemplo) 0.0179 segundos

A solução proposta retornou o **resultado correto**.

<details>
  <summary>Clique para ver a saída completa retornada pelo algoritmo.</summary>

  ```
Todas as soluções encontradas:
Solução 1: Pedidos ['O3'], Corredores ['A3', 'A4'], Objetivo (média, total) = (2.5, 5)
Solução 2: Pedidos ['O3'], Corredores ['A2', 'A3', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 3: Pedidos ['O3'], Corredores ['A1', 'A4'], Objetivo (média, total) = (2.5, 5)
Solução 4: Pedidos ['O3'], Corredores ['A1', 'A3'], Objetivo (média, total) = (2.5, 5)
Solução 5: Pedidos ['O3'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 6: Pedidos ['O3'], Corredores ['A1', 'A2'], Objetivo (média, total) = (2.5, 5)
Solução 7: Pedidos ['O3'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 8: Pedidos ['O3'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 9: Pedidos ['O3'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 10: Pedidos ['O3'], Corredores ['A0', 'A4'], Objetivo (média, total) = (2.5, 5)
Solução 11: Pedidos ['O3'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 12: Pedidos ['O3'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 13: Pedidos ['O3'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 14: Pedidos ['O3'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 15: Pedidos ['O3'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 16: Pedidos ['O3'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 17: Pedidos ['O3'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 18: Pedidos ['O3'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 19: Pedidos ['O3'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.25, 5)
Solução 20: Pedidos ['O3'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.0, 5)
Solução 21: Pedidos ['O3', 'O4'], Corredores ['A3', 'A4'], Objetivo (média, total) = (3.0, 6)
Solução 22: Pedidos ['O3', 'O4'], Corredores ['A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 23: Pedidos ['O3', 'O4'], Corredores ['A1', 'A4'], Objetivo (média, total) = (3.0, 6)
Solução 24: Pedidos ['O3', 'O4'], Corredores ['A1', 'A3'], Objetivo (média, total) = (3.0, 6)
Solução 25: Pedidos ['O3', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 26: Pedidos ['O3', 'O4'], Corredores ['A1', 'A2'], Objetivo (média, total) = (3.0, 6)
Solução 27: Pedidos ['O3', 'O4'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 28: Pedidos ['O3', 'O4'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (2.0, 6)
Solução 29: Pedidos ['O3', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 30: Pedidos ['O3', 'O4'], Corredores ['A0', 'A4'], Objetivo (média, total) = (3.0, 6)
Solução 31: Pedidos ['O3', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 32: Pedidos ['O3', 'O4'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 33: Pedidos ['O3', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 34: Pedidos ['O3', 'O4'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 35: Pedidos ['O3', 'O4'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (2.0, 6)
Solução 36: Pedidos ['O3', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 37: Pedidos ['O3', 'O4'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (2.0, 6)
Solução 38: Pedidos ['O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 39: Pedidos ['O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.5, 6)
Solução 40: Pedidos ['O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.2, 6)
Solução 41: Pedidos ['O2', 'O3'], Corredores ['A1', 'A4'], Objetivo (média, total) = (4.0, 8)
Solução 42: Pedidos ['O2', 'O3'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 43: Pedidos ['O2', 'O3'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 44: Pedidos ['O2', 'O3'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 45: Pedidos ['O2', 'O3'], Corredores ['A0', 'A4'], Objetivo (média, total) = (4.0, 8)
Solução 46: Pedidos ['O2', 'O3'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 47: Pedidos ['O2', 'O3'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 48: Pedidos ['O2', 'O3'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 49: Pedidos ['O2', 'O3'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 50: Pedidos ['O2', 'O3'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 51: Pedidos ['O2', 'O3'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 52: Pedidos ['O2', 'O3'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 53: Pedidos ['O2', 'O3'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 54: Pedidos ['O2', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.0, 8)
Solução 55: Pedidos ['O2', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.6, 8)
Solução 56: Pedidos ['O2', 'O3', 'O4'], Corredores ['A1', 'A4'], Objetivo (média, total) = (4.5, 9)
Solução 57: Pedidos ['O2', 'O3', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 58: Pedidos ['O2', 'O3', 'O4'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 59: Pedidos ['O2', 'O3', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 60: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A4'], Objetivo (média, total) = (4.5, 9)
Solução 61: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 62: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 63: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 64: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 65: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (3.0, 9)
Solução 66: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 67: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (3.0, 9)
Solução 68: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 69: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.25, 9)
Solução 70: Pedidos ['O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.8, 9)
Solução 71: Pedidos ['O1', 'O3'], Corredores ['A3', 'A4'], Objetivo (média, total) = (3.5, 7)
Solução 72: Pedidos ['O1', 'O3'], Corredores ['A2', 'A3', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 73: Pedidos ['O1', 'O3'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 74: Pedidos ['O1', 'O3'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 75: Pedidos ['O1', 'O3'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 76: Pedidos ['O1', 'O3'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 77: Pedidos ['O1', 'O3'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 78: Pedidos ['O1', 'O3'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 79: Pedidos ['O1', 'O3'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 80: Pedidos ['O1', 'O3'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 81: Pedidos ['O1', 'O3'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 82: Pedidos ['O1', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.75, 7)
Solução 83: Pedidos ['O1', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.4, 7)
Solução 84: Pedidos ['O1', 'O3', 'O4'], Corredores ['A3', 'A4'], Objetivo (média, total) = (4.0, 8)
Solução 85: Pedidos ['O1', 'O3', 'O4'], Corredores ['A2', 'A3', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 86: Pedidos ['O1', 'O3', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 87: Pedidos ['O1', 'O3', 'O4'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 88: Pedidos ['O1', 'O3', 'O4'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 89: Pedidos ['O1', 'O3', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 90: Pedidos ['O1', 'O3', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 91: Pedidos ['O1', 'O3', 'O4'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 92: Pedidos ['O1', 'O3', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 93: Pedidos ['O1', 'O3', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 94: Pedidos ['O1', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 95: Pedidos ['O1', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.0, 8)
Solução 96: Pedidos ['O1', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.6, 8)
Solução 97: Pedidos ['O1', 'O2'], Corredores ['A4'], Objetivo (média, total) = (5.0, 5)
Solução 98: Pedidos ['O1', 'O2'], Corredores ['A3', 'A4'], Objetivo (média, total) = (2.5, 5)
Solução 99: Pedidos ['O1', 'O2'], Corredores ['A2', 'A4'], Objetivo (média, total) = (2.5, 5)
Solução 100: Pedidos ['O1', 'O2'], Corredores ['A2', 'A3', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 101: Pedidos ['O1', 'O2'], Corredores ['A1', 'A4'], Objetivo (média, total) = (2.5, 5)
Solução 102: Pedidos ['O1', 'O2'], Corredores ['A1', 'A3'], Objetivo (média, total) = (2.5, 5)
Solução 103: Pedidos ['O1', 'O2'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 104: Pedidos ['O1', 'O2'], Corredores ['A1', 'A2'], Objetivo (média, total) = (2.5, 5)
Solução 105: Pedidos ['O1', 'O2'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 106: Pedidos ['O1', 'O2'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 107: Pedidos ['O1', 'O2'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 108: Pedidos ['O1', 'O2'], Corredores ['A0', 'A4'], Objetivo (média, total) = (2.5, 5)
Solução 109: Pedidos ['O1', 'O2'], Corredores ['A0', 'A3'], Objetivo (média, total) = (2.5, 5)
Solução 110: Pedidos ['O1', 'O2'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 111: Pedidos ['O1', 'O2'], Corredores ['A0', 'A2'], Objetivo (média, total) = (2.5, 5)
Solução 112: Pedidos ['O1', 'O2'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 113: Pedidos ['O1', 'O2'], Corredores ['A0', 'A2', 'A3'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 114: Pedidos ['O1', 'O2'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 115: Pedidos ['O1', 'O2'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 116: Pedidos ['O1', 'O2'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 117: Pedidos ['O1', 'O2'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 118: Pedidos ['O1', 'O2'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 119: Pedidos ['O1', 'O2'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 120: Pedidos ['O1', 'O2'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.25, 5)
Solução 121: Pedidos ['O1', 'O2'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.0, 5)
Solução 122: Pedidos ['O1', 'O2', 'O4'], Corredores ['A3', 'A4'], Objetivo (média, total) = (3.0, 6)
Solução 123: Pedidos ['O1', 'O2', 'O4'], Corredores ['A2', 'A4'], Objetivo (média, total) = (3.0, 6)
Solução 124: Pedidos ['O1', 'O2', 'O4'], Corredores ['A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 125: Pedidos ['O1', 'O2', 'O4'], Corredores ['A1', 'A4'], Objetivo (média, total) = (3.0, 6)
Solução 126: Pedidos ['O1', 'O2', 'O4'], Corredores ['A1', 'A3'], Objetivo (média, total) = (3.0, 6)
Solução 127: Pedidos ['O1', 'O2', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 128: Pedidos ['O1', 'O2', 'O4'], Corredores ['A1', 'A2'], Objetivo (média, total) = (3.0, 6)
Solução 129: Pedidos ['O1', 'O2', 'O4'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 130: Pedidos ['O1', 'O2', 'O4'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (2.0, 6)
Solução 131: Pedidos ['O1', 'O2', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 132: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A4'], Objetivo (média, total) = (3.0, 6)
Solução 133: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A3'], Objetivo (média, total) = (3.0, 6)
Solução 134: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 135: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A2'], Objetivo (média, total) = (3.0, 6)
Solução 136: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 137: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A2', 'A3'], Objetivo (média, total) = (2.0, 6)
Solução 138: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 139: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 140: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (2.0, 6)
Solução 141: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 142: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (2.0, 6)
Solução 143: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 144: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.5, 6)
Solução 145: Pedidos ['O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.2, 6)
Solução 146: Pedidos ['O1', 'O2', 'O3'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 147: Pedidos ['O1', 'O2', 'O3'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 148: Pedidos ['O1', 'O2', 'O3'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 149: Pedidos ['O1', 'O2', 'O3'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 150: Pedidos ['O1', 'O2', 'O3'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 151: Pedidos ['O1', 'O2', 'O3'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 152: Pedidos ['O1', 'O2', 'O3'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 153: Pedidos ['O1', 'O2', 'O3'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 154: Pedidos ['O1', 'O2', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.5, 10)
Solução 155: Pedidos ['O1', 'O2', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 10)
Solução 156: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (3.6666666666666665, 11)
Solução 157: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A1', 'A2', 'A4'], Objetivo (média, total) = (3.6666666666666665, 11)
Solução 158: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.75, 11)
Solução 159: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (3.6666666666666665, 11)
Solução 160: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A0', 'A2', 'A4'], Objetivo (média, total) = (3.6666666666666665, 11)
Solução 161: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.75, 11)
Solução 162: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.75, 11)
Solução 163: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.75, 11)
Solução 164: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.75, 11)
Solução 165: Pedidos ['O1', 'O2', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.2, 11)
Solução 166: Pedidos ['O0', 'O4'], Corredores ['A1', 'A3'], Objetivo (média, total) = (2.5, 5)
Solução 167: Pedidos ['O0', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 168: Pedidos ['O0', 'O4'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 169: Pedidos ['O0', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 170: Pedidos ['O0', 'O4'], Corredores ['A0', 'A3'], Objetivo (média, total) = (2.5, 5)
Solução 171: Pedidos ['O0', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 172: Pedidos ['O0', 'O4'], Corredores ['A0', 'A2', 'A3'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 173: Pedidos ['O0', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 174: Pedidos ['O0', 'O4'], Corredores ['A0', 'A1'], Objetivo (média, total) = (2.5, 5)
Solução 175: Pedidos ['O0', 'O4'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 176: Pedidos ['O0', 'O4'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 177: Pedidos ['O0', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 178: Pedidos ['O0', 'O4'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (1.6666666666666667, 5)
Solução 179: Pedidos ['O0', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.25, 5)
Solução 180: Pedidos ['O0', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.25, 5)
Solução 181: Pedidos ['O0', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.0, 5)
Solução 182: Pedidos ['O0', 'O3'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 183: Pedidos ['O0', 'O3'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 184: Pedidos ['O0', 'O3'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 185: Pedidos ['O0', 'O3'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 186: Pedidos ['O0', 'O3'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 187: Pedidos ['O0', 'O3'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (3.0, 9)
Solução 188: Pedidos ['O0', 'O3'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 189: Pedidos ['O0', 'O3'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (3.0, 9)
Solução 190: Pedidos ['O0', 'O3'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 191: Pedidos ['O0', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.25, 9)
Solução 192: Pedidos ['O0', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.8, 9)
Solução 193: Pedidos ['O0', 'O3', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 194: Pedidos ['O0', 'O3', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 195: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 196: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 197: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 198: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 199: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 200: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 201: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 202: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.5, 10)
Solução 203: Pedidos ['O0', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 10)
Solução 204: Pedidos ['O0', 'O2'], Corredores ['A1', 'A3'], Objetivo (média, total) = (3.5, 7)
Solução 205: Pedidos ['O0', 'O2'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 206: Pedidos ['O0', 'O2'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 207: Pedidos ['O0', 'O2'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 208: Pedidos ['O0', 'O2'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 209: Pedidos ['O0', 'O2'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 210: Pedidos ['O0', 'O2'], Corredores ['A0', 'A1'], Objetivo (média, total) = (3.5, 7)
Solução 211: Pedidos ['O0', 'O2'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 212: Pedidos ['O0', 'O2'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 213: Pedidos ['O0', 'O2'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 214: Pedidos ['O0', 'O2'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 215: Pedidos ['O0', 'O2'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 216: Pedidos ['O0', 'O2'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.75, 7)
Solução 217: Pedidos ['O0', 'O2'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.4, 7)
Solução 218: Pedidos ['O0', 'O2', 'O4'], Corredores ['A1', 'A3'], Objetivo (média, total) = (4.0, 8)
Solução 219: Pedidos ['O0', 'O2', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 220: Pedidos ['O0', 'O2', 'O4'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 221: Pedidos ['O0', 'O2', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 222: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 223: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 224: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A1'], Objetivo (média, total) = (4.0, 8)
Solução 225: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 226: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 227: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 228: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (2.6666666666666665, 8)
Solução 229: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.0, 8)
Solução 230: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.0, 8)
Solução 231: Pedidos ['O0', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.6, 8)
Solução 232: Pedidos ['O0', 'O2', 'O3'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (4.0, 12)
Solução 233: Pedidos ['O0', 'O2', 'O3'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (3.0, 12)
Solução 234: Pedidos ['O0', 'O2', 'O3'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (4.0, 12)
Solução 235: Pedidos ['O0', 'O2', 'O3'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (3.0, 12)
Solução 236: Pedidos ['O0', 'O2', 'O3'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (3.0, 12)
Solução 237: Pedidos ['O0', 'O2', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.4, 12)
Solução 238: Pedidos ['O0', 'O1'], Corredores ['A1', 'A3'], Objetivo (média, total) = (3.0, 6)
Solução 239: Pedidos ['O0', 'O1'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 240: Pedidos ['O0', 'O1'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (2.0, 6)
Solução 241: Pedidos ['O0', 'O1'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 242: Pedidos ['O0', 'O1'], Corredores ['A0', 'A3'], Objetivo (média, total) = (3.0, 6)
Solução 243: Pedidos ['O0', 'O1'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 244: Pedidos ['O0', 'O1'], Corredores ['A0', 'A2', 'A3'], Objetivo (média, total) = (2.0, 6)
Solução 245: Pedidos ['O0', 'O1'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 246: Pedidos ['O0', 'O1'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (2.0, 6)
Solução 247: Pedidos ['O0', 'O1'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (2.0, 6)
Solução 248: Pedidos ['O0', 'O1'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 249: Pedidos ['O0', 'O1'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (2.0, 6)
Solução 250: Pedidos ['O0', 'O1'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.5, 6)
Solução 251: Pedidos ['O0', 'O1'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.5, 6)
Solução 252: Pedidos ['O0', 'O1'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.2, 6)
Solução 253: Pedidos ['O0', 'O1', 'O4'], Corredores ['A1', 'A3'], Objetivo (média, total) = (3.5, 7)
Solução 254: Pedidos ['O0', 'O1', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 255: Pedidos ['O0', 'O1', 'O4'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 256: Pedidos ['O0', 'O1', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 257: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A3'], Objetivo (média, total) = (3.5, 7)
Solução 258: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 259: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A2', 'A3'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 260: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 261: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 262: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 263: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 264: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (2.3333333333333335, 7)
Solução 265: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (1.75, 7)
Solução 266: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (1.75, 7)
Solução 267: Pedidos ['O0', 'O1', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.4, 7)
Solução 268: Pedidos ['O0', 'O1', 'O3'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (3.6666666666666665, 11)
Solução 269: Pedidos ['O0', 'O1', 'O3'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.75, 11)
Solução 270: Pedidos ['O0', 'O1', 'O3'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (3.6666666666666665, 11)
Solução 271: Pedidos ['O0', 'O1', 'O3'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.75, 11)
Solução 272: Pedidos ['O0', 'O1', 'O3'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.75, 11)
Solução 273: Pedidos ['O0', 'O1', 'O3'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.75, 11)
Solução 274: Pedidos ['O0', 'O1', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.75, 11)
Solução 275: Pedidos ['O0', 'O1', 'O3'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.2, 11)
Solução 276: Pedidos ['O0', 'O1', 'O3', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (4.0, 12)
Solução 277: Pedidos ['O0', 'O1', 'O3', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (3.0, 12)
Solução 278: Pedidos ['O0', 'O1', 'O3', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (4.0, 12)
Solução 279: Pedidos ['O0', 'O1', 'O3', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (3.0, 12)
Solução 280: Pedidos ['O0', 'O1', 'O3', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (3.0, 12)
Solução 281: Pedidos ['O0', 'O1', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (3.0, 12)
Solução 282: Pedidos ['O0', 'O1', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (3.0, 12)
Solução 283: Pedidos ['O0', 'O1', 'O3', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.4, 12)
Solução 284: Pedidos ['O0', 'O1', 'O2'], Corredores ['A1', 'A3'], Objetivo (média, total) = (4.5, 9)
Solução 285: Pedidos ['O0', 'O1', 'O2'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 286: Pedidos ['O0', 'O1', 'O2'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (3.0, 9)
Solução 287: Pedidos ['O0', 'O1', 'O2'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 288: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 289: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 290: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (3.0, 9)
Solução 291: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (3.0, 9)
Solução 292: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 293: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (3.0, 9)
Solução 294: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.25, 9)
Solução 295: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.25, 9)
Solução 296: Pedidos ['O0', 'O1', 'O2'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (1.8, 9)
Solução 297: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A1', 'A3'], Objetivo (média, total) = (5.0, 10)
Solução 298: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A1', 'A3', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 299: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A1', 'A2', 'A3'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 300: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 301: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A3', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 302: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 303: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A4'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 304: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A3'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 305: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A3', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 306: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2'], Objetivo (média, total) = (3.3333333333333335, 10)
Solução 307: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A4'], Objetivo (média, total) = (2.5, 10)
Solução 308: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo (média, total) = (2.5, 10)
Solução 309: Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3', 'A4'], Objetivo (média, total) = (2.0, 10)

==================== SOLUÇÃO ÓTIMA ====================
Pedidos selecionados: ['O0', 'O1', 'O2', 'O4']
Corredores selecionados: ['A1', 'A3']
Número de corredores selecionados: 2
Total de unidades dos pedidos selecionados: 10
Valor objetivo (média de itens por corredor): 5.0
Tempo de execução: 0.0179 segundos
==========================================================
```
</details>

### Comparação de Waves Geradas

#### Solução 1
- **Pedidos:** ['O3']
- **Corredores:** ['A3', 'A4']
- **Objetivo:** (média = 2.5, total = 5)

Nesta solução, apenas o pedido O3 é selecionado, resultando em 5 unidades no total. Como são usados 2 corredores, a média é baixa (2.5), indicando baixa eficiência.

#### Solução 41
- **Pedidos:** ['O2', 'O3']
- **Corredores:** ['A1', 'A4']
- **Objetivo:** (média = 4.0, total = 8)

Aqui, os pedidos O2 e O3 totalizam 8 unidades. Com 2 corredores, a média é de 4.0, melhorando a eficiência, mas ainda abaixo da solução ótima.

#### Solução 21
- **Pedidos:** ['O3', 'O4']
- **Corredores:** ['A3', 'A4']
- **Objetivo:** (média = 3.0, total = 6)

Nesta configuração, os pedidos O3 e O4 somam 6 unidades, resultando em uma média de 3.0 com 2 corredores. Embora melhor que a solução com um único pedido, ainda não maximiza a produtividade.

#### Solução Ótima
- **Pedidos Selecionados:** ['O0', 'O1', 'O2', 'O4']
- **Corredores Selecionados:** ['A1', 'A3']
- **Objetivo:** (média = 5.0, total = 10)

A solução ótima agrupa quatro pedidos, atingindo 10 unidades. Com 2 corredores, a média é de 5.0, evidenciando um equilíbrio ideal entre quantidade e uso de recursos.

#### Detalhes

- **Cobertura dos Pedidos:**  
  A solução ótima inclui 4 pedidos, enquanto as demais englobam apenas 1 ou 2. Mais pedidos resultam em maior total de unidades e, consequentemente, melhor média.

- **Utilização dos Corredores:**  
  Apesar de todas as soluções utilizarem 2 corredores, a distribuição dos pedidos na solução ótima maximiza a eficiência, aumentando a média de itens por corredor.

- **Valor Objetivo:**  
  A solução ótima apresenta o maior valor (5.0) quando comparada aos valores 2.5, 3.0 e 4.0 das outras soluções, demonstrando a importância de agrupar pedidos de forma estratégica para maximizar a produtividade.

### Análise de Desempenho do CSP

- **Cenário Atual:**  
  No exemplo atual, com 10 variáveis e 1024 combinações possíveis, a enumeração completa via backtracking se mostrou extremamente eficiente, com um tempo de execução de apenas 0.0179 segundos. Esse resultado evidencia que, para o problema em escala atual, o algoritmo é muito rápido e eficaz.

  No entanto, é importante notar que o tempo de execução está diretamente relacionado ao tamanho do espaço de busca. Se o número de variáveis aumentar, o tempo de execução pode crescer exponencialmente, o que ressalta a importância de otimizações e heurísticas para problemas maiores.

- **Conclusão do Desempenho:**  
  A abordagem atual é adequada para o exemplo fornecido. Para aplicações em larga escala, adaptações e otimizações serão necessárias para manter a eficiência da resolução.

---

## Conclusão

A solução desenvolvida foi capaz de encontrar a solução ótimo descrita pelo problema. Além disso, a solução modela o problema de seleção ótima de pedidos em waves como um CSP, definindo explicitamente as variáveis, os domínios e as restrições, e utiliza a implementação do AIMA como base. A solução ótima encontrada pelo algoritmo foi:

- **Pedidos Selecionados:** ['O0', 'O1', 'O2', 'O4']
- **Corredores Selecionados:** ['A1', 'A3']
- **Número de Corredores:** 2
- **Total de Unidades:** 10
- **Valor Objetivo (Média):** 5.0
- **Tempo de Execução:** (exemplo) 0.0179 segundos

O tempo de execução exibido, demonstrando que, embora a enumeração completa seja viável para o exemplo atual, métodos heurísticos serão essenciais para problemas de maior escala.
