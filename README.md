

# `aima-python` [![Build Status](https://travis-ci.org/aimacode/aima-python.svg?branch=master)](https://travis-ci.org/aimacode/aima-python) [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/aimacode/aima-python)


Python code for the book *[Artificial Intelligence: A Modern Approach](http://aima.cs.berkeley.edu).* You can use this in conjunction with a course on AI, or for study on your own. We're looking for [solid contributors](https://github.com/aimacode/aima-python/blob/master/CONTRIBUTING.md) to help.

# Resolução do Problema de Seleção Ótima de Pedidos em Waves

Esta documentação apresenta a resolução do problema em três partes, detalhando como modelar o problema como um CSP, implementar a solução em Python (utilizando o código do AIMA) e, por fim, comparar as diferentes waves geradas, testar o exemplo fornecido e analisar o desempenho do CSP em cenários variados.

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

\[
\text{Objetivo} = \frac{\text{Total de Unidades dos Pedidos Selecionados}}{\text{Número de Corredores Selecionados}}
\]

Para desempate, é considerado também o total de unidades – ou seja, entre soluções com a mesma média, a que tiver maior total de unidades é considerada melhor.

---

## Parte 2: Implementação da Solução em Python

**Abordagem e Estrutura:**

- **Dados e Domínios:**  
  Os pedidos e os corredores são definidos conforme o exemplo (cada um representado por uma lista de quantidades) e os limites LB e UB são estabelecidos de acordo com o problema.

- **Restrição Global:**  
  Uma função de restrição verifica se o total de unidades dos pedidos selecionados está entre LB e UB e, quando a atribuição é completa, se para cada item a soma das quantidades dos pedidos selecionados não ultrapassa a soma das quantidades disponíveis nos corredores selecionados.

- **Função Objetivo:**  
  É definida uma função que retorna um par (média, total de unidades). Essa representação permite comparar soluções lexicograficamente, favorecendo a solução com maior média e, em caso de empate, a que possui maior total de unidades.

- **Método de Busca:**  
  Utiliza-se uma implementação de backtracking (adaptada do código do AIMA) que enumera todas as soluções viáveis. Com 10 variáveis (domínio binário), o espaço de busca possui 2¹⁰ = 1024 combinações, o que torna a enumeração completa viável.

**Comparação de Diferentes Waves e Destaque da Solução Ótima:**

- Durante a busca, o algoritmo gera e lista todas as soluções (waves) viáveis, exibindo para cada uma o conjunto de pedidos e corredores selecionados, bem como o valor objetivo (par: média, total de unidades).
- Ao final, a solução com o maior par (média, total de unidades) é selecionada e exibida de forma destacada para evidenciar a wave ótima.

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

**Resultado Esperado:**

A solução ótima deve ser:
- **Pedidos Selecionados:** O0, O1, O2 e O4  
  - Total de unidades:  
    - O0: 3 + 0 + 1 + 0 + 0 = 4  
    - O1: 0 + 1 + 0 + 1 + 0 = 2  
    - O2: 0 + 0 + 1 + 0 + 2 = 3  
    - O4: 0 + 1 + 0 + 0 + 0 = 1  
    - **Total = 4 + 2 + 3 + 1 = 10**
- **Corredores Selecionados:** A1 e A3  
  - Número de corredores: 2  
- **Valor Objetivo:** Média = 10 / 2 = 5

### Comparação e Cálculo do Valor Objetivo

- Cada wave gerada é avaliada pela função objetivo, que retorna o par (média, total de unidades).  
- O algoritmo exibe todas as soluções encontradas com os respectivos valores.  
- Ao final, a solução com o maior par é destacada.  
- No resultado obtido, por exemplo, são listadas soluções como:
  - *Sol 1:* Pedidos ['O3'], Corredores ['A3', 'A4'], Objetivo = (2.5, 5)
  - ...
  - *Sol 307:* Pedidos ['O0', 'O1', 'O2', 'O4'], Corredores ['A0', 'A1', 'A2', 'A3'], Objetivo = (2.5, 10)
  - E, finalmente, a solução ótima é destacada:
    - **Pedidos selecionados:** ['O0', 'O1', 'O2', 'O4']
    - **Corredores selecionados:** ['A1', 'A3']
    - **Número de Corredores:** 2
    - **Total de Unidades:** 10
    - **Valor Objetivo (Média):** 5.0

### Análise de Desempenho do CSP

- **Cenário Atual:**  
  Com 10 variáveis e 1024 combinações possíveis, a enumeração completa via backtracking é eficiente, e o tempo de execução é muito baixo para este exemplo.

- **Cenários de Maior Escala:**  
  Em problemas com um número maior de variáveis (por exemplo, com muitos pedidos e corredores), o espaço de busca cresce exponencialmente.  
  - Para tais casos, recomenda-se o uso de heurísticas como MRV (Minimum Remaining Values) para a seleção de variáveis e LCV (Least Constraining Value) para a ordenação dos valores, além de técnicas de propagação de restrições.  
  - Essas técnicas, alinhadas com a estrutura fatorada dos PSRs, podem eliminar rapidamente atribuições inviáveis, reduzindo significativamente o tempo de busca.

- **Conclusão do Desempenho:**  
  A abordagem atual é adequada para o exemplo fornecido. Para aplicações em larga escala, adaptações e otimizações são necessárias para manter a eficiência da resolução.

---

## Conclusão

A solução desenvolvida modela o problema de seleção ótima de pedidos em waves como um CSP, definindo explicitamente as variáveis, os domínios e as restrições, e utiliza a implementação do AIMA para buscar, comparar e selecionar a melhor wave.  
**Resultados Obtidos no Exemplo:**
- **Total de Unidades:** 10  
- **Número de Corredores:** 2  
- **Valor Objetivo (Média):** 5

Além disso, o algoritmo lista todas as soluções (waves) viáveis com seus respectivos valores objetivos, permitindo a comparação detalhada. A solução ótima foi destacada de forma clara, e a análise de desempenho demonstra que, embora a enumeração completa seja viável para o exemplo atual, métodos heurísticos serão essenciais para problemas de maior escala.
